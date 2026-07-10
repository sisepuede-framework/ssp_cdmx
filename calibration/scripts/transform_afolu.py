#!/usr/bin/env python
"""AFOLU calibration: Mexico national -> CDMX (livestock, cropland/soil, land use).

SEDEMA 2022 CDMX territorial AFOLU ≈ 0.067 Mt CO2e (source-only; NO LULUCF sink):
ganadería 0.042 (enteric 0.041 + manure 0.001) + agricultura 0.007 (fertilizer
0.0066 + burning 0.0001) + incendios forestales 0.0175 + quemas 0.0005.

Model (national) for CDMX after prior sectors: lvst 56.9 + soil 28.3 + lsmm 9.5.
These are driven by ABSOLUTE national inputs that population/GDP/area scaling did
not touch:
- pop_lvst_initial_* = national herd sizes (cattle 33.7M, chickens 615M, ...).
  Replaced with CDMX herds (INEGI Censo Agropecuario 2022).
- area_lndu_supremum_croplands_ha = 180.4M ha (national) drives soil N2O
  (fertilizer + urea) independent of country area. Set to CDMX cropland 19,233 ha.

CDMX herds (INEGI Censo Agropecuario 2022): poultry 50,631, sheep 32,839,
pigs 14,003, cattle 6,487 (dairy ~2,000 + nondairy ~4,487), goats 1,393; small
equine working stock (horses ~3,000, mules ~500); buffalo 0.

Emission factors kept national. Idempotent absolutes. Mutates ONLY lvst/lndu
(cropland area) columns; soil/agrc/lsmm respond endogenously.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib_calib as L

SRC = "INEGI Censo Agropecuario 2022 (CDMX) + SEDEMA Inventario 2022"
URL = "https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/CA_Def/CA_Def2022_CDMX.pdf"

LVST = {
    "pop_lvst_initial_cattle_dairy": 2000,
    "pop_lvst_initial_cattle_nondairy": 4487,
    "pop_lvst_initial_chickens": 50631,
    "pop_lvst_initial_pigs": 14003,
    "pop_lvst_initial_sheep": 32839,
    "pop_lvst_initial_goats": 1393,
    "pop_lvst_initial_horses": 3000,
    "pop_lvst_initial_mules": 500,
    "pop_lvst_initial_buffalo": 0,
}
CROPLAND_HA = 19233.0  # INEGI Censo Agropecuario 2022 CDMX agricultural area

# Soil N2O (fertilizer + urea) is driven by demand-based crop production (feeding
# 9.24M people) not by the local cropland area. CDMX imports ~95% of its food and
# farms only 19,233 ha. Scale synthetic-fertilizer and liming application to the
# CDMX-actual agricultural footprint so soil emissions match SEDEMA agri 0.007 Mt.
# Factor = CDMX fertilizer emissions target / modeled (0.0066 / 14.77 ~ 4.5e-4).
SOIL_SCALARS = {
    "demscalar_soil_fertilizer_n_per_area": 0.00045,
    "demscalar_soil_liming_per_area": 0.00045,
    "frac_lndu_receiving_fertilizer_croplands": 0.00045,
}


def transform(df):
    for col, val in LVST.items():
        if col in df.columns:
            L.set_col(df, col, float(val))
    if "area_lndu_supremum_croplands_ha" in df.columns:
        L.set_col(df, "area_lndu_supremum_croplands_ha", CROPLAND_HA)
    for col, val in SOIL_SCALARS.items():
        if col in df.columns:
            L.set_col(df, col, float(val))
    return df


def main():
    args = L.cli_io()
    df = L.load(args.io)
    base = L.load(L.BASELINE)
    df = transform(df)
    L.save(df, args.io)
    rows = []
    allvals = list(LVST.items()) + [("area_lndu_supremum_croplands_ha", CROPLAND_HA)] + list(SOIL_SCALARS.items())
    for col, val in allvals:
        if col not in df.columns:
            continue
        sub = "soil" if "soil" in col or "receiving_fertilizer" in col else ("lndu" if "lndu" in col else "lvst")
        rows.append({"variable": col, "subsector": sub,
                     "original_value_mex": L.baseline_value(base, col, 2022),
                     "new_value_cdmx": val, "year": 2022,
                     "method": "direct CDMX herd/area + fertilizer scaled to actual cropland (INEGI Censo Agropecuario 2022; CDMX imports ~95% food)",
                     "source_name": SRC, "source_url": URL, "agent": "afolu-agent"})
    L.log_change(rows)
    print(f"afolu transform applied: {len(LVST)} herds + cropland area")


if __name__ == "__main__":
    main()
