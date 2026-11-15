# Energy Supply (entc / enfu / fgtv) — CDMX Research & Re-specification Notes

**Agent:** energy-supply-agent · **Date retrieved:** 2026-07-04
**Governing decision:** DECISIONS.md D1 (ENTC → in-city generation only ≈ 0.106 Mt; FGTV → ~0;
CDMX modeled as near-total electricity importer). Strategy: 02_downscaling_strategy.md §3.

---

## 1. Research confirmations (live, 2026-07-04)

### 1.1 In-city electricity generation capacity — CONFIRMED 417.4 MW
- **417.4 MW** of large-scale (>500 kW) installed generation capacity within CDMX limits.
- Technology mix: **turbogás (gas turbine, natural gas) 77% · internal combustion (diesel/gas)
  18.3% · steam turbine 4.5%** — i.e. all thermal, predominantly gas.
- Ownership: ~75% CFE (e.g. Central Turbogás Nonoalco, backup for Metro), 12% private
  self-supply, 7% permits, 5% continuous self-use, 1% cogeneration.
- Sources (retrieved 2026-07-04):
  - Global Energy, "Energía y zonas industriales en la Ciudad de México":
    https://globalenergy.mx/noticias-especiales/energia-y-zonas-industriales-en-la-ciudad-de-mexico/
  - PAN CDMX (CFE/CRE permit data), "Situación de la generación y consumo de energía eléctrica
    en la Ciudad de México": https://bibliotecapancdmx.org.mx/wp-content/uploads/2021/11/15-Situacion-de-la-generacion-y-consumo-de-la-energia-electrica-en-la-Ciudad-de-Mexico180.pdf
  - CFE Nonoalco turbogás plant: https://www.gem.wiki/Central_turbog%C3%A1s_Nonoalco
- **Model value: `nemomod_entc_residual_capacity_pp_gas_gw` = 0.4174 GW** (the entire 417.4 MW
  mapped to pp_gas; the small internal-combustion/steam shares are also fossil-thermal and
  SISEPUEDE has no closer tech; keeps the ~0.1 Mt in-city ENTC magnitude of SEDEMA).

### 1.2 Distributed solar in CDMX — CONFIRMED 161.32 MW
- **18,686 distributed-generation photovoltaic systems totaling 161.32 MW** inside CDMX
  (Global Energy, citing CRE distributed-generation interconnection statistics; retrieved
  2026-07-04): https://globalenergy.mx/noticias-especiales/energia-y-zonas-industriales-en-la-ciudad-de-mexico/
- Context: national distributed generation was 3,361.69 MW at end-2023, 99.3% solar PV
  (pv magazine México, 2024-03-14): https://www.pv-magazine-mexico.com/2024/03/14/la-generacion-distribuida-en-mexico-agrego-mas-de-700-mw-en-2023-y-supera-los-3-gw-de-capacidad-instalada/
  CDMX's ~161 MW ≈ 5% of national is plausible (CDMX is among the top-5 GD states).
- **Model value: `nemomod_entc_residual_capacity_pp_solar_gw` = 0.16132 GW.**

### 1.3 ~99.9% of electricity imported — CONFIRMED
- The same Global Energy piece states CDMX brings in **"99.9% de la energía [eléctrica] que se
  utiliza"** from other states — matching the approved import fraction 0.999 exactly.
- CDMX net electricity consumption **≈ 11,877 GWh (2022)** vs. in-city capacity of only
  ~0.42 GW thermal + 0.16 GW solar (Phase-1: CONACYT PLANEAS / SENER SIE via
  https://www.reguladores.com.mx/blog/consumo-de-energia-electrica/ ; interactive source
  https://energia.conacyt.mx/planeas/electricidad/consumo). 11,877 GWh would require
  ~1.6 GW baseload-equivalent — the city physically cannot self-supply.
- **Model value: `frac_enfu_fuel_demand_imported_pj_fuel_electricity` = 0.999** (all years;
  national baseline 0.0081). NOT 1.0, to keep NemoMod non-degenerate (approved).

### 1.4 No refineries, no oil/gas extraction in CDMX — CONFIRMED
- The only refinery ever inside CDMX, **Pemex "18 de Marzo" (Azcapotzalco), was closed by
  presidential decree on 1991-03-18** and dismantled 1992–1999; the site is now Parque
  Bicentenario. CDMX has had **zero refining capacity since 1991**.
  - https://es.wikipedia.org/wiki/Refiner%C3%ADa_18_de_Marzo
  - https://elceo.com/negocios/pemex-que-le-paso-a-la-refineria-18-de-marzo-en-azcapotzalco/
  - https://expansion.mx/empresas/2024/03/26/refineria-18-de-marzo-pemex-cdmx
- Pemex's operating refineries (Tula, Salamanca, Cadereyta, Madero, Minatitlán, Salina Cruz,
  Dos Bocas) and all crude/gas extraction are outside CDMX (offshore Gulf, Tabasco, etc.).
  CDMX has **no hydrocarbon production wells** — FGTV production/venting/flaring activity = 0.
