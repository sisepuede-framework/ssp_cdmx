# Fuentes de calibración por variable — SISEPUEDE CDMX

Total: **238 variables** calibradas de nacional→CDMX. Cada fila registra el valor MEX original, el valor CDMX, el método y la fuente.
Fuente completa/machine-readable: `variable_sources_cdmx.csv`. Año base 2022.


## Socioeconómico (gnrl) — 5 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `area_gnrl_country_ha` | 196437500.0 | 149430.0 | direct: INEGI CDMX superficie 1,494.3 km2 = 149,430 ha | INEGI Panorama Sociodemografico de CDMX 2020 |
| `gdp_mmm_usd` | 2582.57 | 387.3855 | share: national gdp_mmm_usd * 0.150 | INEGI PIB por Entidad Federativa |
| `population_gnrl_rural` | 23982180.05 | 18475.29 | direct: CONAPO CDMX total * rural share 0.002 | CONAPO Proyecciones de Poblacion 2020-2070 |
| `population_gnrl_urban` | 104452121.6 | 9219168.71 | direct: CONAPO CDMX total * urban share 0.998 | CONAPO Proyecciones de Poblacion 2020-2070 |

## Transporte (trns/trde) — 22 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `deminit_trde_freight_mt_km` | 1081585.394 | 26496.0 | inverse-calibrated: CDMX urban logistics = 2.45% of nat | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `deminit_trde_private_and_public_per_capita_passenger` | 8772.614598 | 15139.0 | inverse-calibrated to SEDEMA per-category on-road CO2e | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `deminit_trde_regional_per_capita_passenger_km` | 744.1993982 | 744.2 | national default | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_fuelmix_powered_bikes_electricity` | 0.54974981 | 0.0005 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_fuelmix_powered_bikes_gasoline` | 0.45025019 | 0.9995 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_fuelmix_rail_passenger_diesel` | 0.480398075 | 0.0 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_fuelmix_rail_passenger_electricity` | 0.519601925 | 1.0 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_mtkm_dem_freight_aviation` | 0.000867818 | 0.0 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_mtkm_dem_freight_rail_freight` | 0.102111269 | 0.0852 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_mtkm_dem_freight_road_heavy_freight` | 0.671487231 | 0.9148 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_mtkm_dem_freight_water_borne` | 0.225533681 | 0.0 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_private_and_public_human_powered` | 0.03 | 0.0534 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_private_and_public_powered_bikes` | 0.08 | 0.0182 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_private_and_public_public` | 0.43 | 0.2346 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_private_and_public_road_light` | 0.46 | 0.6938 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_private_and_public_water_borne` | 6.9e-05 | 0.0 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_regional_aviation` | 0.33 | 0.2196 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_regional_rail_passenger` | 0.07 | 0.5057 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_regional_road_heavy_regional` | 0.3 | 0.1403 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_regional_road_light` | 0.3 | 0.1344 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `frac_trns_pkm_dem_regional_water_borne` | 6.08e-05 | 0.0 | inverse-calibrated share vs SEDEMA per-category CO2e /  | SEDEMA Inventario de Emisiones CDMXyZC 2022 |
| `occrate_trns_passenger_per_vehicle_public` | 78.34671429 | 25.0 | CDMX effective bus/micro occupancy | SEDEMA Inventario de Emisiones CDMXyZC 2022 |

