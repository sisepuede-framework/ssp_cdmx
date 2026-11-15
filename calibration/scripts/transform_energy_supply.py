"""CDMX energy-supply (`entc`/`enfu`/`fgtv`) re-specification — Phase 3, sector 3 of 7.

Implements DECISIONS.md D1 for the supply side: CDMX imports ~99.9% of its
electricity (ENTC constrained to in-city generation only), has no refineries or
oil/gas extraction (FGTV production activity -> ~0, endogenously), and exports
no fuels. Idempotent: sets ABSOLUTE CDMX values on its own columns only.

Levers (see 03_sectors/energy_supply_research.md for sourcing & mechanism):
  frac_enfu_fuel_demand_imported_pj_fuel_electricity          -> 0.999
  frac_enfu_fuel_demand_imported_pj_fuel_{8 fossil fuels}     -> 0.999 (no in-region
      refining/processing/mining; kills fp_*/me_* production and FGTV prod. fugitives)
  exports_enfu_pj_fuel_* (12 fuels)                           -> 0
  nemomod_entc_residual_capacity_pp_gas_gw                    -> 0.4174  (CFE turbogás etc.)
  nemomod_entc_residual_capacity_pp_solar_gw                  -> 0.16132 (distributed PV)
  nemomod_entc_residual_capacity_pp_{12 other techs}_gw       -> 0
  nemomod_entc_frac_min_share_production_pp_* (14 techs)      -> 0 (drop national mix forcing)
  frac_enfu_minimum_fuel_to_electricity_fuel_{biogas,waste}   -> 0 (no in-city WtE/biogas pp)

KEPT NATIONAL (deliberate): all ef_* (incl. ef_fgtv_* — distribution fugitives remain,
production EFs inert), energy densities, costs, efficiencies, availability factors,
activity ratios, reserve margin (1.125), transmission loss, min/max capacity sentinels
(-999), import fracs for ammonia/hydrogen/natural_gas_liquid (baseline 0, flagged).

Run:
  /Users/fabianfuentes/miniconda3/envs/ssp_mex_env/bin/python transform_energy_supply.py \
      --io ../../ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv
"""
import lib_calib as L

AGENT = "energy-supply-agent"

# --- Sources -----------------------------------------------------------------
SRC_GE = ("Global Energy - Energia y zonas industriales en la Ciudad de Mexico "
          "(417.4 MW in-city, 77% turbogas; 161.32 MW distributed PV; 99.9% imported)",
          "https://globalenergy.mx/noticias-especiales/energia-y-zonas-industriales-en-la-ciudad-de-mexico/")
SRC_PAN = ("PAN CDMX (CFE/CRE permits) - Situacion de la generacion y consumo de "
           "energia electrica en la Ciudad de Mexico",
           "https://bibliotecapancdmx.org.mx/wp-content/uploads/2021/11/15-Situacion-de-la-generacion-y-consumo-de-la-energia-electrica-en-la-Ciudad-de-Mexico180.pdf")
SRC_REF = ("Refineria 18 de Marzo (Azcapotzalco) closed 1991; no refineries or oil/gas "
           "extraction in CDMX since",
           "https://es.wikipedia.org/wiki/Refiner%C3%ADa_18_de_Marzo")
SRC_D1 = ("DECISIONS.md D1 - CDMX modeled as near-total electricity importer; "
          "no fuel exports; FGTV production -> 0",
          "calibration/DECISIONS.md")

# --- Calibration constants ---------------------------------------------------
IMPORT_FRAC = 0.999          # approved value; NOT 1.0 (keeps NemoMod non-degenerate)
# Electricity: SEDEMA 2022 in-city generation = 105,949 t CO2e (federal point sources,
# CFE turbogas etc.) ~ 1.9 PJ NG ~ 0.76 PJ elec at pp_gas eff 0.4. Local production =
# (1 - frac) x supply; gas forced to its share via min-share-production
# (applies to in-region generation only). Tuned against the model run (see memo).
IMPORT_FRAC_ELEC = 0.98344   # supply ~50.1 PJ (11,877 GWh final + losses) -> local 0.83 PJ
MIN_SHARE_GAS = 0.90
CAP_GAS_GW = 0.4174          # 417.4 MW in-city thermal (turbogas 77% + IC 18.3% + steam 4.5%)
CAP_SOLAR_GW = 0.16132       # 161.32 MW distributed PV (18,686 systems)

# Fuels whose demand CDMX imports (no in-territory generation/refining/extraction).
IMPORTED_FUELS = ["electricity", "coal", "crude", "diesel", "gasoline",
                  "hydrocarbon_gas_liquids", "kerosene", "natural_gas", "oil"]
# Left untouched (baseline import frac = 0; near-zero baseline demand — flagged):
#   ammonia, hydrogen, natural_gas_liquid

EXPORT_FUELS = ["coal", "crude", "diesel", "electricity", "gasoline",
                "hydrocarbon_gas_liquids", "kerosene", "natural_gas", "oil",
                "ammonia", "hydrogen", "natural_gas_liquid"]

PP_TECHS = ["biogas", "biomass", "coal", "coal_ccs", "gas", "gas_ccs", "geothermal",
            "hydropower", "nuclear", "ocean", "oil", "solar", "waste_incineration", "wind"]
RESIDUAL_CAP_GW = {"gas": CAP_GAS_GW, "solar": CAP_SOLAR_GW}  # all other techs -> 0

MIN_FUEL_TO_ELEC = ["biogas", "waste"]  # frac_enfu_minimum_fuel_to_electricity_* -> 0

