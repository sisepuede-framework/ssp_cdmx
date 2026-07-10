# Diagnostic — Model vs Observed (SEDEMA 2022), running state

Benchmark: SEDEMA 2022 Scope-1 gross = 23.465 Mt CO2e (excl. FRST sink).
Model view: gross = sum of subsector totals excl. frst. Compare at year 2022.

## State after sector 1/7 (socioeconomic only)

| Sector (SISEPUEDE→SEDEMA) | Model Mt | Obs Mt | Dev % | Gap to close | Owner |
|---|---:|---:|---:|---:|---|
| Transport (trns) | 47.73 | 17.802 | +168% | -29.9 | transport-agent |
| Energy stationary (scoe+inen+fgtv+entc) | 143.04 | 5.237 | +2631% | -137.8 | energy-supply + buildings |
| IPPU (ippu) | 144.91 | 0.002 | huge | -144.9 | ippu-agent |
| Waste (waso+trww) | 12.47 | 0.361 | +3356% | -12.1 | waste-agent |
| AFOLU (agrc+lvst+lsmm+soil) | 94.73 | 0.067 | huge | -94.7 | afolu-agent |
| **TOTAL gross** | **442.88** | **23.465** | **+1787%** | **-419.4** | — |

Transport share = 10.8% (target ~76%). FRST sink = +0.05 (excluded from gross).

Structural re-specs pending (approved, D1): entc 52.46→~0 · fgtv 45.11→~0 · ippu 144.91→~0.

Drivers (calibrated, matching obs): pop 9.24M (+0.3% vs Censo), gdp 15% share,
occupancy 3.34, area 149,430 ha.

## Convergence path
715.6 (national) → 442.9 (socio) → [energy-supply] → [transport] → ... → target ~23.5
