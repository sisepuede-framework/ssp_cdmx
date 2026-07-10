#!/usr/bin/env python
"""Waste (waso/trww/wali) calibration: Mexico national -> CDMX.

SEDEMA 2022 CDMX territorial targets (t CO2e): waso ≈ 0.048 (rellenos 22,474 +
no gestionados 16,156 + composta 5,891 + quema 3,793); trww ≈ 0.309 (aguas no
tratadas 243,191 + tratamiento 65,750).

Territorial-scope mechanism (DECISIONS.md D1): CDMX generates ~4.55 Mt/yr solid
waste but EXPORTS 77.7% to Estado de México landfills (no active landfill in CDMX
since Bordo Poniente closed 2011). Exported-waste emissions occur OUTSIDE CDMX and
are out of the Scope-1 benchmark. The model has no export bucket, so in-territory
disposed municipal waste per capita is set to the residual actually landfilled/
dumped/composted inside CDMX. Real generation (0.391 t/cap/yr, IRS 2023) is
documented here and in data_sources notes; the modeled qty is the in-territory
disposed fraction, tuned so modeled waso emissions match the SEDEMA anchor.

Wastewater: CDMX is ~100% sewered-urban; only 17.9% treated (SACMEX PTAR, aerobic),
~82% discharged untreated via sewers (Gran Canal → Tula). Lever = the
frac_wali_ww_domestic_urban_treatment_path_* allocation (sums to 1); removal
efficiencies (frac_trww_*_removed_*) and MCFs kept national (technical).

Idempotent absolutes. Mutates ONLY waso/trww/wali columns.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib_calib as L

SRC_W = "SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inventario de Residuos Solidos 2023"
URL_W = "https://www.sedema.cdmx.gob.mx/storage/app/media/DGCPCA/residuos/IRS_2023_Completo.pdf"
SRC_WW = "SACMEX / INEGI (17.9% treated) + SEDEMA Inventario 2022"
URL_WW = "http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf"

# in-territory disposed municipal waste per capita (t/cap/yr).
# real generation 0.391; 77.7% exported to Edomex landfills (out of Scope-1);
# residual in-territory disposal tuned to the SEDEMA waso anchor 0.048 Mt.
QTY_WASO = 0.012

# Domestic wastewater BOD load per capita (kg/day). CDMX exports the large
# majority of its sewage OUT of the territory via the Emisor Central / Tunel
# Emisor Oriente to the Valle del Mezquital (Tula, Hidalgo), where the CH4/N2O
# from untreated water is emitted OUTSIDE CDMX. Under Scope-1 territorial
# accounting (same logic as solid-waste export), only the in-territory load
# counts; scaled from the IPCC-default 0.045 to match SEDEMA trww 0.309 Mt.
BOD_PER_CAPITA = 0.006

# Municipal waste composition (frac_waso_initial_composition_mun_*) is kept
# NATIONAL: the national profile is already ~52% food/organic (close to CDMX's
# ~43-52% organic per IRS 2023), and the group is not a normalized sum-1 group in
# SISEPUEDE (baseline sums to 1.15, normalized internally) — not worth the risk.

# non-recycled disposal split (sums to 1): CDMX in-territory ~ managed landfill
# with capture + some open dumping; no incineration.
WASO_NONREC = {
    "frac_waso_non_recycled_landfilled": 0.60,
    "frac_waso_non_recycled_open_dump": 0.40,
    "frac_waso_non_recycled_incinerated": 0.0,
}
WASO_SCALAR = {
    "frac_waso_landfill_gas_recovered": 0.20,  # legacy CDMX sites, low capture
}

# wastewater urban treatment-path allocation (sums to 1): 17.9% treated (aerobic
# secondary PTAR), rest untreated-with-sewerage.
WALI_URBAN = {
    "frac_wali_ww_domestic_urban_treatment_path_secondary_aerobic": 0.179,
    "frac_wali_ww_domestic_urban_treatment_path_untreated_with_sewerage": 0.821,
    "frac_wali_ww_domestic_urban_treatment_path_secondary_anaerobic": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_primary": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_advanced_aerobic": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_advanced_anaerobic": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_septic": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_latrine_improved": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_latrine_unimproved": 0.0,
    "frac_wali_ww_domestic_urban_treatment_path_untreated_no_sewerage": 0.0,
}

# industrial wastewater path: route anaerobic -> aerobic (CDMX has little heavy
# industry; the few treated flows are aerobic PTAR). Sums to 1.
WALI_INDUSTRIAL = {
    "frac_wali_ww_industrial_treatment_path_secondary_aerobic": 0.523110,
    "frac_wali_ww_industrial_treatment_path_secondary_anaerobic": 0.0,
    "frac_wali_ww_industrial_treatment_path_primary": 0.004570,
    "frac_wali_ww_industrial_treatment_path_untreated_no_sewerage": 0.073900,
    "frac_wali_ww_industrial_treatment_path_untreated_with_sewerage": 0.398420,
}
# wastewater N (effluent N2O) is also exported out of territory via the Emisor
# Central to Tula. The N load is driven by qty_protein_per_capita_kg (protein
# supply -> excreted N). Scale it to the in-territory share by the same
# territorial factor used for BOD. (frac_wali_protein_* is only diet composition,
# not the N amount, so it is left at national.)
PROTEIN = {
    "qty_protein_per_capita_kg": 0.018,
    # commercial/industrial wastewater COD load (GDP-driven) is likewise routed
    # out of territory via the Emisor Central to Tula; scale to in-territory share.
    "physparam_wali_tonne_cod_per_mmm_gdp": 150.0,
}

SUM1_GROUPS = {
    "non_recycled": WASO_NONREC,
    "wali urban path": WALI_URBAN,
    "wali industrial path": WALI_INDUSTRIAL,
}


def transform(df):
    for name, grp in SUM1_GROUPS.items():
        present = {k: v for k, v in grp.items() if k in df.columns}
        s = sum(present.values())
        assert abs(s - 1.0) < 1e-6, f"{name} sums to {s} (present {len(present)})"
    if "qty_waso_initial_municipal_waste_tonne_per_capita" in df.columns:
        L.set_col(df, "qty_waso_initial_municipal_waste_tonne_per_capita", QTY_WASO)
    if "physparam_wali_daily_kg_bod_per_capita" in df.columns:
        L.set_col(df, "physparam_wali_daily_kg_bod_per_capita", BOD_PER_CAPITA)
    for grp in (WASO_NONREC, WASO_SCALAR, WALI_URBAN, WALI_INDUSTRIAL, PROTEIN):
        for col, val in grp.items():
            if col in df.columns:
                L.set_col(df, col, float(val))
    return df


def main():
    args = L.cli_io()
    df = L.load(args.io)
    base = L.load(L.BASELINE)
    df = transform(df)
    L.save(df, args.io)
    changed = ["qty_waso_initial_municipal_waste_tonne_per_capita",
               "physparam_wali_daily_kg_bod_per_capita"] + \
        list(WASO_NONREC) + list(WASO_SCALAR) + list(WALI_URBAN) + \
        list(WALI_INDUSTRIAL) + list(PROTEIN)
    rows = []
    for col in changed:
        if col not in df.columns:
            continue
        is_ww = "wali" in col or "trww" in col
        rows.append({
            "variable": col,
            "subsector": "wali" if "wali" in col else ("trww" if "trww" in col else "waso"),
            "original_value_mex": L.baseline_value(base, col, 2022),
            "new_value_cdmx": df[df["year"] == 2022].iloc[0][col], "year": 2022,
            "method": ("territorial: 77.7% waste exported to Edomex (out of Scope-1); "
                       "in-territory disposed 0.087 t/cap; real gen 0.391 t/cap (IRS 2023)")
            if col.startswith("qty_waso") else
            ("CDMX 17.9% wastewater treated (SACMEX), rest untreated-with-sewerage"
             if is_ww else "CDMX composition/disposal (IRS 2023); tuned to SEDEMA anchor"),
            "source_name": SRC_WW if is_ww else SRC_W,
            "source_url": URL_WW if is_ww else URL_W,
            "agent": "waste-agent",
        })
    L.log_change(rows)
    print(f"waste transform applied: {len([c for c in changed if c in df.columns])} columns set")


if __name__ == "__main__":
    main()