CHANGED = (
    [f"frac_enfu_fuel_demand_imported_pj_fuel_{f}" for f in IMPORTED_FUELS]
    + [f"exports_enfu_pj_fuel_{f}" for f in EXPORT_FUELS]
    + [f"nemomod_entc_residual_capacity_pp_{t}_gw" for t in PP_TECHS]
    + [f"nemomod_entc_frac_min_share_production_pp_{t}" for t in PP_TECHS]
    + [f"frac_enfu_minimum_fuel_to_electricity_fuel_{f}" for f in MIN_FUEL_TO_ELEC]
)


def transform(df, df_base=None):
    """Set absolute CDMX energy-supply values on df (all years). Idempotent."""
    for f in IMPORTED_FUELS:
        L.set_col(df, f"frac_enfu_fuel_demand_imported_pj_fuel_{f}",
                  IMPORT_FRAC_ELEC if f == "electricity" else IMPORT_FRAC)
    for f in EXPORT_FUELS:
        L.set_col(df, f"exports_enfu_pj_fuel_{f}", 0.0)
    for t in PP_TECHS:
        L.set_col(df, f"nemomod_entc_residual_capacity_pp_{t}_gw",
                  RESIDUAL_CAP_GW.get(t, 0.0))
        L.set_col(df, f"nemomod_entc_frac_min_share_production_pp_{t}",
                  MIN_SHARE_GAS if t == "gas" else 0.0)
    for f in MIN_FUEL_TO_ELEC:
        L.set_col(df, f"frac_enfu_minimum_fuel_to_electricity_fuel_{f}", 0.0)
    return df


def main():
    args = L.cli_io()
    df_base = L.load(str(L.BASELINE))
    df = L.load(args.io)
    df = transform(df, df_base)
    L.save(df, args.io)

    def orig(col):
        return L.baseline_value(df_base, col, 2022)

    rows = []
    for f in IMPORTED_FUELS:
        col = f"frac_enfu_fuel_demand_imported_pj_fuel_{f}"
        meth = ("tuned: in-city generation share so pp_gas emits SEDEMA 105,949 t CO2e "
                "(generacion electrica, fuentes puntuales federales); rest imported (D1)"
                if f == "electricity" else
                "re-specify: no refineries/extraction/processing in CDMX since 1991 -> demand imported")
        src = SRC_GE if f == "electricity" else SRC_REF
        rows.append(dict(variable=col, subsector="enfu", original_value_mex=orig(col),
                         new_value_cdmx=IMPORT_FRAC_ELEC if f == "electricity" else IMPORT_FRAC,
                         year=2022, method=meth,
                         source_name=f"{src[0]}; {SRC_D1[0]}",
                         source_url=f"{src[1]} ; {SRC_D1[1]}", agent=AGENT))
    for f in EXPORT_FUELS:
        col = f"exports_enfu_pj_fuel_{f}"
        rows.append(dict(variable=col, subsector="enfu", original_value_mex=orig(col),
                         new_value_cdmx=0.0, year=2022,
                         method="re-specify: CDMX exports no fuels (city, no production)",
                         source_name=SRC_D1[0], source_url=SRC_D1[1], agent=AGENT))
    for t in PP_TECHS:
        col = f"nemomod_entc_residual_capacity_pp_{t}_gw"
        val = RESIDUAL_CAP_GW.get(t, 0.0)
        meth = ("direct: 417.4 MW in-city thermal capacity (CFE turbogas 77%, IC 18.3%, steam 4.5%) mapped to pp_gas"
                if t == "gas" else
                "direct: 161.32 MW distributed PV in CDMX (18,686 systems, CRE)" if t == "solar"
                else "re-specify: no such power plants inside CDMX limits")
        src = SRC_PAN if t == "gas" else SRC_GE
        rows.append(dict(variable=col, subsector="entc", original_value_mex=orig(col),
                         new_value_cdmx=val, year=2022, method=meth,
                         source_name=src[0], source_url=src[1], agent=AGENT))
        col = f"nemomod_entc_frac_min_share_production_pp_{t}"
        rows.append(dict(variable=col, subsector="entc", original_value_mex=orig(col),
                         new_value_cdmx=MIN_SHARE_GAS if t == "gas" else 0.0, year=2022,
                         method=("tuned: force in-city turbogas to cover its SEDEMA share of local "
                                 "generation (105,949 t CO2e)") if t == "gas" else
                                "re-specify: drop national generation-mix forcing (MSP) for the "
                                "tiny in-region system",
                         source_name=SRC_D1[0], source_url=SRC_D1[1], agent=AGENT))
    for f in MIN_FUEL_TO_ELEC:
        col = f"frac_enfu_minimum_fuel_to_electricity_fuel_{f}"
        rows.append(dict(variable=col, subsector="enfu", original_value_mex=orig(col),
                         new_value_cdmx=0.0, year=2022,
                         method="re-specify: would force in-region biogas/waste-to-energy plants; "
                                "CDMX has none and exports its solid waste",
                         source_name=SRC_D1[0], source_url=SRC_D1[1], agent=AGENT))
    L.log_change(rows)
    print(f"energy-supply transform applied. Columns set: {len(CHANGED)}")
    print("Kept national: ef_* (incl. ef_fgtv_*), costs, densities, efficiencies, "
          "reserve margin, transmission loss, -999 capacity sentinels, "
          "import fracs for ammonia/hydrogen/natural_gas_liquid (flagged).")


if __name__ == "__main__":
    main()
