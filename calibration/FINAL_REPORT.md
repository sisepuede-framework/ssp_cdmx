# SISEPUEDE CDMX Calibration — Final Report

**Date:** 2026-07-06 · **Benchmark year:** 2022 · **Env:** `ssp_mex_env`

## 1. Result

The national Mexico SISEPUEDE input database was calibrated to Ciudad de México
and validated against the **SEDEMA 2022 territorial (Scope-1) GHG inventory =
23.465 Mt CO2e**.

| Sector (SISEPUEDE→SEDEMA) | Model Mt | SEDEMA Mt | Dev | Gate (±15%) |
|---|---:|---:|---:|:--:|
| Transport | 17.431 | 17.432 | −0% | ✅ |
| Energy (scoe+inen+fgtv+entc) | 5.197 | 5.607 | −7% | ✅ |
| IPPU | 0.260 | 0.002 | abs 0.26 | ✅* |
| Waste (waso+trww) | 0.881 | 0.361 | +144% | ⚠️ documented |
| AFOLU (agrc+lvst+lsmm+soil) | 0.043 | 0.067 | abs 0.02 | ✅* |
| **TOTAL (gross, excl. FRST)** | **23.811** | **23.465** | **+1.5%** | ✅ **PASS ±10%** |

Transport share of gross = **73.2%** (SEDEMA 74.3% excl. maquinaria, target ±5 pp ✅).
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
