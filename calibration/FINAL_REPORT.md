# SISEPUEDE CDMX Calibration — Final Report

**Date:** 2026-07-06 · **Benchmark year:** 2022 · **Env:** `ssp_mex_env`

## 1. Result

The national Mexico SISEPUEDE input database was calibrated to Ciudad de México
and validated against the **SEDEMA 2022 territorial (Scope-1) GHG inventory =
23.465 Mt CO2e**.

| Sector (SISEPUEDE→SEDEMA) | Model Mt | SEDEMA Mt | Dev | Gate (±15%) |
|---|---:|---:|---:|:--:|
| Transport | 17.431 | 17.432 | −0% | ✅ |
| Energy (scoe+inen+fgtv+entc) | 5.678 | 5.607 | +1% | ✅ |
| IPPU | 0.260 | 0.002 | abs 0.26 | ✅* |
| Waste (waso+trww) | 0.881 | 0.361 | +144% | ⚠️ documented |
| AFOLU (agrc+lvst+lsmm+soil) | 0.043 | 0.067 | abs 0.02 | ✅* |
| **TOTAL (gross, excl. FRST)** | **24.293** | **23.465** | **+3.5%** | ✅ **PASS ±10%** |

Transport share of gross = **71.8%** (SEDEMA 74.3% excl. maquinaria, target ±5 pp ✅).

**Revision 2026-11-10 (energy):** (1) SCOE commercial emissions were NEGATIVE from
2020 on: the national elasticity of commercial per-GDP demand is +13.07 in 2019, and
with the 2020 COVID GDP/cap drop (−8.6%) the growth factor 1+e·r = −0.117 flipped the
sign (same flaw in the national baseline). Pre-2020 commercial elasticities are now
held at the 2020 value (−0.5). (2) SEDEMA "Comercios y servicios regulados" (0.312 Mt
point source) moved from `inen` to SCOE commercial. Energy split now: SCOE residential
1.757 vs 1.716 · commercial 0.560 vs 0.560 · INEN 3.225 vs 3.225 · ENTC 0.105 vs 0.106
· FGTV 0.028 vs ~0. (3) ENTC in-city generation calibrated: SEDEMA "Generación,
transmisión y distribución de energía eléctrica" = 105,949 t CO2e (federal point
sources, CFE turbogas; combustion only, imported power excluded). Electricity import
frac 0.999 → 0.9894 (now 0.98344, see 4) and `nemomod_entc_frac_min_share_production_pp_gas` = 0.90 →
pp_gas 0.75 PJ (~207 GWh, ~6% capacity factor of 417.4 MW). Constant share, so ENTC
grows with demand (0.236 Mt in 2060). (4) Final electricity demand calibrated to 11,877 GWh (2022,
CONACYT PLANEAS / SENER SIE): it was 18,540 GWh (+56%). Residential/commercial appliance
intensities ×0.5317 (9.50 → 5.051 GJ/hh; 62.0 → 32.96 TJ/mmm); inen and trns electricity
kept. Split: residential 15.3 PJ (~1,540 kWh/hh) · commercial 13.6 · industry 11.9 ·
transport 1.9. Electricity import frac re-tuned 0.9894 → 0.98344 so in-city generation
stays 0.83 PJ (ENTC 0.105 Mt). No Scope-1 change.
*IPPU/AFOLU: % is meaningless at ~0; both within 0.4 Mt absolute.

**Revision 2026-11-10 (transport category re-mapping):** SEDEMA categories were
re-mapped to the official SISEPUEDE `$CAT-TRANSPORTATION$` definitions —
motorcycles → `powered_bikes` (was `road_light`), carga ≤3.8 t → `road_light`,
terminales de autobuses → `road_heavy_regional`, locomotoras (6,931 t) →
`rail_freight`, and **maquinaria (0.370 Mt, construction off-road) moved from
Transport to Energy (`inen`, IPCC 1.A.2.g)**; hence the SEDEMA column now reads
Transport 17.432 / Energy 5.607. All 10 trns categories match SEDEMA within ±0.3%.
Motorcycle efficiency is the MOVES-implied effective 9.84 km/L (see
`03_sectors/transport_research.md`).

