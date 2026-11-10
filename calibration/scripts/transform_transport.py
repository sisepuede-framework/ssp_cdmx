#!/usr/bin/env python
"""Transport (trns/trde) calibration: Mexico national -> CDMX.

Method: inverse calibration against the SEDEMA 2022 CDMX inventory (Table 27/36,
mobile sources). The SISEPUEDE chain emissions_c ~ deminit*frac_c / occrate_c *
fuelmix * (national efficiency & EF) is linear in (deminit*frac), so per-category
multipliers are derived from the current model decomposition (2022) vs the SEDEMA
per-vehicle-category anchors:

  SEDEMA CDMX 2022 Tabla 27 (t CO2e), mapped to SISEPUEDE category definitions:
    road_light          10,584,804 = autos 4,530,064 + SUV 2,180,141 + taxis
                                     3,336,138 + vagonetas 451,940 + carga<=3.8t
                                     86,521 (SSP: "cars and light duty trucks")
    powered_bikes        3,467,819 = motocicletas
    public               2,024,579 = micro/midibus 1,029,875 + autobuses 954,113
                                     + Metrobus/Mexibus 40,591
    road_heavy_freight     912,077 = tractocamiones 310,987 + carga>3.8t 601,090
    aviation               417,812 = operacion de aeronaves
    road_heavy_regional     18,170 = terminales de autobuses de pasajeros (foraneos)
    rail_freight             6,931 = locomotoras (foraneas/patio)
    trns total          17,432,192
  Maquinaria (369,813, construction) is NOT transport (IPCC 1.A.2.g) -> inen,
  see transform_buildings_industry.py.

Key structural (CDMX-specific) re-specifications, all documented in
calibration/03_sectors/transport_research.md:
- Motorcycles: activity from official data = 589,797 CDMX motos (SEDEMA 2022
  Anexo Tabla 3) x 24,727 km/yr (CAMe 2020 Tabla 5.5) = 14.58e9 pkm (occ 1).
  Fuel efficiency = MOVES-implied effective 9.84 km/L so emissions replicate
  SEDEMA 3.468 Mt. CONUEE/CAMe nominal is 25 km/L; at 25 km/L motos would give
  ~1.3 Mt -- SEDEMA's MOVES-Mexico 2023 moto factors are ~2.6x the fuel-based
  estimate (same ratio for all CDMXyZC). Decision: replicate the benchmark.
- pkm/cap urban at territorial-activity level (SEDEMA inventory is territorial:
  includes metropolitan through-traffic, high-VKT taxis).
- occrate public 78.35 -> 25 (CDMX effective bus/micro occupancy).
- Motorcycles fuel mix -> 99.95% gasoline (SEDEMA fleet: 725 electric of 1.505M).
- Rail passenger fuel mix -> 100% electricity (Metro/Tren Ligero/Suburbano are
  electric; imported electricity is out of Scope-1 per DECISIONS.md D1).
- Freight collapsed to CDMX urban logistics (road 97.1% / rail 2.9%), water &
  air freight -> 0 (no port; AICM freight negligible combustion attribution).
- Aviation kept (AICM inside CDMX): regional aviation share tuned to 0.418 Mt.

Emission factors, elasticities, fuel efficiencies: kept national (technology),
EXCEPT powered_bikes gasoline efficiency (see above).
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
    "deminit_trde_private_and_public_per_capita_passenger_km": 13781.1,
    "deminit_trde_regional_per_capita_passenger_km": 744.2,   # kept national
    "deminit_trde_freight_mt_km": 22563.1,
    # urban passenger category shares (sum exactly 1)
    "frac_trns_pkm_dem_private_and_public_road_light": 0.5753,
    "frac_trns_pkm_dem_private_and_public_public": 0.2568,
    "frac_trns_pkm_dem_private_and_public_powered_bikes": 0.1092,
    "frac_trns_pkm_dem_private_and_public_human_powered": 0.0587,
    "frac_trns_pkm_dem_private_and_public_water_borne": 0.0,
    # regional passenger shares (sum exactly 1; rail is electric -> 0 combustion)
    "frac_trns_pkm_dem_regional_aviation": 0.2197,
    "frac_trns_pkm_dem_regional_road_heavy_regional": 0.0507,
    "frac_trns_pkm_dem_regional_road_light": 0.1344,
    "frac_trns_pkm_dem_regional_rail_passenger": 0.5952,
    "frac_trns_pkm_dem_regional_water_borne": 0.0,
    # freight category shares (sum exactly 1)
    "frac_trns_mtkm_dem_freight_road_heavy_freight": 0.9714,
    "frac_trns_mtkm_dem_freight_rail_freight": 0.0286,
    "frac_trns_mtkm_dem_freight_water_borne": 0.0,
    "frac_trns_mtkm_dem_freight_aviation": 0.0,
    # motorcycles: MOVES-implied effective efficiency (national 39.14; CONUEE 25)
    "fuelefficiency_trns_powered_bikes_gasoline_km_per_litre": 9.84,
    # CDMX-specific fuel mixes
    "frac_trns_fuelmix_powered_bikes_gasoline": 0.9995,
    "frac_trns_fuelmix_powered_bikes_electricity": 0.0005,
    "frac_trns_fuelmix_rail_passenger_electricity": 1.0,
    "frac_trns_fuelmix_rail_passenger_diesel": 0.0,
    # occupancy: CDMX effective public-road occupancy (micros dominate vkm)
    "occrate_trns_passenger_per_vehicle_public": 25.0,
}

# Baseline fuel efficiencies go flat after 2050; continue the 2049->2050 slope
# linearly to 2070 (user's trnseff version, 2026-11-10). powered_bikes excluded
# (constant MOVES-implied value above).
EXTEND_YEAR = 2050
EXTEND_COLS = [
    "fuelefficiency_trns_road_light_biofuels_km_per_litre",
    "fuelefficiency_trns_road_light_diesel_km_per_litre",
    "fuelefficiency_trns_road_light_gasoline_km_per_litre",
    "fuelefficiency_trns_road_light_hydrogen_km_per_litre",
    "fuelefficiency_trns_road_light_hydrocarbon_gas_liquids_km_per_litre",
    "fuelefficiency_trns_road_heavy_regional_diesel_km_per_litre",
    "fuelefficiency_trns_road_heavy_regional_gasoline_km_per_litre",
    "fuelefficiency_trns_road_heavy_regional_hydrogen_km_per_litre",
    "fuelefficiency_trns_road_heavy_regional_natural_gas_km_per_litre",
    "fuelefficiency_trns_road_heavy_regional_hydrocarbon_gas_liquids_km_per_litre",
    "fuelefficiency_trns_road_heavy_freight_hydrogen_km_per_litre",
    "fuelefficiency_trns_road_heavy_freight_hydrocarbon_gas_liquids_km_per_litre",
    "fuelefficiency_trns_public_hydrocarbon_gas_liquids_km_per_litre",
]


def extend_efficiency(df):
    """Linear post-2050 extension; idempotent (reads only 2049/2050, never written)."""
    y = df["year"]
    for col in EXTEND_COLS:
        v50 = df.loc[y == EXTEND_YEAR, col].iloc[0]
        slope = v50 - df.loc[y == EXTEND_YEAR - 1, col].iloc[0]
        df.loc[y > EXTEND_YEAR, col] = v50 + slope * (y[y > EXTEND_YEAR] - EXTEND_YEAR)
    return df


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
        "inverse-calibrated: CDMX urban logistics (road 0.912 Mt + rail 0.007 Mt anchors)",
    "frac_trns_pkm_dem_private_and_public_powered_bikes":
        "589,797 CDMX motos (SEDEMA 2022 Anexo T3) x 24,727 km/yr (CAMe 2020 T5.5) = 14.58e9 pkm",
    "fuelefficiency_trns_powered_bikes_gasoline_km_per_litre":
        "MOVES-implied effective km/L so motos = SEDEMA 3.468 Mt at official activity "
        "(CONUEE/CAMe 2020 T6.4 nominal 25 km/L gives ~1.3 Mt)",
    "occrate_trns_passenger_per_vehicle_public":
        "CDMX effective bus/micro occupancy (EOD 2017 / SEMOVI); 78.35->25",
}


def transform(df):
    for group, keys in GROUPS.items():
        s = sum(VALS[k] for k in keys)
        assert abs(s - 1.0) < 1e-6, f"{group} sums to {s}, expected 1"
    for col, val in VALS.items():
        L.set_col(df, col, float(val))
    return extend_efficiency(df)


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
    for col in EXTEND_COLS:
        rows.append({
            "variable": col, "subsector": "trns",
            "original_value_mex": L.baseline_value(base, col, 2060),
            "new_value_cdmx": df.loc[df["year"] == 2060, col].iloc[0], "year": 2060,
            "method": "post-2050 linear extension at the 2049->2050 slope (baseline flat after 2050)",
            "source_name": "trend extrapolation of national baseline trajectory",
            "source_url": "", "agent": "transport-agent",
        })
    L.log_change(rows)
    print(f"transport transform applied: {len(VALS)} columns set, "
          f"{len(EXTEND_COLS)} efficiencies extended past {EXTEND_YEAR}")
    r = df[df["year"] == 2022].iloc[0]
    for c in ("deminit_trde_private_and_public_per_capita_passenger_km",
              "deminit_trde_freight_mt_km",
              "frac_trns_pkm_dem_private_and_public_road_light",
              "occrate_trns_passenger_per_vehicle_public"):
        print(f"  {c} = {r[c]}")


if __name__ == "__main__":
    main()
