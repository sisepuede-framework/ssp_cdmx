#!/usr/bin/env python
"""IPPU calibration: Mexico national -> CDMX.

SEDEMA 2022 CDMX territorial IPPU ≈ 0.102 Mt CO2e = all HFC in Tabla 27 (78 t HFC):
vehicle A/C inside "Fuentes móviles" 77.3 t (≈100.5 kt CO2e, GWP 1,300) + residential
A/C maintenance 1,776 t + point sources ~0.1 t. In SISEPUEDE mobile A/C belongs to
IPPU product_use_ods_refrigeration (IPCC 2.F.1), so it is moved from the transport
target to IPPU. SEDEMA has no N2O product-use or SF6 categories and NO
industrial-process bucket: heavy industry
(cement, steel, bulk chemicals) is OUTSIDE CDMX limits, and the few point sources
inside the city are accounted as combustion (Energy/INEN), not process.

Model (national baseline) IPPU for CDMX = 144.9 Mt = production 138.9
(chemicals 57.7, metals 51.4, cement 18.5, plastic 10.6, ...) + product-use 6.05
(GDP-driven HFC/ODS refrigerant banks).

Re-specification (DECISIONS.md D1, approved: IPPU -> ~0):
1. prodinit_ippu_*_tonne -> 0 for all industries. CDMX has no cement/steel/bulk
   chemical/mining production (physically absent). This ALSO collapses the INEN
   production-part energy (per-tonne × production) — correct, CDMX industrial
   energy is the GDP-linked light-manufacturing part set by buildings-agent.
2. Product-use HFC/ODS: the model attributes CDMX's 15%-GDP share of national
   refrigerant emissions (~6 Mt). Scale demscalar_ippu_product_use_ods_refrigeration
   so 2022 HFC = SEDEMA's 102.5 kt (vehicle + residential A/C); ods_other -> 0.

Emission factors kept national. Idempotent absolutes. Mutates ONLY ippu columns.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib_calib as L

SRC = "SEDEMA Inventario CDMXyZC 2022 (no IPPU bucket; heavy industry outside CDMX)"
URL = "http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf"

# product-use demand scalars: reconcile to SEDEMA Scope-1 (excludes refrigerant banks).
# Refrigeration tuned so 2022 HFCs = 102.5 kt CO2e = all SEDEMA Tabla 27 HFC (total
# CO2e - CO2 - 28*CH4 - 265*N2O): vehicle A/C 100.5 kt + residential A/C 1.8 kt.
# ods_other has no SEDEMA counterpart -> 0. Minor product uses kept at 0.01 (~0.3 kt).
PRODUCT_USE_SCALARS = {
    "demscalar_ippu_product_use_ods_refrigeration": 0.05611,
    "demscalar_ippu_product_use_ods_other": 0.0,
    "demscalar_ippu_product_use_other": 0.01,
    "demscalar_ippu_product_use_lubricants": 0.01,
    "demscalar_ippu_product_use_paraffin_wax": 0.01,
}
PRODUCT_USE_KEYS = list(PRODUCT_USE_SCALARS)

# Sources that bypass prodinit and are not in the SEDEMA inventory -> 0:
#  - OPM N2O/SF6 (IPCC 2.G): EF per mmm GDP x GDP, not scaled by demscalar;
#    0.108 Mt in 2022, grew with GDP.
#  - cement clinker: national net imports (-174,431 t = Mexico's clinker exports) were
#    copied unscaled; with zero production the model "produced" that export
#    (0.091 Mt CO2). CDMX has no clinker kilns.
OUT_OF_SCOPE = {
    "ef_ippu_tonne_n2o_per_mmm_gdp_other_product_manufacturing": "N2O from other product manufacture/use (IPCC 2.G.3) not inventoried by SEDEMA",
    "ef_ippu_tonne_sf6_per_mmm_gdp_other_product_manufacturing": "SF6 from electrical equipment (IPCC 2.G.1) not inventoried by SEDEMA",
    "net_imports_cement_clinker_tonne": "national clinker exports copied unscaled; no clinker kilns in CDMX",
}


def transform(df):
    # 1. zero all virgin production tonnages (recycled already 0)
    prod = [c for c in df.columns if c.startswith("prodinit_ippu_") and c.endswith("_tonne")]
    for c in prod:
        L.set_col(df, c, 0.0)
    # 2. scale product-use down to SEDEMA scope
    for c, v in PRODUCT_USE_SCALARS.items():
        if c in df.columns:
            L.set_col(df, c, v)
    # 3. zero GDP/household-driven sources outside SEDEMA scope
    for c in OUT_OF_SCOPE:
        L.set_col(df, c, 0.0)
    return df


def main():
    args = L.cli_io()
    df = L.load(args.io)
    base = L.load(L.BASELINE)
    prod = [c for c in df.columns if c.startswith("prodinit_ippu_") and c.endswith("_tonne")]
    df = transform(df)
    L.save(df, args.io)
    rows = []
    for c in prod:
        rows.append({"variable": c, "subsector": "ippu",
                     "original_value_mex": L.baseline_value(base, c, 2022),
                     "new_value_cdmx": 0.0, "year": 2022,
                     "method": "set 0: heavy industrial production absent in CDMX (SEDEMA has no IPPU bucket)",
                     "source_name": SRC, "source_url": URL, "agent": "ippu-agent"})
    for c in PRODUCT_USE_KEYS:
        if c in df.columns:
            rows.append({"variable": c, "subsector": "ippu",
                         "original_value_mex": L.baseline_value(base, c, 2022),
                         "new_value_cdmx": PRODUCT_USE_SCALARS[c], "year": 2022,
                         "method": "product-use scaled to SEDEMA Scope-1 (excludes refrigerant banks; refrigeration tuned to all SEDEMA HFC 102.5 kt: vehicle + residential A/C)",
                         "source_name": SRC, "source_url": URL, "agent": "ippu-agent"})
    for c, why in OUT_OF_SCOPE.items():
        rows.append({"variable": c, "subsector": "ippu",
                     "original_value_mex": L.baseline_value(base, c, 2022),
                     "new_value_cdmx": 0.0, "year": 2022,
                     "method": f"set 0: {why}",
                     "source_name": SRC, "source_url": URL, "agent": "ippu-agent"})
    L.log_change(rows)
    print(f"ippu transform applied: {len(prod)} prodinit zeroed + {len(PRODUCT_USE_KEYS)} product-use scalars "
          f"+ {len(OUT_OF_SCOPE)} out-of-scope sources zeroed")


if __name__ == "__main__":
    main()