## Energía-oferta (entc/enfu/fgtv) — 51 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `exports_enfu_pj_fuel_ammonia` | 0.0 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_coal` | 0.053 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_crude` | 2180.192 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_diesel` | 126.613692 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_electricity` | 7.085 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_gasoline` | 204.379509 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_hydrocarbon_gas_liquids` | 17.194452 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_hydrogen` | 0.0 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_kerosene` | 36.733602 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_natural_gas` | 0.915 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_natural_gas_liquid` | 0.0 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `exports_enfu_pj_fuel_oil` | 41.27721 | 0.0 | re-specify: CDMX exports no fuels | DECISIONS.md D1 - CDMX modeled as near-total  |
| `frac_enfu_fuel_demand_imported_pj_fuel_coal` | 0.390111262 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_crude` | 0.002677406 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_diesel` | 0.81882006 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_electricity` | 0.008128963 | 0.999 | direct: CDMX imports ~99.9% of electricity | Global Energy - Energia y zonas industriales  |
| `frac_enfu_fuel_demand_imported_pj_fuel_gasoline` | 0.81882006 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_hydrocarbon_g` | 0.81882006 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_kerosene` | 0.81882006 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_natural_gas` | 0.62 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_fuel_demand_imported_pj_fuel_oil` | 0.81882006 | 0.999 | re-specify: no refineries/extraction/processing in CDMX | Refineria 18 de Marzo |
| `frac_enfu_minimum_fuel_to_electricity_fuel_biogas` | 0.05 | 0.0 | re-specify: would force in-region biogas/waste-to-energ | DECISIONS.md D1 - CDMX modeled as near-total  |
| `frac_enfu_minimum_fuel_to_electricity_fuel_waste` | 0.05 | 0.0 | re-specify: would force in-region biogas/waste-to-energ | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_biogas` | 0.0 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_biomass` | 0.0 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_coal` | 0.073214036 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_coal_ccs` | 0.0 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_gas` | 0.566370551 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_gas_ccs` | 0.0 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_geothermal` | 0.013790336 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_hydropower` | 0.10899412 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_nuclear` | 0.032986143 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_ocean` | 0.0 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_oil` | 0.074989511 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_solar` | 0.062451737 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_waste_inci` | 0.0 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_frac_min_share_production_pp_wind` | 0.062716234 | 0.0 | re-specify: drop national generation-mix forcing | DECISIONS.md D1 - CDMX modeled as near-total  |
| `nemomod_entc_residual_capacity_pp_biogas_gw` | 0.0 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_biomass_gw` | 0.705344736 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_coal_ccs_gw` | 0.0 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_coal_gw` | 10.92634253 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_gas_ccs_gw` | 0.0 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_gas_gw` | 21.27512312 | 0.4174 | direct: 417.4 MW in-city thermal capacity
| `nemomod_entc_residual_capacity_pp_geothermal_gw` | 1.835684053 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_hydropower_gw` | 25.25548585 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_nuclear_gw` | 3.067599514 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_ocean_gw` | 0.0 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_oil_gw` | 19.12963183 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_solar_gw` | 5.426603855 | 0.16132 | direct: 161.32 MW distributed PV in CDMX | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_waste_incineration` | 0.0 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |
| `nemomod_entc_residual_capacity_pp_wind_gw` | 2.66292016 | 0.0 | re-specify: no such power plants inside CDMX limits | Global Energy - Energia y zonas industriales  |

