"""CDMX buildings & industrial energy (`scoe`/`inen`) re-specification — Phase 3, sector 4 of 7.

Anchored to SEDEMA Inventario 2022 (CDMX-only): SCOE target 1.965 Mt CO2e
(habitacional 1,439,796 + domesticas 276,535 -> residential; comercial 222,081 +
asados 26,102 -> commercial) and INEN GDP-linked target ~3.0 Mt (industria no
regulada 2,431,878 + local point-source combustion ~580 kt). Full derivations in
calibration/03_sectors/buildings_industry_research.md.

Levers:
  SCOE residential:  heat fracs -> LP .80 / NG .10 / elec .10 (biomass/diesel/
                     kerosene/gasoline -> 0); consumpinit heat 11.98 -> 10.40 GJ/hh;
                     elec_appliances 11.98 -> 9.50 GJ/hh (trajectory rescaled).
  SCOE commercial:   heat fracs -> LP .65 / NG .12 / diesel .03 / elec .20;
                     consumpinit heat 73.36 -> 11.98 TJ/mmm-GDP; elec_appliances
                     73.36 -> 62.0 TJ/mmm-GDP (trajectory rescaled).
  INEN:              agriculture_and_livestock total 103.14 -> 0.163 PJ (SEDEMA
                     equipos agricolas 5,767 t CO2e; oil frac moved to diesel);
                     other_product_manufacturing intensity 241.85 -> 219.4 TJ/mmm
                     with mix elec .40 / NG .44 / LP .10 / diesel .06;
                     all production-category fuel mixes: coal+coke+oil -> natural
                     gas (no coal/coke/fuel-oil industry inside CDMX).

KEPT NATIONAL: efficfactor_scoe_*, elasticity_scoe_*, scalar_scoe_*, per-tonne
inen intensities, scalar_inen_*, textiles (100% elec), wood/recycled_wood (zero
frac groups), other_se segment (zero consumption). prodinit_ippu_* NOT touched
(owned by ippu-agent); INEN production part (~15-17 Mt) collapses when ippu runs.

Idempotent: all targets computed from the Mexico BASELINE, set as absolutes.
Run:
  python transform_buildings_industry.py \
      --io ../../ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv
"""
import numpy as np

import lib_calib as L

AGENT = "buildings-industry-energy-agent"
YEAR = 2022

# --- Sources -----------------------------------------------------------------
SRC_INV = ("SEDEMA Inventario de Emisiones CDMX y ZC 2022 - Tabla 3 (GyCEI CDMX), "
           "Tabla 4 (balance de energia por sector/combustible), seccion 1.1",
           "https://www.sedema.cdmx.gob.mx/ (inventario 2022; pre-extracted text)")
SRC_RES = ("Derivation: calibration/03_sectors/buildings_industry_research.md "
           "(IPCC 2006 CO2 EFs: LP 63.1, NG 56.1, diesel 74.1 kg/GJ)",
           "calibration/03_sectors/buildings_industry_research.md")

# --- SCOE calibration constants ----------------------------------------------
SCOE_FUELS = ["coal", "diesel", "electricity", "gasoline", "hydrocarbon_gas_liquids",
              "hydrogen", "kerosene", "natural_gas", "solid_biomass"]

# CDMX residential heat mix: LP-dominant, NG secondary, no firewood (urban).
FRAC_RES = {"hydrocarbon_gas_liquids": 0.80, "natural_gas": 0.10, "electricity": 0.10}
# CDMX commercial heat mix: LP 80/NG 15/diesel 4 of combustion + electric share.
FRAC_COM = {"hydrocarbon_gas_liquids": 0.65, "natural_gas": 0.12, "diesel": 0.03,
            "electricity": 0.20}

# consumpinit 2022 targets (trajectory rescaled from baseline shape).
RES_HEAT_GJ_HH = 10.40      # 1.7163 MtCO2e / 2.766M hh / 59.67 kgCO2 per GJ demand
# Electric appliances scaled so total CDMX final electricity (scoe + inen + trns) =
# 11,877 GWh = 42.76 PJ (2022, CONACYT PLANEAS / SENER SIE); inen (11.9 PJ, tied to
# the OPM combustion mix) and trns (Metro etc., 1.9 PJ) kept -> scoe 28.93 PJ.
# Previous 9.50 / 62.0 gave 18,540 GWh (+56%). Factor 0.5317 on appliances.
RES_ELEC_GJ_HH = 5.051      # -> ~1,535 kWh/hh/yr incl. electric heat
COM_HEAT_TJ_MMM = 25.53     # tuned: 0.263 Mt at 11.98 (post elasticity fix) -> 0.5602
                            # = comercial-institucional 0.222 + comercios y servicios
                            # regulados 0.312 (point source) + asados al carbon 0.026
