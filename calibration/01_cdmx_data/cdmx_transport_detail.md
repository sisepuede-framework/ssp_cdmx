# CDMX / ZMVM Transport — detailed research capture (verified sources)

Source: research subagent, 2026-07-03. Cross-check against `cdmx_ref_energy_transport.csv`.

## Modal split — INEGI EOD 2017 (ZMVM, weekday trips)

Total = 34.56M trips/weekday (17.30M originate in CDMX). Two breakdowns — do NOT mix:

**A) Top-level, mutually exclusive (share of 34.56M):**
| Mode | Trips (M) | % (calc) |
|---|---|---|
| Public transport | 15.57 | 45.1% |
| Private (car/moto) | 7.29 | 21.1% |
| Bicycle | 0.72 | 2.1% |
| Walking only | 11.15 | 32.3% |
| Other | 0.04 | 0.1% |

**B) Within public transport (% of 15.57M PT trips; multimodal → sums >100%):**
Colectivo/micro/combi 74.1% · Metro 28.7% · Taxi 10.5% · Metrobús/Mexibús 7.1% ·
Autobús suburbano 5.8% · RTP/M1 2.6% · Mototaxi 1.8% · Otro 3.5%.

Source: INEGI EOD 2017 Resultados — https://www.gob.mx/cms/uploads/attachment/file/323491/Resultados_EOD.pdf
(program: https://www.inegi.org.mx/programas/eod/2017/). No newer official EOD (prior was 2007).

## Public transport ridership (annual passengers)

**Metro CDMX (STC):** 2025=1,241,582,324 · 2024=1,171,859,113 · 2023=1,115,160,023 ·
2022=1,057,461,875 · 2021=837,473,413 · 2020=935,176,702.
Train-km (not pkm): 2025=40,130,047 km; 2024=37,002,392 km. Passenger-km NOT published.
Source: Metro CDMX Cifras de Operación — https://www.metro.cdmx.gob.mx/operacion/cifras-de-operacion

**Metrobús CDMX:** 2024=529,699,509 · 2025=509,855,934 · 2023=501,682,763 · 2022=438,131,175.
(Summed from official daily open-data CSV; news estimates ~430M are low.)
Source: Datos Abiertos CDMX — https://datos.cdmx.gob.mx/dataset/afluencia-diaria-de-metrobus-cdmx

## Caveats for calibration
- Modal split is ZMVM-wide 2017 (incl. Edo. Méx.), ~7-yr gap vs 2024/25 ridership.
- Metrobús in modal split lumps Mexibús; ridership figure is Metrobús CDMX alone.
- Passenger-km not available for either system (found=no) — will need estimation
  from line lengths × ridership if SISEPUEDE requires pkm.