## Edificios+Industria (scoe/inen) — 99 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `consumpinit_inen_energy_tj_per_mmm_gdp_other_product` | 241.8529984 | 150.0 | derived: 3.0 MtCO2e | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `consumpinit_inen_energy_total_pj_agriculture_and_liv` | 103.1370056 | 0.163 | derived: SEDEMA equipos agricolas 5,767 tCO2e / | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_agriculture_and_livestock_diesel` | 0.0 | 0.477148984 | re-specify: CDMX farm equipment burns diesel, not fuel  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_agriculture_and_livestock_oil` | 0.477148984 | 0.0 | re-specify: no fuel-oil use in CDMX agriculture | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_cement_coal` | 0.061150964 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_cement_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_cement_natural_gas` | 0.216703099 | 0.625598485 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_cement_oil` | 0.347744422 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_chemicals_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_chemicals_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_chemicals_natural_gas` | 0.445325278 | 0.4822183929 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_chemicals_oil` | 0.036893115 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_electronics_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_electronics_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_electronics_natural_gas` | 0.0 | 1.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_electronics_oil` | 1.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_glass_coal` | 0.061150964 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_glass_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_glass_natural_gas` | 0.216703099 | 0.625598485 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_glass_oil` | 0.347744422 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_lime_and_carbonite_coal` | 0.061150964 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_lime_and_carbonite_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_lime_and_carbonite_natural_gas` | 0.216703099 | 0.625598485 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_lime_and_carbonite_oil` | 0.347744422 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_metals_coal` | 0.207405527 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_metals_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_metals_natural_gas` | 0.377132616 | 0.592012656 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_metals_oil` | 0.007474513 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_mining_coal` | 0.001378599 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_mining_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_mining_natural_gas` | 0.446806089 | 0.485242651 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_mining_oil` | 0.037057963 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_coal` | 0.010729896 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_coke` | 0.0 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_diesel` | 0.0 | 0.06 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_electri` | 0.796631577 | 0.4 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_furnace` | 0.0 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_gasolin` | 0.0 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_hydroca` | 0.0 | 0.1 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_hydroge` | 0.0 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_kerosen` | 0.0 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_natural` | 0.059095649 | 0.44 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_oil` | 0.090190909 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_solar` | 0.0 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_other_product_manufacturing_solid_b` | 0.043351968 | 0.0 | re-specify CDMX light-industry | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_paper_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_paper_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_paper_natural_gas` | 0.367020305 | 0.433677221 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_paper_oil` | 0.066656916 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_plastic_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_plastic_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_plastic_natural_gas` | 0.349159063 | 0.493708302 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_plastic_oil` | 0.144549239 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_glass_coal` | 0.061150964 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_glass_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_glass_natural_gas` | 0.216703099 | 0.625598485 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_glass_oil` | 0.347744422 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_metals_coal` | 0.207405527 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_metals_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_metals_natural_gas` | 0.377132616 | 0.592012656 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_metals_oil` | 0.007474513 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_paper_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_paper_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_paper_natural_gas` | 0.367020305 | 0.433677221 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_paper_oil` | 0.066656916 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_plastic_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_plastic_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_plastic_natural_gas` | 0.349159063 | 0.493708302 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_plastic_oil` | 0.144549239 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_rubber_and_leather_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_rubber_and_leather_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_rubber_and_leather_natural` | 0.338573035 | 0.479020244 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_recycled_rubber_and_leather_oil` | 0.140447209 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_rubber_and_leather_coal` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_rubber_and_leather_coke` | 0.0 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_rubber_and_leather_natural_gas` | 0.338573035 | 0.479020244 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_inen_energy_rubber_and_leather_oil` | 0.140447209 | 0.0 | re-specify: no coal/coke/fuel-oil industry inside CDMX | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `consumpinit_scoe_gj_per_hh_residential_elec_applianc` | 11.97834276 | 9.5 | derived: ~27 PJ CDMX residential electricity | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `consumpinit_scoe_gj_per_hh_residential_heat_energy` | 11.97834276 | 10.4 | derived: 1.7163 MtCO2e | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `consumpinit_scoe_tj_per_mmmgdp_commercial_municipal_` | 73.35819134 | 62.0 | derived: ~24 PJ CDMX commercial electricity / 387.39 mm | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `consumpinit_scoe_tj_per_mmmgdp_commercial_municipal_` | 73.35819134 | 11.98 | derived: 0.2482 MtCO2e | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_coal` | 0.0 | 0.0 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_diesel` | 0.0 | 0.03 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_electrici` | 1.0 | 0.2 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_gasoline` | 0.0 | 0.0 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_hydrocarb` | 0.0 | 0.65 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_hydrogen` | 0.0 | 0.0 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_kerosene` | 0.0 | 0.0 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_natural_g` | 0.0 | 0.12 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_commercial_municipal_solid_bio` | 0.0 | 0.0 | re-specify CDMX commercial_municipal heat fuel mix: LP/ | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_coal` | 0.0 | 0.0 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_diesel` | 0.206319147 | 0.0 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_electricity` | 0.02775621 | 0.1 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_gasoline` | 0.073926404 | 0.0 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_hydrocarbon_gas_li` | 0.0 | 0.8 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_hydrogen` | 0.0 | 0.0 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_kerosene` | 0.073926404 | 0.0 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_natural_gas` | 0.069259123 | 0.1 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |
| `frac_scoe_heat_energy_residential_solid_biomass` | 0.548812713 | 0.0 | re-specify CDMX residential heat fuel mix: LP-dominant  | SEDEMA Inventario de Emisiones CDMX y ZC 2022 |