COM_ELEC_TJ_MMM = 32.96     # -> ~13.6 PJ commercial electricity (2022)

# Commercial per-GDP elasticities: national baseline has +13.07 in 2019; with the
# 2020 COVID GDP/cap drop (-8.6%) the growth factor 1+e*r = -0.117 flips the sign
# and commercial heat demand/emissions go NEGATIVE from 2020 on (also nationally).
# Fix: hold pre-2020 values at the 2020 value (-0.5), where the smooth projection
# trajectory starts. Residential elasticities do not flip (min factor > 0) -> kept.
ELAST_FIX_YEAR = 2020
ELAST_FIX_COLS = [
    "elasticity_scoe_enerdem_per_mmmgdp_commercial_municipal_heat_energy_to_gdppc",
    "elasticity_scoe_enerdem_per_mmmgdp_commercial_municipal_elec_appliances_to_gdppc",
]

# Projection elasticities -> 0 after the 2022 benchmark. National trajectories ramp
# to 1.0 by 2050: residential per-hh demand doubled with income (saturated urban LP
# cooking/water heating) and commercial per-GDP intensity grew with GDP/cap on top of
# GDP (double-counted growth, x4.8 by 2060). With 0, residential follows households
# and commercial follows GDP. 2022 calibration untouched.
ELAST_ZERO_AFTER = 2022
ELAST_ZERO_COLS = ELAST_FIX_COLS + [
    "elasticity_scoe_enerdem_per_hh_residential_heat_energy_to_gdppc",
    "elasticity_scoe_enerdem_per_hh_residential_elec_appliances_to_gdppc",
]

# --- INEN calibration constants ----------------------------------------------
INEN_AGRI_PJ = 0.163        # 5,767 tCO2e equipos agricolas / (0.4771 diesel x 74.1)
INEN_OPM_TJ_MMM = 157.69    # tuned: OPM 3.428 Mt at 168.1 -> 3.216 target = SEDEMA
                            # industria no regulada 2.432 + industrial point 0.417 +
                            # maquinaria 0.370 (construction off-road, IPCC 1.A.2.g)
                            # - model agri 0.009; "Comercios y servicios regulados"
                            # (0.312 point source) moved to SCOE commercial.
# ponytail: maquinaria folded into OPM intensity with the light-industry mix (not a
# diesel-only stream); split it out if construction-machinery transformers matter.
FRAC_OPM = {"electricity": 0.40, "natural_gas": 0.44,
            "hydrocarbon_gas_liquids": 0.10, "diesel": 0.06}

INEN_FUELS = ["coal", "coke", "diesel", "electricity", "furnace_gas", "gasoline",
              "hydrocarbon_gas_liquids", "hydrogen", "kerosene", "natural_gas",
              "oil", "solar", "solid_biomass"]
# Production categories whose baseline mix contains coal/coke/oil -> shift to NG.
INEN_SHIFT_CATS = ["cement", "chemicals", "electronics", "glass",
                   "lime_and_carbonite", "metals", "mining", "paper", "plastic",
                   "recycled_glass", "recycled_metals", "recycled_paper",
                   "recycled_plastic", "recycled_rubber_and_leather",
                   "rubber_and_leather"]
# Untouched: textiles/recycled_textiles (100% elec), wood/recycled_wood (zero group).


def _rescale(df, df_base, col, target_2022):
    """Set col to the baseline trajectory rescaled so that 2022 == target_2022."""
    base = df_base[col].to_numpy(dtype=float)
    b22 = df_base.loc[df_base["year"] == YEAR, col].iloc[0]
    df[col] = base * (target_2022 / b22)
    return b22


def _base22(df_base, col):
    return float(df_base.loc[df_base["year"] == YEAR, col].iloc[0])


