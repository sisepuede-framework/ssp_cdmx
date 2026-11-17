"""
tableau_postprocessing.py
-------------------------
Python port of the R post-processing pipeline that produces Tableau-ready
CSVs from a SISEPUEDE run output, adapted for Morocco. Replaces:

  - ssp_modeling/output_postprocessing/scr/data_prep_new_mapping.r
  - ssp_modeling/output_postprocessing/scr/data_prep_drivers.r
  - ssp_modeling/output_postprocessing/levers_and_jobs_table/* (levers + jobs tables)

Usage from a manager notebook:

    from shared_scripts.tableau_postprocessing import run_tableau_postprocessing

    run_tableau_postprocessing(
        run_dir         = RUN_ID_OUTPUT_DIR_PATH,
        project_dir     = PROJECT_DIR,
        region          = "morocco",
        iso_code3       = "MAR",
        year_ref        = 2018,
    )

Outputs land in `<project_dir>/ssp_modeling/tableau/data/`:
  - emissions_<region>_<year_ref>.csv              (raw SSP values, historical + SISEPUEDE)
  - drivers_<region>.csv                            (driver variables + GDP history)
  - tableau_levers_table_complete.csv               (levers + stakeholder merge)
  - jobs_demand_<region>.csv                        (employment subset)
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Emissions table (data_prep_new_mapping.r)
# ---------------------------------------------------------------------------

# In the model all CDMX industrial energy sits in INEN other_product_manufacturing
# (IPPU tonnages are 0, so the per-tonne categories emit nothing). For reporting,
# move the SEDEMA 2022 industrial point sources that carry an industry type
# (Tabla 27, t CO2e) to their SSP category. Denominator = everything calibrated
# into OPM: industria no regulada 2,431,878 + point sources 417,054 + maquinaria
# 369,813. Industria no regulada has no industry type -> stays in OPM.
# ponytail: shares fixed at 2022 for every year/strategy; make them time-varying
# if a strategy targets one industry type.
_OPM_SEDEMA_T = 2_431_878 + 417_054 + 369_813
INEN_OPM_SPLIT = {
    "chemicals": 78_578 / _OPM_SEDEMA_T,
    "paper":     30_846 / _OPM_SEDEMA_T,
    "textiles":  21_775 / _OPM_SEDEMA_T,
    "metals":    16_863 / _OPM_SEDEMA_T,
    "plastic":   13_437 / _OPM_SEDEMA_T,   # plástico y hule
    "glass":      3_560 / _OPM_SEDEMA_T,   # minerales no metálicos
}


FGAS_AGGREGATES = ("emission_co2e_hfcs_", "emission_co2e_pfcs_", "emission_co2e_other_fcs_")


def split_inen_opm(df: pd.DataFrame) -> pd.DataFrame:
    """Reallocate INEN OPM rows to industry-type categories by INEN_OPM_SPLIT; total preserved."""
    is_opm = (df["variable"].str.contains("_inen_")
              & df["variable"].str.endswith("other_product_manufacturing"))
    parts = []
    for cat, share in INEN_OPM_SPLIT.items():
        p = df[is_opm].copy()
        p["value"] *= share
        p["subsector_category"] = p["subsector_category"].str.replace(
            "other_product_manufacturing", cat)
        parts.append(p)
    df = df.copy()
    df.loc[is_opm, "value"] *= 1 - sum(INEN_OPM_SPLIT.values())
    return pd.concat([df, *parts], ignore_index=True)


def build_emissions_table(
    run_dir: Path,
    targets_path: Path,
    edgar_path: Path,
    iso_code3: str,
    region: str,
    year_ref: int,
    out_path: Path,
) -> pd.DataFrame:
    """Port of data_prep_new_mapping.r.

    Emissions are emitted exactly as SISEPUEDE produces them (no HP smoothing).
    Output grain is (sector, subsector, subsector_category, Gas): ``subsector_category``
    breaks each
    subsector into the SSP emission variables that compose it, so summing all
    categories within a subsector reproduces the subsector total.
    """

    # 1 — load mapping
    mapping = pd.read_csv(targets_path)
    mapping = mapping.drop(columns=[c for c in ("id", "ids", iso_code3) if c in mapping.columns])

    # 2 — load historical inventory, filter to country (OPTIONAL)
    #     CDMX has no formatted historical inventory file; if absent, the model
    #     output is emitted on its own (no historical series appended).
    if Path(edgar_path).exists():
        edgar = pd.read_csv(edgar_path)
        edgar = edgar[edgar["Code"] == iso_code3].copy()
        edgar["ID"] = edgar["subsector"].astype(str) + ":" + edgar["Gas"].astype(str)
    else:
        edgar = None
        print(f"[emissions] no historical inventory at {edgar_path} — model output only")

    # 3 — load decomposed_ssp_output, filter to region, sort
    data = pd.read_csv(run_dir / "decomposed_ssp_output.csv")
    data = data[data["region"] == region].copy()
    data = data.sort_values(["primary_id", "time_period", "region"]).reset_index(drop=True)

    # 4 — explode mapping$vars (colon-separated) into one row per SSP emission
    #     variable, carrying a `subsector_category` label = the variable name with its
    #     `emission_co2e_<gas>_<subsector_ssp>_` prefix stripped.
    id_vars = ["region", "time_period", "primary_id"]
    data_cols = set(data.columns)

    var_rows = []
    for _, row in mapping.iterrows():
        prefix = f"emission_co2e_{str(row['gas']).lower()}_{row['subsector_ssp']}_"
        for v in str(row["vars"]).split(":"):
            v = v.strip()
            # hfcs/pfcs/other_fcs are SISEPUEDE sums of the individual gases, which
            # the mapping also lists -> skip them or IPPU F-gases count twice.
            if not v or v not in data_cols or v.startswith(FGAS_AGGREGATES):
                continue
            var_rows.append({
                "variable":  v,
                "ID":        row["ID"],
                "sector":    row["sector"],
                "subsector": row["subsector"],
                "sector_es":    row["sector_es"],
                "subsector_es": row["subsector_es"],
                "Gas":       row["gas"],
                "subsector_category":  v[len(prefix):] if v.startswith(prefix) else v,
            })
    var_map = pd.DataFrame(var_rows)
    present_vars = var_map["variable"].tolist()

    # 5 — wide → long over the individual emission variables
    data_new = data[id_vars + present_vars].melt(
        id_vars=id_vars, var_name="variable", value_name="value"
    )

    # 6 — merge variable → (sector, subsector, subsector_category, Gas, ID)
    data_new = data_new.merge(var_map, on="variable", how="left")

    # 6b — reporting-only split of INEN other_product_manufacturing by industry type
    data_new = split_inen_opm(data_new)

    # 7 — aggregate to (subsector, subsector_category, gas) grain
    data_new = (
        data_new.groupby(
            ["primary_id", "time_period", "ID", "sector", "subsector", "subsector_category", "Gas",
             "sector_es", "subsector_es"],
            dropna=False,
            as_index=False,
        )["value"]
        .sum()
    )

    data_new["Year"] = data_new["time_period"] + 2015

    # 8 — merge with primary + strategy attributes
    att_primary = pd.read_csv(run_dir / "ATTRIBUTE_PRIMARY.csv")
    data_new = data_new.merge(att_primary, on="primary_id", how="left")

    att_strategy = pd.read_csv(run_dir / "ATTRIBUTE_STRATEGY.csv")[["strategy_id", "strategy"]]
    data_new = data_new.merge(att_strategy, on="strategy_id", how="left")

    # 9 — melt historic inventory wide to long (only if historical available)
    if edgar is not None:
        id_vars_edgar = ["Code", "sector", "subsector", "Gas", "ID"]
        measure_cols = [c for c in edgar.columns if re.fullmatch(r"X?\d{4}", str(c))]
        edgar_long = edgar.melt(
            id_vars=id_vars_edgar,
            value_vars=measure_cols,
            var_name="variable",
            value_name="value",
        )
        edgar_long["Year"] = edgar_long["variable"].astype(str).str.lstrip("X").astype(int)
        edgar_long = edgar_long.drop(columns=["variable"])
        edgar_long["strategy_id"] = np.nan
        edgar_long["primary_id"]  = np.nan
        edgar_long["design_id"]   = np.nan
        edgar_long["future_id"]   = np.nan
        edgar_long["Contry"]      = region
        edgar_long["strategy"]    = "Historical"
        edgar_long["source"]      = "NIR"
        edgar_long["subsector_category"]    = np.nan   # historical inventory has no subsector_category split
    else:
        edgar_long = None

    # 10 — prepare data_new for rbind
    data_new = data_new.drop(columns=["time_period"])
    data_new["Code"]   = iso_code3
    data_new["Contry"] = region
    data_new["source"] = "SISEPUEDE"

    if edgar_long is not None:
        cutoff = int(edgar_long["Year"].max())
        data_new = data_new[data_new["Year"] >= cutoff].copy()
        combined = pd.concat([data_new, edgar_long], ignore_index=True, sort=False)
    else:
        data_new = data_new[data_new["Year"] >= year_ref].copy()
        combined = data_new
    combined = combined.sort_values(
        ["strategy_id", "sector", "subsector", "Gas", "Year"], na_position="last"
    ).reset_index(drop=True)

    # 11 — Spanish subsector_category label from output_postprocessing/data/subsector_category_es.csv
    #      (next to data/invent/). Unknown categories fall back to the raw code.
    cat_es = pd.read_csv(Path(targets_path).parents[1] / "subsector_category_es.csv")
    cat_es = dict(zip(cat_es["subsector_category"], cat_es["subsector_category_es"]))
    combined["subsector_category_es"] = combined["subsector_category"].map(cat_es)
    missing = combined["subsector_category"].notna() & combined["subsector_category_es"].isna()
    if missing.any():
        print(f"[emissions] subsector_category sin traducción (se deja el código): "
              f"{sorted(combined.loc[missing, 'subsector_category'].unique())}")
        combined.loc[missing, "subsector_category_es"] = combined.loc[missing, "subsector_category"]

    # 12 — write CSV with the column order expected by Tableau
    final_cols = [
        "strategy_id", "primary_id", "ID", "sector", "subsector", "subsector_category", "value",
        "Year", "Gas", "design_id", "future_id", "strategy", "Code",
        "Contry", "source",
        # Spanish labels, appended so existing Tableau bindings keep working
        "sector_es", "subsector_es", "subsector_category_es",
    ]
    final_cols = [c for c in final_cols if c in combined.columns]
    out = combined[final_cols].copy()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    print(f"[emissions] {out_path}  ({len(out):,} rows)")
    return out


# CDMX municipal solid waste sent to Estado de México landfills (SEDEMA IRS 2023,
# receipts t/day: La Cañada 2,284.42 + El Milagro 2,269.45 + Bicentenario 1,516.40 +
# Naucalpan 476.25 + La Perseverancia 230.92). Emitted outside CDMX -> GPC scope 3,
# not in the SEDEMA territorial (scope 1) benchmark the model is calibrated to.
EXPORTED_MSW_T_PER_YEAR = 6_777.44 * 365


def build_waste_gpc_table(emissions: pd.DataFrame, run_dir: Path, out_path: Path) -> pd.DataFrame:
    """Reporting-only GPC scope-3 line: CH4 from CDMX waste landfilled in Edomex.

    The model only carries the small in-territory waste stream. Exported emissions =
    in-territory landfill CH4 x F, with F = exported tonnes / BASE-strategy 2022
    in-territory landfilled MSW tonnes (industrial 'chemical_industrial' excluded).
    F is fixed, so Basura Cero levers (food waste, recycling, compost, biogas capture)
    scale the exported line by the same proportion they cut the in-territory one.
    """
    # ponytail: exported stream assumed to behave like the in-territory landfilled
    # stream (same composition, FOD history, 20% gas recovery); model the Edomex
    # sites explicitly if site-level data (MCF, capture) becomes available.
    att = pd.read_csv(run_dir / "ATTRIBUTE_PRIMARY.csv")
    base_pid = att.loc[att["strategy_id"] == 0, "primary_id"].iloc[0]
    cols = pd.read_csv(run_dir / "decomposed_ssp_output.csv", nrows=0).columns
    lf = [c for c in cols if c.startswith("qty_waso_landfilled_") and c.endswith("_tonne")
          and "chemical_industrial" not in c]
    d = pd.read_csv(run_dir / "decomposed_ssp_output.csv", usecols=["primary_id", "time_period"] + lf)
    lf_2022 = float(d.loc[(d.primary_id == base_pid) & (d.time_period == 2022 - 2015), lf].sum(axis=1).iloc[0])
    factor = EXPORTED_MSW_T_PER_YEAR / lf_2022

    g = emissions[emissions["subsector_category"].astype(str).str.startswith("landfilled_")].copy()
    g["value"] *= factor
    g["subsector_category"] = "exported_" + g["subsector_category"]
    if "subsector_category_es" in g:
        g["subsector_category_es"] = g["subsector_category_es"].str.replace(
            "Relleno sanitario", "Relleno Edomex (exportado)")
    g["subsector"] = "4.A - Solid Waste Disposal (exported, GPC scope 3)"
    if "subsector_es" in g:
        g["subsector_es"] = "Residuos sólidos exportados al Edomex (alcance 3 GPC)"
    g["ID"] = g["subsector"] + ":" + g["Gas"].astype(str)
    g["source"] = "SISEPUEDE x GPC export factor"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    g.to_csv(out_path, index=False)
    print(f"[waste GPC] factor {factor:.1f} (exported {EXPORTED_MSW_T_PER_YEAR:,.0f} t / "
          f"in-territory landfilled {lf_2022:,.0f} t, 2022)  {out_path}  ({len(g):,} rows)")
    return g


# ---------------------------------------------------------------------------
# Drivers table (data_prep_drivers.r)
# ---------------------------------------------------------------------------

def build_drivers_table(
    run_dir: Path,
    drivers_taxonomy_path: Path,
    wide_inputs_outputs_path: Path,
    iso_code3: str,
    region: str,
    year_ref: int,
    out_path: Path,
) -> pd.DataFrame:
    """Port of data_prep_drivers.r."""

    data = pd.read_csv(run_dir / "decomposed_ssp_output.csv")
    id_vars = ["region", "time_period", "primary_id"]
    measure_cols = [c for c in data.columns if c not in id_vars]
    long_df = data.melt(id_vars=id_vars, value_vars=measure_cols,
                        var_name="variable", value_name="value")

    drivers = pd.read_csv(drivers_taxonomy_path).rename(columns={"field": "variable"})

    long_df = long_df[long_df["variable"].isin(drivers["variable"].unique())].copy()
    long_df = long_df.merge(drivers, on="variable", how="left")

    long_df["Year"] = long_df["time_period"] + 2015
    long_df = long_df.drop(columns=["time_period"])
    long_df = long_df[long_df["Year"] >= year_ref].copy()

    att_primary = pd.read_csv(run_dir / "ATTRIBUTE_PRIMARY.csv")
    long_df = long_df.merge(att_primary, on="primary_id", how="left")

    att_strategy = pd.read_csv(run_dir / "ATTRIBUTE_STRATEGY.csv")[["strategy_id", "strategy"]]
    long_df = long_df.merge(att_strategy, on="strategy_id", how="left")

    long_df["Units"]           = "NA"
    long_df["Data_Type"]       = "sisepuede simulation"
    long_df["iso_code3"]       = iso_code3
    long_df["Country"]         = region
    long_df["output_type"]     = "drivers"
    long_df["gas"]             = np.nan
    long_df = long_df.drop(columns=[c for c in ("region", "subsector_total_field",
                                                "model_variable_information") if c in long_df.columns])

    # energy_subsector classification
    energy_keywords = {
        "ccsq": "Carbon Capture and Sequestration",
        "inen": "Industrial Energy",
        "entc": "Power(electricity/heat)",
        "trns": "Transportation",
        "scoe": "Buildings",
    }
    long_df["energy_subsector"] = pd.Series(pd.NA, index=long_df.index, dtype=object)
    energy_mask = long_df["variable"].str.contains("energy", regex=False, na=False)
    es = pd.Series("TBD", index=long_df.index, dtype=object)
    for kw, label in energy_keywords.items():
        es = es.where(~long_df["variable"].str.contains(kw, regex=False, na=False), label)
    long_df.loc[energy_mask, "energy_subsector"] = es[energy_mask]
    long_df["energy_subsector_es"] = long_df["energy_subsector"].map({
        "Carbon Capture and Sequestration": "Captura y secuestro de carbono",
        "Industrial Energy": "Energía industrial",
        "Power(electricity/heat)": "Generación (electricidad/calor)",
        "Transportation": "Transporte",
        "Buildings": "Edificaciones",
        "TBD": "Por definir",
    })

    # GDP history
    gdp = pd.read_csv(wide_inputs_outputs_path, usecols=["primary_id", "time_period", "gdp_mmm_usd"])
    gdp = gdp[gdp["primary_id"] == 0].copy()
    gdp["year"] = gdp["time_period"] + 2015
    gdp = gdp[gdp["year"] <= year_ref][["year", "gdp_mmm_usd"]]

    strategies_df = (
        long_df[["strategy_id", "design_id", "future_id", "strategy"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    gdp = gdp.assign(_k=1).rename(columns={"year": "Year", "gdp_mmm_usd": "value"})
    strategies_df = strategies_df.assign(_k=1)
    drivers_hist = strategies_df.merge(gdp, on="_k").drop(columns="_k")
    drivers_hist["variable"]         = "gdp_mmm_usd"
    drivers_hist["primary_id"]       = 0
    drivers_hist["sector"]           = "Socioeconomic"
    drivers_hist["subsector"]        = "Economy"
    drivers_hist["model_variable"]   = "GDP"
    drivers_hist["category_value"]   = "('', '')"
    drivers_hist["category_name"]    = "cat_economy"
    drivers_hist["gas"]              = np.nan
    drivers_hist["gas_name"]         = ""
    drivers_hist["Units"]            = "NA"
    drivers_hist["Data_Type"]        = "historical"
    drivers_hist["iso_code3"]        = iso_code3
    drivers_hist["Country"]          = region
    drivers_hist["output_type"]      = "drivers"
    drivers_hist["energy_subsector"] = np.nan
    drivers_hist["sector_es"]        = "Socioeconómico"
    drivers_hist["subsector_es"]     = "Economía"
    drivers_hist["model_variable_es"] = "PIB"
    drivers_hist["gas_name_es"]      = ""

    years_in_sim = long_df.loc[long_df["variable"] == "gdp_mmm_usd", "Year"].dropna().unique()
    if len(years_in_sim):
        last_year_in_sim = int(min(years_in_sim))
        drivers_hist = drivers_hist[drivers_hist["Year"] < last_year_in_sim].copy()

    out_cols = [
        "variable", "strategy_id", "primary_id", "value", "sector", "subsector",
        "model_variable", "category_value", "category_name", "gas", "gas_name",
        "Year", "design_id", "future_id", "strategy", "Units", "Data_Type",
        "iso_code3", "Country", "output_type", "energy_subsector",
        # Spanish labels, appended so existing Tableau bindings keep working
        "sector_es", "subsector_es", "model_variable_es", "gas_name_es", "energy_subsector_es",
    ]
    for c in out_cols:
        if c not in long_df.columns:
            long_df[c] = np.nan
        if c not in drivers_hist.columns:
            drivers_hist[c] = np.nan

    final = pd.concat([long_df[out_cols], drivers_hist[out_cols]], ignore_index=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(out_path, index=False)
    print(f"[drivers]   {out_path}  ({len(final):,} rows)")
    return final


# ---------------------------------------------------------------------------
# Levers table
# ---------------------------------------------------------------------------

# R make.names() converts spaces and parentheses to dots.
_R_MAKE_NAMES_RENAME = {
    "Sector (output)":            "Sector..output.",
    "Subsector (output)":         "Subsector..output.",
    "Example government policies": "Example.government.policies",
}


def build_levers_table(
    run_dir: Path,
    descriptions_path: Path,
    stakeholder_codes_path: Path,
    out_path: Path,
    levers_filename: str = "levers_implementation_morocco.csv",
) -> pd.DataFrame:
    """Merges levers_implementation_<region>.csv with descriptions + stakeholder codes."""

    ssp_table = pd.read_csv(run_dir / levers_filename)
    ssp_table["transformation_code"] = ssp_table["transformer_code"].str.replace("TFR:", "", regex=False)

    desp = pd.read_csv(descriptions_path)
    scodes = pd.read_csv(stakeholder_codes_path).rename(columns=_R_MAKE_NAMES_RENAME)
    scodes["transformation_code"] = scodes["transformation_code"].str.replace("TX:", "", regex=False)

    merged = ssp_table.merge(desp, on="transformation_code", how="inner")
    merged = merged.merge(
        scodes[["transformation_code", "transformation_name_stakeholder",
                "Sector..output.", "Subsector..output.", "Example.government.policies"]],
        on="transformation_code",
        how="inner",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_path, index=False)
    print(f"[levers]    {out_path}  ({len(merged):,} rows)")
    return merged


# ---------------------------------------------------------------------------
# Jobs table
# ---------------------------------------------------------------------------

def build_jobs_table(
    employment_path: Path,
    iso_code3: str,
    out_path: Path,
) -> pd.DataFrame:
    """Splits the ":"-encoded Strategy column and filters to country."""

    jobs = pd.read_csv(employment_path)
    parts = jobs["Strategy"].astype(str).str.split(":", n=1, expand=True)
    jobs["ssp_sector"]                 = parts[0]
    jobs["ssp_transformation_name"]    = parts[1] if parts.shape[1] > 1 else ""
    jobs = jobs[jobs["Country"] == iso_code3].copy()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    jobs.to_csv(out_path, index=False)
    print(f"[jobs]      {out_path}  ({len(jobs):,} rows)")
    return jobs


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------

def run_tableau_postprocessing(
    run_dir: str | Path,
    project_dir: str | Path,
    region: str,
    iso_code3: str,
    year_ref: int,
    wide_inputs_outputs_filename: str | None = None,
    out_dir: str | Path | None = None,
    drivers_taxonomy_filename: str = "driver_variables_taxonomy_20251013.csv",
    levers_filename: str | None = None,
) -> dict:
    """Generate every Tableau-ready CSV in one call (Morocco-adapted).

    Parameters
    ----------
    run_dir : run output directory (must contain decomposed_ssp_output.csv,
        ATTRIBUTE_PRIMARY.csv, ATTRIBUTE_STRATEGY.csv,
        levers_implementation_<region>.csv, and the WIDE_INPUTS_OUTPUTS.csv).
    project_dir : repo root.
    region : region label inside the model output, e.g. "morocco".
    iso_code3 : ISO 3-letter country code, e.g. "MAR".
    year_ref : reference / calibration year (e.g. 2018).
    wide_inputs_outputs_filename : explicit filename of the WIDE_INPUTS_OUTPUTS
        file inside run_dir; if None, auto-detected.
    out_dir : where to write the Tableau CSVs (defaults to
        <project_dir>/ssp_modeling/tableau/data).
    drivers_taxonomy_filename : filename of the drivers taxonomy file under
        output_postprocessing/data/ (Morocco currently has
        driver_variables_taxonomy_20240117.csv).
    levers_filename : explicit name for the levers implementation CSV
        (default: levers_implementation_<region>.csv).
    """
    run_dir     = Path(run_dir)
    project_dir = Path(project_dir)
    out_dir     = Path(out_dir) if out_dir else project_dir / "ssp_modeling" / "tableau" / "data"

    # Auto-detect WIDE_INPUTS_OUTPUTS file
    if wide_inputs_outputs_filename is None:
        candidates = sorted(run_dir.glob("*WIDE_INPUTS_OUTPUTS.csv"))
        if not candidates:
            raise FileNotFoundError(f"No *WIDE_INPUTS_OUTPUTS.csv found in {run_dir}")
        wide_path = candidates[-1]
    else:
        wide_path = run_dir / wide_inputs_outputs_filename

    pp_root = project_dir / "ssp_modeling" / "output_postprocessing"
    pp_data = pp_root / "data"
    levers_dir = pp_root / "levers_and_jobs_table"

    targets_path           = pp_data / "invent" / f"emission_targets_{iso_code3.lower()}_{year_ref}.csv"
    edgar_path             = pp_data / "invent" / f"invent_historic_{iso_code3.lower()}.csv"
    drivers_taxonomy_path  = pp_data / drivers_taxonomy_filename
    descriptions_path      = levers_dir / "ssp_descriptions.csv"
    stakeholder_codes_path = levers_dir / "stakeholder_codes.csv"
    employment_path        = levers_dir / "Sisepuede - Employment Results - WB (SECTOR).csv"

    levers_filename = levers_filename or f"levers_implementation_{region}.csv"

    emissions = build_emissions_table(
        run_dir        = run_dir,
        targets_path   = targets_path,
        edgar_path     = edgar_path,
        iso_code3      = iso_code3,
        region         = region,
        year_ref       = year_ref,
        out_path       = out_dir / f"emissions_{region}_{year_ref}.csv",
    )
    # separate file so territorial totals in existing Tableau views are unchanged
    build_waste_gpc_table(
        emissions,
        run_dir  = run_dir,
        out_path = out_dir / f"emissions_waste_gpc_scope3_{region}_{year_ref}.csv",
    )
    drivers = build_drivers_table(
        run_dir                  = run_dir,
        drivers_taxonomy_path    = drivers_taxonomy_path,
        wide_inputs_outputs_path = wide_path,
        iso_code3                = iso_code3,
        region                   = region,
        year_ref                 = year_ref,
        out_path                 = out_dir / f"drivers_{region}.csv",
    )
    # levers + jobs are OPTIONAL: they need region-specific reference files
    # (levers implementation, stakeholder codes, employment results) that CDMX
    # does not have yet. Skip gracefully when absent.
    levers = None
    if (run_dir / levers_filename).exists() and descriptions_path.exists() and stakeholder_codes_path.exists():
        levers = build_levers_table(
            run_dir                = run_dir,
            descriptions_path      = descriptions_path,
            stakeholder_codes_path = stakeholder_codes_path,
            out_path               = out_dir / "tableau_levers_table_complete.csv",
            levers_filename        = levers_filename,
        )
    else:
        print("[levers]    skipped (reference files not present)")

    jobs = None
    if employment_path.exists():
        jobs = build_jobs_table(
            employment_path = employment_path,
            iso_code3       = iso_code3,
            out_path        = out_dir / f"jobs_demand_{region}.csv",
        )
    else:
        print("[jobs]      skipped (employment file not present)")

    return {
        "emissions": emissions,
        "drivers":   drivers,
        "levers":    levers,
        "jobs":      jobs,
    }