## IPPU — 23 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `demscalar_ippu_product_use_lubricants` | 1.0 | 0.01 | product-use scaled to SEDEMA Scope-1 | SEDEMA Inventario CDMXyZC 2022 |
| `demscalar_ippu_product_use_ods_other` | 1.0 | 0.01 | product-use scaled to SEDEMA Scope-1 | SEDEMA Inventario CDMXyZC 2022 |
| `demscalar_ippu_product_use_ods_refrigeration` | 1.0 | 0.01 | product-use scaled to SEDEMA Scope-1 | SEDEMA Inventario CDMXyZC 2022 |
| `demscalar_ippu_product_use_other` | 1.0 | 0.01 | product-use scaled to SEDEMA Scope-1 | SEDEMA Inventario CDMXyZC 2022 |
| `demscalar_ippu_product_use_paraffin_wax` | 1.0 | 0.01 | product-use scaled to SEDEMA Scope-1 | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_cement_tonne` | 49762332.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_chemicals_tonne` | 4119136.502 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_electronics_tonne` | 13065804.12 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_glass_tonne` | 454242.9998 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_lime_and_carbonite_tonne` | 65835.25978 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_metals_tonne` | 25904671.09 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_mining_tonne` | 149866929.6 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_paper_tonne` | 5732815.124 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_plastic_tonne` | 5703680.73 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_recycled_glass_tonne` | 0.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_recycled_metals_tonne` | 0.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_recycled_paper_tonne` | 0.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_recycled_plastic_tonne` | 0.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_recycled_rubber_and_leather_tonne` | 0.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_recycled_textiles_tonne` | 0.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_rubber_and_leather_tonne` | 242445.7028 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_textiles_tonne` | 852630.0083 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |
| `prodinit_ippu_wood_tonne` | 18333230.0 | 0.0 | set 0: heavy industrial production absent in CDMX | SEDEMA Inventario CDMXyZC 2022 |

## Residuos (waso/trww/wali) — 25 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `frac_wali_protein_in_diet_with_red_meat` | 0.166 | 0.022 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_protein_in_diet_without_red_meat` | 0.145 | 0.019 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_advanced_` | 0.0 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_advanced_` | 0.0 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_latrine_i` | 0.000228522 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_latrine_u` | 0.000228522 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_primary` | 0.004113394 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_secondary` | 0.261553696 | 0.179 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_secondary` | 0.261553696 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_septic` | 0.0 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_untreated` | 0.073899806 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_domestic_urban_treatment_path_untreated` | 0.398422364 | 0.821 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_industrial_treatment_path_primary` | 0.004570438 | 0.00457 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_industrial_treatment_path_secondary_aer` | 0.261553696 | 0.52311 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_industrial_treatment_path_secondary_ana` | 0.261553696 | 0.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_industrial_treatment_path_untreated_no_` | 0.073899806 | 0.0739 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_wali_ww_industrial_treatment_path_untreated_wit` | 0.398422364 | 0.39842 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `physparam_wali_daily_kg_bod_per_capita` | 0.045 | 0.006 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `physparam_wali_tonne_cod_per_mmm_gdp` | 1000.0 | 150.0 | CDMX 17.9% wastewater treated | SACMEX / INEGI |
| `frac_waso_landfill_gas_recovered` | 0.745 | 0.2 | CDMX composition/disposal | SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inven |
| `frac_waso_non_recycled_incinerated` | 0.492915926 | 0.0 | CDMX composition/disposal | SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inven |
| `frac_waso_non_recycled_landfilled` | 0.0 | 0.6 | CDMX composition/disposal | SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inven |
| `frac_waso_non_recycled_open_dump` | 0.507084074 | 0.4 | CDMX composition/disposal | SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inven |
| `qty_protein_per_capita_kg` | 0.0777 | 0.018 | CDMX composition/disposal | SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inven |
| `qty_waso_initial_municipal_waste_tonne_per_capita` | 0.355 | 0.012 | territorial: 77.7% waste exported to Edomex | SEDEMA Inventario CDMXyZC 2022 + SEDEMA Inven |

## AFOLU (lvst/soil/lndu) — 13 variables

| Variable | MEX | CDMX | Método | Fuente |
|---|---|---|---|---|
| `area_lndu_supremum_croplands_ha` | 180398300.0 | 19233.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_buffalo` | 0.0 | 0.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_cattle_dairy` | 2678454.0 | 2000.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_cattle_nondairy` | 33659912.0 | 4487.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_chickens` | 614975000.0 | 50631.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_goats` | 8817200.0 | 1393.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_horses` | 6407072.0 | 3000.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_mules` | 3290520.0 | 500.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_pigs` | 19224000.0 | 14003.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `pop_lvst_initial_sheep` | 8805415.0 | 32839.0 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `demscalar_soil_fertilizer_n_per_area` | 1.0 | 0.00045 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `demscalar_soil_liming_per_area` | 1.0 | 0.00045 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
| `frac_lndu_receiving_fertilizer_croplands` | 1.0 | 0.00045 | direct CDMX herd/area + fertilizer scaled to actual cro | INEGI Censo Agropecuario 2022 |
