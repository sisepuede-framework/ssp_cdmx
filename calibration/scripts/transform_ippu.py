#!/usr/bin/env python
"""IPPU calibration: Mexico national -> CDMX.

SEDEMA 2022 CDMX territorial IPPU ≈ 0.002 Mt CO2e (only HFC from residential AC
maintenance, 1,776 t). SEDEMA has NO industrial-process bucket: heavy industry
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
2. Product-use HFC/ODS: SEDEMA Scope-1 excludes refrigerant banks (counts only
   AC-maintenance ~1,776 t). Scale demscalar_ippu_product_use_* down to reconcile
   to that benchmark scope. Documented scope reconciliation (the model otherwise
   attributes CDMX's 15%-GDP share of national refrigerant emissions = 6 Mt,
   which SEDEMA does not inventory).

Emission factors kept national. Idempotent absolutes. Mutates ONLY ippu columns.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib_calib as L

SRC = "SEDEMA Inventario CDMXyZC 2022 (no IPPU bucket; heavy industry outside CDMX)"
URL = "http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf"

# product-use demand scalar: reconcile to SEDEMA Scope-1 (excludes refrigerant banks)
PRODUCT_USE_SCALAR = 0.01
PRODUCT_USE_KEYS = [
    "demscalar_ippu_product_use_ods_refrigeration",
    "demscalar_ippu_product_use_ods_other",
    "demscalar_ippu_product_use_other",
    "demscalar_ippu_product_use_lubricants",
    "demscalar_ippu_product_use_paraffin_wax",
]


def transform(df):
    # 1. zero all virgin production tonnages (recycled already 0)
    prod = [c for c in df.columns if c.startswith("prodinit_ippu_") and c.endswith("_tonne")]
    for c in prod:
        L.set_col(df, c, 0.0)
    # 2. scale product-use down to SEDEMA scope
    for c in PRODUCT_USE_KEYS:
        if c in df.columns:
            L.set_col(df, c, PRODUCT_USE_SCALAR)
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
                         "new_value_cdmx": PRODUCT_USE_SCALAR, "year": 2022,
                         "method": "product-use scaled to SEDEMA Scope-1 (excludes refrigerant banks; counts only AC maint.)",
                         "source_name": SRC, "source_url": URL, "agent": "ippu-agent"})
    L.log_change(rows)
    print(f"ippu transform applied: {len(prod)} prodinit zeroed + {len(PRODUCT_USE_KEYS)} product-use scalars")


if __name__ == "__main__":
    main()
