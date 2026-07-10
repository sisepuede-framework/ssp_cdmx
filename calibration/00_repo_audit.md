# Phase 0 — Repository Audit (SISEPUEDE CDMX Calibration)

**Author:** Orchestrator agent
**Date:** 2026-07-03
**Repo:** `ssp_cdmx` (fork of SISEPUEDE Mexico national repo)

---

## 1. Repository structure

The fork has no commits yet — all files are untracked. The README header still
says "Egypt" (leftover template text), but the actual data is **Mexico national**.

```
ssp_cdmx/
├── environment.yml            # conda env spec (see §4 — BROKEN, wrong env)
├── README.md                  # generic SISEPUEDE run instructions (says "Egypt")
├── .gitignore, LICENSE
└── ssp_modeling/
    ├── config_files/config.yaml          # run config (country_name, input file, flags)
    ├── input_data/
    │   └── sisepuede_adj_inputs_MEX.csv   # THE national input DB (see §2)
    ├── notebooks/
    │   └── mexico_manager_strategy_3Path.ipynb  # entry point, 95 code cells
    ├── transformations/       # per-strategy transformation YAMLs + strategy_definitions.csv
    ├── scenario_mapping/       # Excel crosswalks (strategy → transformation intensities)
    ├── output_postprocessing/  # R scripts to rescale results for Tableau
    ├── ssp_run_output/         # run outputs land here
    └── tableau/                # dashboard + data
```

## 2. The input database (calibration surface)

**Everything to be calibrated lives in ONE file:**
`ssp_modeling/input_data/sisepuede_adj_inputs_MEX.csv`

| Property | Value |
|---|---|
| Shape | 56 rows × 2421 columns |
| Rows | one per **year, 2015–2070** (`time_period` 0–55) |
| ID columns | `year`, `time_period`, `region` |
| `region` value | `mexico` (single region) |
| Data columns | **2418 SISEPUEDE variables** |
| Run truncation | notebook keeps `time_period` 0–45 → **2015–2060** |

Variable naming follows SISEPUEDE's field convention
`<type>_<subsector>_<detail>`, e.g. `ef_ippu_tonne_sf6_per_tonne_production_metals`,
`nemomod_entc_capital_cost_pp_solar_mm_usd_per_gw`, `pop_gnrl_...`.

### Variables per subsector (the sector-agent workload)

| Subsector | # vars | Maps to sector agent |
|---|---:|---|
| entc (electricity generation, NemoMod) | 338 | energy-supply-agent |
| lndu (land use) | 333 | afolu-agent |
| inen (industrial energy) | 315 | buildings-industry-energy-agent |
| lvst (livestock) | 191 | afolu-agent |
| agrc (crops) | 187 | afolu-agent |
| ippu (industrial processes) | 185 | ippu-agent |
| trns (transport demand) | 174 | transport-agent |
| enfu (energy fuels) | 157 | energy-supply-agent |
| waso (solid waste) | 118 | waste-agent |
| scoe (stationary/buildings energy) | 72 | buildings-industry-energy-agent |
| lsmm (livestock manure mgmt) | 58 | afolu-agent |
| trww (wastewater treatment) | 54 | waste-agent |
| wali (liquid waste / water) | 46 | waste-agent |
| soil (soil management) | 40 | afolu-agent |
| fgtv (fugitive emissions) | 38 | energy-supply-agent |
| frst (forestry) | 32 | afolu-agent |
| enst (energy storage) | 28 | energy-supply-agent |
| trde (transport demand/distribution) | 9 | transport-agent |
| gnrl (general/socioeconomic) | 9 | socioeconomic-agent |
| ccsq (carbon capture) | 9 | (national default) |

(Remaining tokens: `protein`, `gravimetric`, etc. are detail tokens within the
above subsectors.) Variable **prefixes** (types): `frac` (840), `ef` (468),
`nemomod` (333), `pij` (121), `elasticity` (62), `efficfactor` (61), plus
`qty`, `fuelefficiency`, `exports`, `physparam`, `cost`, `area`, `pop`, etc.

## 3. How the model runs (entry point)

Entry point: `notebooks/mexico_manager_strategy_3Path.ipynb`. Core pipeline:

1. **Build inputs** (cells 6–15): read CSV → fill gaps from
   `SISEPUEDEExamples("input_data_frame")` → `add_missing_cols` →
   set `region = country_name` (from config) → truncate `time_period` to 0–45.
2. **Manual one-off edits** (cells 21–25): ENTC capital costs overwritten
   directly on the dataframe. ⚠️ Violates ground rule #4 (no manual edits) —
   for CDMX these must become scripted transformations.
3. **Transformers + strategies** (cells 48–78): instantiate `trf.Transformers`,
   generate transformation YAMLs from the Excel crosswalk
   (`ssp_transformation_cw`), define strategies, build templates.