- The city DOES have a natural-gas **distribution** network → distribution fugitives
  (`ef_fgtv_distribution_*`) legitimately remain, driven by in-city gas demand.

---

## 2. How the re-specification is implemented (mechanism)

SISEPUEDE has **no `prodinit_enfu_*` variables** — fossil-fuel production (extraction `me_*`
and refining/processing `fp_*` technologies) is **endogenous in NemoMod**, sized to meet
non-imported fuel demand plus exports. Production is therefore driven to ~0 structurally by:

| Lever | Baseline (MEX, 2022) | CDMX value | Effect |
|---|---|---|---|
| `frac_enfu_fuel_demand_imported_pj_fuel_electricity` | 0.0081 | **0.999** | demand met by imports; in-region generation ≈ 0.1% |
| `frac_enfu_fuel_demand_imported_pj_fuel_{gasoline,diesel,kerosene,oil,hydrocarbon_gas_liquids,crude,coal,natural_gas}` | 0.003–0.82 | **0.999** | no in-region refining/processing/mining → kills `fp_petroleum_refinement`, `fp_natural_gas`, `me_crude/coal/natural_gas` activity and their combustion + FGTV production fugitives |
| `exports_enfu_pj_fuel_*` (12 fuels) | crude 2,180 PJ, gasoline 204, diesel 127, oil 41, kerosene 37, HGL 17, elec 7.1, … | **0** | CDMX exports no fuels; removes export-driven production |
| `nemomod_entc_residual_capacity_pp_gas_gw` | 21.28 | **0.4174** | in-city CFE turbogás + thermal (§1.1) |
| `nemomod_entc_residual_capacity_pp_solar_gw` | 5.427 | **0.16132** | CDMX distributed PV (§1.2) |
| `nemomod_entc_residual_capacity_pp_{coal,hydropower,oil,nuclear,wind,geothermal,biomass,biogas,ocean,waste_incineration,coal_ccs,gas_ccs}_gw` | up to 25.3 (hydro) | **0** | no such plants inside CDMX |
| `nemomod_entc_frac_min_share_production_pp_*` (14 techs) | national mix (gas 0.57, hydro 0.11, coal 0.07, …) | **0** | the national MSP would FORCE the national generation mix (hydro/coal/nuclear…) onto the tiny in-region production, forcing builds of techs CDMX doesn't have. Zeroed → optimizer dispatches the residual gas+solar freely |
| `frac_enfu_minimum_fuel_to_electricity_fuel_{biogas,waste}` | 0.05 | **0** | would force in-region biogas/waste-incineration power plants; CDMX has no waste-to-energy plant and exports its solid waste to Edomex landfills |

**Feasibility:** import fraction 0.999 (not 1.0) leaves a ~0.1% in-region requirement
(~12 GWh) that the 0.58 GW residual gas+solar capacity covers trivially; min/max capacity
bounds are inactive sentinels (-999); MSP=0 removes mix constraints. NemoMod stays feasible.

**REVISION 2026-11-10 — in-city generation calibrated to SEDEMA:** the note below
left pp_gas at 0 PJ (NemoMod met the 0.1% local share with solar), so ENTC ≈ 0 while
SEDEMA reports 105,949 t CO2e for in-city generation (Tabla 27, federal point sources:
CO2 105,254 t, CH4 4.65 t, N2O 2.13 t; SF6/HFC not estimated). That is ~1.9 PJ NG ≈
0.76 PJ elec at eff 0.4. Now `frac_enfu_fuel_demand_imported_pj_fuel_electricity` =
0.9894 and `nemomod_entc_frac_min_share_production_pp_gas` = 0.90 (other fossil fuels
stay at 0.999). Result 2022: pp_gas 0.7465 PJ, solar 0.083 PJ, ENTC 0.105 Mt (−0.9%).
After calibrating final electricity demand to 11,877 GWh (supply ~50.1 PJ incl. losses),
the import frac was re-tuned to **0.98344** to keep local production at 0.83 PJ
(pp_gas 0.747 PJ, ENTC 0.1051 Mt).

