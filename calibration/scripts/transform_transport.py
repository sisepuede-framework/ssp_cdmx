#!/usr/bin/env python
"""Transport (trns/trde) calibration: Mexico national -> CDMX.

Method: inverse calibration against the SEDEMA 2022 CDMX inventory (Table 27/36,
mobile sources). The SISEPUEDE chain emissions_c ~ deminit*frac_c / occrate_c *
fuelmix * (national efficiency & EF) is linear in (deminit*frac), so per-category
multipliers are derived from the current model decomposition (2022) vs the SEDEMA
per-vehicle-category anchors:

  SEDEMA CDMX 2022 (Mt CO2e): on-road 16.989 = light passenger (autos 4.530 +
  SUV 2.180 + taxis 3.336 + vagonetas 0.452) 10.498 + motorcycles 3.468 +
  public road (micro/midibus 1.030 + autobuses 0.954 + Metrobus 0.041) 2.025 +
  road freight (carga<=3.8t 0.087 + tracto 0.311 + carga>3.8t 0.601) 0.999;
  off-road aviation 0.418; locomotives ~0.024. Transport total 17.802.

Key structural (CDMX-specific) re-specifications, all documented in
calibration/03_sectors/transport_research.md:
- pkm/cap urban raised to territorial-activity level (SEDEMA inventory is
  territorial: includes metropolitan through-traffic, high-VKT taxis/motos).
- occrate public 78.35 -> 25 (CDMX effective bus/micro occupancy).
- Motorcycles fuel mix -> 99.95% gasoline (SEDEMA fleet: 725 electric of 1.505M).
- Rail passenger fuel mix -> 100% electricity (Metro/Tren Ligero/Suburbano are
  electric; imported electricity is out of Scope-1 per DECISIONS.md D1).
- Freight collapsed to CDMX urban logistics: 26,496 Mtkm (2.45% of national),
  road 91.5% / rail 8.5%, water & air freight -> 0 (no port; AICM freight
  handled at terminals, negligible combustion attribution).
- Aviation kept (AICM inside CDMX): regional aviation share tuned to 0.418 Mt.

Emission factors, fuel efficiencies, elasticities: kept national (technology).
Idempotent: absolute values only. Mutates ONLY trde/trns columns listed below.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib_calib as L

SRC = "SEDEMA Inventario de Emisiones CDMXyZC 2022"
URL = "http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf"

# --- calibrated absolute values (see module docstring for derivation) ---
VALS = {
    # demand pools (trde)
    "deminit_trde_private_and_public_per_capita_passenger_km": 15139.0,
    "deminit_trde_regional_per_capita_passenger_km": 744.2,   # kept national
    "deminit_trde_freight_mt_km": 26496.0,
    # urban passenger category shares (sum exactly 1)
    "frac_trns_pkm_dem_private_and_public_road_light": 0.6938,
    "frac_trns_pkm_dem_private_and_public_public": 0.2346,
    "frac_trns_pkm_dem_private_and_public_powered_bikes": 0.0182,
    "frac_trns_pkm_dem_private_and_public_human_powered": 0.0534,
    "frac_trns_pkm_dem_private_and_public_water_borne": 0.0,
    # regional passenger shares (sum exactly 1; rail is electric -> 0 combustion)
    "frac_trns_pkm_dem_regional_aviation": 0.2196,
    "frac_trns_pkm_dem_regional_road_heavy_regional": 0.1403,
    "frac_trns_pkm_dem_regional_road_light": 0.1344,
    "frac_trns_pkm_dem_regional_rail_passenger": 0.5057,
    "frac_trns_pkm_dem_regional_water_borne": 0.0,
    # freight category shares (sum exactly 1)
    "frac_trns_mtkm_dem_freight_road_heavy_freight": 0.9148,
    "frac_trns_mtkm_dem_freight_rail_freight": 0.0852,
    "frac_trns_mtkm_dem_freight_water_borne": 0.0,
    "frac_trns_mtkm_dem_freight_aviation": 0.0,
    # CDMX-specific fuel mixes
    "frac_trns_fuelmix_powered_bikes_gasoline": 0.9995,
    "frac_trns_fuelmix_powered_bikes_electricity": 0.0005,
    "frac_trns_fuelmix_rail_passenger_electricity": 1.0,
    "frac_trns_fuelmix_rail_passenger_diesel": 0.0,
    # occupancy: CDMX effective public-road occupancy (micros dominate vkm)
    "occrate_trns_passenger_per_vehicle_public": 25.0,
}

GROUPS = {
    "urban pkm fracs": [k for k in VALS if k.startswith("frac_trns_pkm_dem_private_and_public_")],
    "regional pkm fracs": [k for k in VALS if k.startswith("frac_trns_pkm_dem_regional_")],
    "freight mtkm fracs": [k for k in VALS if k.startswith("frac_trns_mtkm_dem_freight_")],
}

METHODS = {
    "deminit_trde_private_and_public_per_capita_passenger_km":
        "inverse-calibrated to SEDEMA per-category on-road CO2e (territorial activity)",
    "deminit_trde_regional_per_capita_passenger_km": "national default (kept)",
    "deminit_trde_freight_mt_km":
        "inverse-calibrated: CDMX urban logistics = 2.45% of national tkm (road 0.999 Mt anchor)",
    "occrate_trns_passenger_per_vehicle_public":
        "CDMX effective bus/micro occupancy (EOD 2017 / SEMOVI); 78.35->25",
}


def transform(df):
    for group, keys in GROUPS.items():
        s = sum(VALS[k] for k in keys)
        assert abs(s - 1.0) < 1e-6, f"{group} sums to {s}, expected 1"
    for col, val in VALS.items():
        L.set_col(df, col, float(val))
    return df


def main():
    args = L.cli_io()
    df = L.load(args.io)
    base = L.load(L.BASELINE)
    df = transform(df)
    L.save(df, args.io)
    rows = []
    for col, val in VALS.items():
        rows.append({
            "variable": col, "subsector": "trde" if "_trde_" in col else "trns",
            "original_value_mex": L.baseline_value(base, col, 2022),
            "new_value_cdmx": val, "year": 2022,
            "method": METHODS.get(col, "inverse-calibrated share vs SEDEMA per-category CO2e / structural CDMX re-spec"),
            "source_name": SRC, "source_url": URL, "agent": "transport-agent",
        })
    L.log_change(rows)
    print(f"transport transform applied: {len(VALS)} columns set")
    r = df[df["year"] == 2022].iloc[0]
    for c in ("deminit_trde_private_and_public_per_capita_passenger_km",
              "deminit_trde_freight_mt_km",
              "frac_trns_pkm_dem_private_and_public_road_light",
              "occrate_trns_passenger_per_vehicle_public"):
        print(f"  {c} = {r[c]}")


if __name__ == "__main__":
    main()