4. **Run** (cells 79–81):
   ```python
   ssp = si.SISEPUEDE("calibrated", db_type="csv", regions=[country_name],
                      strategies=strategies, attribute_time_period=...)
   ssp.project_scenarios({ssp.key_design:[0], ssp.key_future:[0],
                          ssp.key_strategy: strategies_to_run},
                         save_inputs=True, include_electricity_in_energy=True)
   ```
   **Baseline = strategy_id `0` (primary_id 0).** A baseline national run only
   needs `strategies_to_run = [0]` — no transformation machinery required.
5. **Read output** (cells 84–92): `df_out = ssp.read_output(None)`; emission
   fields via `matt.get_all_subsector_emission_total_fields()`; export
   `WIDE_INPUTS_OUTPUTS.csv` to `ssp_run_output/`.

**Region ID:** the model keys off `region`/`country_name = "mexico"`. This drives
region-level attribute lookups (grid factors, areas). Representing CDMX as a
subnational region is the key **Phase 2 structural decision** (imported
electricity, see plan).

## 4. Runtime environment ⚠️

- conda is installed at `~/miniconda3` (shell function; not auto-on-PATH in
  non-interactive shells — invoke env python by absolute path).
- **`environment.yml` is misleading**: it names env `ssp_mexico_jan_21_01_26`,
  but that env is **incomplete — `sisepuede` and `ssp_transformations_handler`
  are NOT installed there**.
- **Working environment: `ssp_mex_env`** →
  `/Users/fabianfuentes/miniconda3/envs/ssp_mex_env/bin/python`.
  Verified: all notebook imports succeed (`sisepuede`,
  `ssp_transformations_handler`, `costs_benefits_ssp`, `polars`).
- **Energy model backend:** `energy_model_flag: true` → ENTC uses **NemoMod
  (Julia)**. `juliacall` is installed and manages Julia via
  `~/.julia/environments/pyjuliapkg`. First energy run pays a multi-minute
  Julia precompile cost. A non-energy run is possible with
  `initialize_as_dummy=True` / `energy_model_flag=false`.

## 5. Config (`config_files/config.yaml`)

```yaml
country_name: "mexico"
ssp_input_file_name: "sisepuede_adj_inputs_MEX.csv"
ssp_transformation_cw: "ssp_mexico_transformation_strategy_pemex_vf.xlsx"
set_lndu_reallocation_factor_to_zero: true
energy_model_flag: true
```

For CDMX we will add a `config_files/config_cdmx.yaml` (or switch these) pointing
to `sisepuede_adj_inputs_CDMX.csv` and `country_name` handling per the Phase 2
regionalization decision.

## 6. Phase 0 gate status

| Check | Status |
|---|---|
| Repo structure mapped | ✅ |
| Input DB schema / units / time range identified | ✅ (2015–2070, run 2015–2060) |
| Subsectors + input files identified | ✅ (single CSV, 20 subsectors) |
| Run entry point + region ID understood | ✅ |
| Working env identified | ✅ `ssp_mex_env` (not the one in environment.yml) |
| **Baseline national run executed end-to-end** | ✅ **DONE** — see below |

**Baseline run succeeded** via `calibration/scripts/run_baseline.py` (env
`ssp_mex_env`, full energy model, NemoMod/HiGHS). Runtime ~2 min after Julia
precompile. Outputs in `calibration/reference_mexico/`:
`baseline_mex_wide.csv`, `baseline_mex_emissions_by_subsector.csv`, `baseline_run.log`.

**National base-year (2015) emissions = 798.36 Mt CO2e** (plausible for Mexico).
Subsector split (Mt CO2e): entc 204.8 · ippu 167.8 · trns 132.2 · fgtv 76.3 ·
waso 72.9 · inen 72.9 · lvst 61.3 · lndu 56.9 · scoe 33.2 · soil 31.4 · trww 23.9 ·
lsmm 9.6 · agrc 2.1 · ccsq 0.0 · **frst −146.9 (sink)**.

Note: the NemoMod precompile prints a non-fatal `ConfParser`/`NemoMod` method-
overwrite ERROR line; the optimization still runs to completion (all years
solved by HiGHS). Not a blocker.

## 7. Open items / flags for the user

1. **Fix `environment.yml`** to reflect the real working env (`ssp_mex_env`), or
   rebuild that env from a corrected spec. Currently the documented env is broken.
2. **Manual CSV/YAML edits in the notebook** (cells 21–25, 57–59) must be
   converted to reproducible scripts under `calibration/scripts/` for CDMX.
3. **Region representation decision** (Phase 2): how CDMX is modeled as a
   subnational region — especially imported electricity (grid emission factor vs.
   in-city generation). Needs the Louisiana/subnational precedent check.
4. **Baseline run**: confirm whether to launch the full energy baseline now
   (long) — required to close the Phase 0 gate.