**Accepted quantitative note (superseded):** with 0.999 imports, modeled in-city generation ≈ 12 GWh
→ ENTC emissions ≈ 0.005 Mt, below SEDEMA's 0.106 Mt in-city figure. The gap (~0.1 Mt,
0.4% of the 23.465 Mt target) is within D1 tolerance and is the cost of the approved
single-knob import mechanism. Flagged for the Orchestrator validation pass.

## 3. Variables inspected and deliberately KEPT NATIONAL (untouched)

- All `ef_*` (incl. all `ef_fgtv_*` — distribution fugitives legitimately remain; production
  EFs become inert because production activity → 0), energy densities, `cost_enfu_*`,
  all `nemomod_entc_*` capital/fixed/variable costs, availability factors,
  input/output activity ratios, emissions-activity ratios, renewable/reserve-margin tags.
- `nemomod_entc_total_annual_{min,max}_capacity[_investment]_*`: all **-999 sentinels**
  (inactive bounds) in the baseline — left as-is.
- `nemomod_enfu_reserve_margin_fuel_electricity` = 1.125: kept national; applies to the
  residual in-region system. WATCH-ITEM: if the gated model run shows NemoMod building
  in-region capacity to satisfy reserve margin against total (not net-of-import) demand,
  revisit.
- `nemomod_enfu_renewable_energy_minimum_production_target_fuel_electricity` = 0 already.
- `frac_enfu_transmission_loss_fuel_electricity` = 0.147: kept national (technical factor).
- `frac_enfu_fuel_demand_imported_pj_fuel_{ammonia,hydrogen,natural_gas_liquid}` = 0
  (baseline): left untouched — near-zero demand fuels in the baseline; flagged as AMBIGUOUS
  for the Orchestrator (if scenarios introduce hydrogen demand, in-region reformation would
  appear; `nemomod_entc_frac_min_share_production_fp_hydrogen_*` also left national).
- `frac_fgtv_reduction_in_fugitive_leaks` = 0: policy lever, untouched.
- `nemomod_enst_*` (storage): residual capacities already 0; untouched.
- `frac_enfu_minimum_fuel_to_electricity` exists only for biogas/waste (both zeroed, §2).

## 4. Sources (all retrieved 2026-07-04)

1. Global Energy — Energía y zonas industriales en la Ciudad de México (417.4 MW; 77% turbogás;
   161.32 MW GD solar; 99.9% imported): https://globalenergy.mx/noticias-especiales/energia-y-zonas-industriales-en-la-ciudad-de-mexico/
2. PAN CDMX — Situación de la generación y consumo de energía eléctrica en la CDMX (CFE/CRE):
   https://bibliotecapancdmx.org.mx/wp-content/uploads/2021/11/15-Situacion-de-la-generacion-y-consumo-de-la-energia-electrica-en-la-Ciudad-de-Mexico180.pdf
3. Global Energy Monitor — Central turbogás Nonoalco: https://www.gem.wiki/Central_turbog%C3%A1s_Nonoalco
4. pv magazine México — GD nacional 3,361.69 MW a dic-2023 (99.3% FV):
   https://www.pv-magazine-mexico.com/2024/03/14/la-generacion-distribuida-en-mexico-agrego-mas-de-700-mw-en-2023-y-supera-los-3-gw-de-capacidad-instalada/
5. Wikipedia — Refinería 18 de Marzo (cierre 1991): https://es.wikipedia.org/wiki/Refiner%C3%ADa_18_de_Marzo
6. El CEO — Qué le pasó a la Refinería 18 de Marzo: https://elceo.com/negocios/pemex-que-le-paso-a-la-refineria-18-de-marzo-en-azcapotzalco/
7. Expansión — Así era la Refinería 18 de Marzo: https://expansion.mx/empresas/2024/03/26/refineria-18-de-marzo-pemex-cdmx
8. Reguladores.com (CONACYT PLANEAS / SENER SIE) — consumo eléctrico CDMX 11,877 GWh 2022:
   https://www.reguladores.com.mx/blog/consumo-de-energia-electrica/ (cross-check:
   https://energia.conacyt.mx/planeas/electricidad/consumo)
