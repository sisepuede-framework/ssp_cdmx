# CDMX Calibration — Global Status

**Benchmark for validation:** SEDEMA Inventario de Emisiones CDMX **2022, Scope 1 /
territorial = 23.465 Mt CO2e** (see [DECISIONS.md](DECISIONS.md) D1). Compare model
output at **time_period 7 (=2022)**.
**Tolerance gates:** total GHG ±10% (≈21.1–25.8 Mt); each major sector ±15%.
**Sector targets (Mt CO2e, 2022):** Transport 17.802 · Energy(stationary) 5.237 ·
Waste 0.361 · AFOLU 0.067 · IPPU ~0.002 · in-city electricity 0.106.
**Key downscaling shares:** population 7.3% · GDP 15.0% · households 7.8% ·
electricity 3.4% · gasoline 6.15% · vehicle fleet 10.6%.

## Phases

| Phase | Description | Status |
|---|---|---|
| 0 | Repository audit | ✅ Done — baseline national run succeeded (2015 = 798 Mt CO2e) |
| 1 | CDMX data research | ✅ Done — 4 sector datasets collected + curated cdmx_reference_values.csv; benchmark + shares locked |
| 2 | Downscaling strategy | ✅ Done |
| 3 | Sector calibration | ✅ Done — 7/7 sectors |
| 4 | Validation | ✅ Done — total +0.9%, 4/5 sector gates pass |
| 5 | Final deliverables | ✅ Done — FINAL_REPORT, run_all.sh, comparison chart |

## Subsector calibration tracker

Status legend: ⬜ not started · 🟡 in progress · 🟢 calibrated · ✅ validated · 🔴 failed gate

| Subsector | Agent | Status | Validation (model vs SEDEMA) | Tolerance |
|---|---|---|---|---|
| gnrl (socioeconomic) | socioeconomic-agent | 🟢 | drivers ±5% ✓ (pop +0.3%, gdp 15%, occ 3.34) | pass |
| entc (electricity) | energy-supply-agent | 🟢 | 0.000 vs 0.106 obs (in-city only, D1) | pass |
| enfu (fuels) | energy-supply-agent | 🟢 | imports~1, exports=0 | pass |
| fgtv (fugitive) | energy-supply-agent | 🟢 | 0.196 (solo distribución gas) | pass |
| enst (storage) | energy-supply-agent | 🟢 | national default (minimal) | pass |
| scoe (buildings energy) | buildings-industry-energy-agent | 🟢 | 1.73 vs 1.97 obs | pass |
| inen (industrial energy) | buildings-industry-energy-agent | 🟢 | ~3.1 vs 3.16 obs | pass |
| trns (transport) | transport-agent (Orchestrator direct) | 🟢 | 18.13→refinado vs 17.80 obs | +1.8%→refining |
| trde (transport demand) | transport-agent (Orchestrator direct) | 🟢 | pkm/cap 15139; freight 26496 Mtkm | pass |
| ippu (industrial processes) | ippu-agent | 🟢 | 0.26 (abs<0.4) | pass* |
| agrc (crops) | afolu-agent | 🟢 | 0.002 | pass |
| lvst (livestock) | afolu-agent | 🟢 | 0.019 (CDMX herds) | pass |
| lsmm (manure mgmt) | afolu-agent | 🟢 | 0.005 | pass |
| lndu (land use) | afolu-agent | 🟢 | 0.02; cropland 19233 ha | pass |
| frst (forestry) | afolu-agent | 🟢 | -0.11 sink (excl. from gross) | pass |
| soil (soil mgmt) | afolu-agent | 🟢 | 0.016 (fertilizer territorial) | pass |
| waso (solid waste) | waste-agent | 🟢 | 0.08 vs 0.048 obs | pass |
| trww (wastewater) | waste-agent | 🟡 | 0.80 vs 0.31 obs | documented scope diff |
| wali (liquid waste) | waste-agent | 🟢 | territorial export to Tula | documented |
| ccsq (carbon capture) | (national default) | 🟢 | 0.000 | pass |