## 2. Methodology

- **Baseline:** untouched Mexico national inputs preserved in
  `reference_mexico/`; every CDMX value written by a reproducible, idempotent
  script in `scripts/` (`transform_<sector>.py`), chained by `run_all.sh`.
- **Drivers (direct replace):** population 9.24M (CONAPO/Censo), GDP 15% of
  national, households (occupancy 3.34), area 149,430 ha.
- **Activity (direct / share):** vehicle fleet, fuel, electricity demand, waste
  tonnage, cropland 19,233 ha, livestock heads — all from official sources.
- **Structural re-specifications (Scope-1):**
  - **ENTC → ~0** (CDMX imports 99.9% of electricity; only in-city generation
    counts; imported power out of Scope-1).
  - **FGTV → ~0** (no oil/gas extraction/refining in CDMX).
  - **IPPU → ~0** (no heavy industry; production zeroed; SEDEMA has no IPPU bucket).
  - **Transport** inverse-calibrated to SEDEMA per-vehicle-category CO2e; pkm/cap
    reflects territorial (metropolitan) activity; Metro/rail = electric (0 combustion).
  - **Territorial export** of solid waste (to Edomex landfills) and wastewater
    (to Tula/Mezquital via Emisor Central) — emissions out of Scope-1.
- **Kept national:** emission factors, fuel efficiencies, energy densities,
  per-tonne intensities, MCFs (technology identical to national) — except
  powered_bikes gasoline efficiency (MOVES-implied 9.84 km/L).

## 3. Convergence path (2022 gross, Mt CO2e)

715.6 (national) → 442.9 (socioeconomic) → 345.5 (energy-supply) → 315.5
(transport) → 305.9 (buildings-industry) → 296.4 (waste) → 121.9 (IPPU) → 43.3
(AFOLU livestock) → 27.2 (AFOLU soil) → 23.68 (waste/energy refinements).
See `04_validation/convergence_log.csv`.

## 4. Known limitations / documented exceptions

- **Waste +144% (0.88 vs 0.36 Mt):** reduced 14× from the national-scaled 12.5 Mt
  via documented territorial export (solid waste → Edomex; wastewater → Tula).
  The residual is an irreducible methodological difference — SISEPUEDE's
  IPCC-default wastewater COD/BOD/N accounting exceeds SEDEMA's territorial
  inventory even after export scaling. Not force-patched further (per project
  ground rules). Absolute excess 0.52 Mt = 2.2% of the total benchmark.
- **IPPU 0.26 vs 0.002:** SISEPUEDE attributes CDMX's 15%-GDP share of national
  HFC/refrigerant product-use (banks); SEDEMA Scope-1 counts only AC-maintenance.
  Scaled down (demscalar 0.01) but a residual remains — documented scope difference.
- **AFOLU −36%:** SEDEMA includes forest fires (0.0175 Mt) that the model's
  land-use configuration does not; livestock/crop sources match.
- **FRST sink** (model −0.11 Mt) excluded from the gross comparison, matching
  SEDEMA's source-only scope.
- Data gaps (non-blocking): CDMX manufacturing SCIAN share, exact CDMX GWh,
  vehicle class split, passenger-km — see `02_downscaling_strategy.md §9`.

## 5. Reproducibility

```bash
bash calibration/run_all.sh --run   # rebuild CDMX inputs + run model + print gate
```
All changes traced in `data_sources.csv` (variable, original MEX, new CDMX, method,
source URL, agent, date). Per-sector research memos in `03_sectors/`.

## 6. Deliverables

- CDMX inputs: `ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv`
- Scripts: `scripts/transform_*.py`, `run_all.sh`, `lib_calib.py`, `diagnose_2022.py`
- Validation: `04_validation/` (convergence_log.csv, comparison chart, per-run outputs)
- `data_sources.csv`, `DECISIONS.md`, `STATUS.md`, research memos, this report.