def transform(df, df_base):
    """Set absolute CDMX SCOE/INEN values on df. Idempotent (targets from baseline)."""
    changed = []

    # --- SCOE fuel fracs (residential + commercial_municipal; other_se untouched)
    for seg, mix in (("residential", FRAC_RES), ("commercial_municipal", FRAC_COM)):
        assert abs(sum(mix.values()) - 1.0) < 1e-9
        for f in SCOE_FUELS:
            col = f"frac_scoe_heat_energy_{seg}_{f}"
            L.set_col(df, col, mix.get(f, 0.0))
            changed.append(col)
        tot = sum(df[f"frac_scoe_heat_energy_{seg}_{f}"].iloc[0] for f in SCOE_FUELS)
        assert abs(tot - 1.0) < 1e-9, f"scoe {seg} fracs sum {tot}"

    # --- SCOE commercial elasticities: remove pre-2020 sign-flipping values
    y = df["year"]
    for col in ELAST_FIX_COLS:
        df.loc[y < ELAST_FIX_YEAR, col] = df.loc[y == ELAST_FIX_YEAR, col].iloc[0]
        changed.append(col)

    # --- SCOE projection elasticities: 0 after benchmark (no income-driven growth)
    for col in ELAST_ZERO_COLS:
        df.loc[y > ELAST_ZERO_AFTER, col] = 0.0
        changed.append(col)

    # --- SCOE consumption intensities (rescaled trajectories)
    for col, tgt in [
        ("consumpinit_scoe_gj_per_hh_residential_heat_energy", RES_HEAT_GJ_HH),
        ("consumpinit_scoe_gj_per_hh_residential_elec_appliances", RES_ELEC_GJ_HH),
        ("consumpinit_scoe_tj_per_mmmgdp_commercial_municipal_heat_energy", COM_HEAT_TJ_MMM),
        ("consumpinit_scoe_tj_per_mmmgdp_commercial_municipal_elec_appliances", COM_ELEC_TJ_MMM),
    ]:
        _rescale(df, df_base, col, tgt)
        changed.append(col)

    # --- INEN agriculture: absolute PJ + oil->diesel
    _rescale(df, df_base, "consumpinit_inen_energy_total_pj_agriculture_and_livestock",
             INEN_AGRI_PJ)
    changed.append("consumpinit_inen_energy_total_pj_agriculture_and_livestock")
    oil_b = df_base["frac_inen_energy_agriculture_and_livestock_oil"].to_numpy(dtype=float)
    dsl_b = df_base["frac_inen_energy_agriculture_and_livestock_diesel"].to_numpy(dtype=float)
    L.set_col(df, "frac_inen_energy_agriculture_and_livestock_diesel", dsl_b + oil_b)
    L.set_col(df, "frac_inen_energy_agriculture_and_livestock_oil", 0.0)
    changed += ["frac_inen_energy_agriculture_and_livestock_diesel",
                "frac_inen_energy_agriculture_and_livestock_oil"]

    # --- INEN other_product_manufacturing: intensity + full CDMX light-industry mix
    _rescale(df, df_base,
             "consumpinit_inen_energy_tj_per_mmm_gdp_other_product_manufacturing",
             INEN_OPM_TJ_MMM)
    changed.append("consumpinit_inen_energy_tj_per_mmm_gdp_other_product_manufacturing")
    assert abs(sum(FRAC_OPM.values()) - 1.0) < 1e-9
    for f in INEN_FUELS:
        col = f"frac_inen_energy_other_product_manufacturing_{f}"
        L.set_col(df, col, FRAC_OPM.get(f, 0.0))
        changed.append(col)

    # --- INEN production categories: coal + coke + oil -> natural gas (from baseline)
    for cat in INEN_SHIFT_CATS:
        cols = {f: f"frac_inen_energy_{cat}_{f}" for f in INEN_FUELS
                if f"frac_inen_energy_{cat}_{f}" in df.columns}
        base = {f: df_base[c].to_numpy(dtype=float) for f, c in cols.items()}
        shift = base["coal"] + base["coke"] + base["oil"]
        L.set_col(df, cols["coal"], 0.0)
        L.set_col(df, cols["coke"], 0.0)
        L.set_col(df, cols["oil"], 0.0)
        L.set_col(df, cols["natural_gas"], base["natural_gas"] + shift)
        changed += [cols["coal"], cols["coke"], cols["oil"], cols["natural_gas"]]
        tot = sum(df[c].to_numpy(dtype=float) for c in cols.values())
        base_tot = sum(base.values())
        assert np.allclose(tot, base_tot) and np.allclose(tot[np.abs(base_tot - 1) < 1e-6], 1.0), \
            f"inen {cat} frac sum broken"

    return changed


def main():
    args = L.cli_io()
    df_base = L.load(str(L.BASELINE))
    df = L.load(args.io)
    changed = transform(df, df_base)
    L.save(df, args.io)

    def row(col, val, meth, src):
        return dict(variable=col, subsector=("scoe" if "scoe" in col else "inen"),
                    original_value_mex=_base22(df_base, col), new_value_cdmx=val,
                    year=YEAR, method=meth, source_name=f"{src[0]}; {SRC_RES[0]}",
                    source_url=f"{src[1]} ; {SRC_RES[1]}", agent=AGENT)

    rows = []
    for seg, mix, name in (("residential", FRAC_RES, "LP-dominant urban cooking/water heating, firewood ~0"),
                           ("commercial_municipal", FRAC_COM, "LP/NG/diesel commercial combustion per Tabla 4")):
        for f in SCOE_FUELS:
            col = f"frac_scoe_heat_energy_{seg}_{f}"
            rows.append(row(col, mix.get(f, 0.0),
                            f"re-specify CDMX {seg} heat fuel mix: {name}", SRC_INV))
    rows.append(row("consumpinit_scoe_gj_per_hh_residential_heat_energy", RES_HEAT_GJ_HH,
                    "derived: 1.7163 MtCO2e (habitacional+domesticas) / 2.766M hh / "
                    "59.67 kgCO2 per GJ demand (mix-weighted, effic-adjusted); trajectory rescaled",
                    SRC_INV))
    rows.append(row("consumpinit_scoe_gj_per_hh_residential_elec_appliances", RES_ELEC_GJ_HH,
                    "tuned: total CDMX final electricity = 11,877 GWh (CONACYT PLANEAS / "
                    "SENER SIE 2022); appliances x0.5317; trajectory rescaled", SRC_INV))
    rows.append(row("consumpinit_scoe_tj_per_mmmgdp_commercial_municipal_heat_energy",
                    COM_HEAT_TJ_MMM,
                    "tuned: 0.5602 MtCO2e (comercial-institucional + comercios regulados + asados) after "
                    "elasticity fix; trajectory rescaled", SRC_INV))
    rows.append(row("consumpinit_scoe_tj_per_mmmgdp_commercial_municipal_elec_appliances",
                    COM_ELEC_TJ_MMM,
                    "tuned: total CDMX final electricity = 11,877 GWh (CONACYT PLANEAS / "
                    "SENER SIE 2022); appliances x0.5317; trajectory rescaled", SRC_INV))
    rows.append(row("consumpinit_inen_energy_total_pj_agriculture_and_livestock",
                    INEN_AGRI_PJ,
                    "derived: SEDEMA equipos agricolas 5,767 tCO2e / (0.4771 diesel x "
                    "74.1 kgCO2/GJ) = 0.163 PJ; national 103.14 PJ not applicable to CDMX",
                    SRC_INV))
    rows.append(row("frac_inen_energy_agriculture_and_livestock_diesel",
                    float(df["frac_inen_energy_agriculture_and_livestock_diesel"].iloc[7]),
                    "re-specify: CDMX farm equipment burns diesel, not fuel oil (oil share moved)",
                    SRC_INV))
    rows.append(row("frac_inen_energy_agriculture_and_livestock_oil", 0.0,
                    "re-specify: no fuel-oil use in CDMX agriculture", SRC_INV))
    rows.append(row("consumpinit_inen_energy_tj_per_mmm_gdp_other_product_manufacturing",
                    INEN_OPM_TJ_MMM,
                    "tuned: 3.216 MtCO2e = industria no regulada 2.432 + industrial point "
                    "sources 0.417 + maquinaria 0.370 - model agri 0.009 (comercios "
                    "regulados -> SCOE); trajectory rescaled", SRC_INV))
    for col in ELAST_FIX_COLS:
        rows.append(row(col, float(df.loc[df["year"] == ELAST_FIX_YEAR, col].iloc[0]),
                        "pre-2020 values held at 2020 value: national +13.07 (2019) x "
                        "COVID GDP/cap drop flipped commercial demand negative", SRC_INV))
    for col in ELAST_ZERO_COLS:
        rows.append(row(col, 0.0,
                        "set 0 after 2022: national ramp to 1.0 doubled per-hh demand and "
                        "double-counted commercial growth; res follows households, com follows GDP",
                        SRC_INV))
    for f in INEN_FUELS:
        col = f"frac_inen_energy_other_product_manufacturing_{f}"
        rows.append(row(col, FRAC_OPM.get(f, 0.0),
                        "re-specify CDMX light-industry (food/beverage/print) mix: "
                        "elec .40 / NG .44 / LP .10 / diesel .06; no coal/oil/biomass",
                        SRC_INV))
    for cat in INEN_SHIFT_CATS:
        for f in ("coal", "coke", "oil", "natural_gas"):
            col = f"frac_inen_energy_{cat}_{f}"
            rows.append(row(col, float(df[col].iloc[7]),
                            "re-specify: no coal/coke/fuel-oil industry inside CDMX; "
                            "share shifted to natural gas (group sum preserved)", SRC_INV))
    L.log_change(rows)

    n = len(set(changed))
    print(f"buildings-industry transform applied. Columns set: {n}")
    print("Targets 2022: SCOE res 1.716 + com 0.560; INEN 3.225 (incl. agri, maquinaria).")
    print("Kept national: efficfactor/scalar scoe, pre-2022 elasticities (except commercial pre-2020), per-tonne inen "
          "intensities, scalar_inen_*, textiles/wood frac groups, other_se, "
          "prodinit_ippu_* (ippu-agent).")


if __name__ == "__main__":
    main()
