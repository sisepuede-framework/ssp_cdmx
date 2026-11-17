# CDMX GHG Emissions — Reference Benchmark Memo (SISEPUEDE calibration)

_Prepared 2026-07-03. Primary validation benchmark for the SISEPUEDE CDMX calibration._

## 1. Chosen benchmark: Inventory YEAR 2022 (published 2026)

**Document:** *Inventario de Emisiones de la Ciudad de México y su Zona Conurbada 2022 — Contaminantes criterio, tóxicos, gases y compuestos de efecto invernadero.* SEDEMA (Secretaría del Medio Ambiente de la Ciudad de México).

- **Inventory year (emissions correspond to):** 2022
- **Publication year:** 2026 (PDF metadata CreationDate D:20260129 — created Jan 2026)
- **Frequency:** biennial
- **Raw PDF (primary source):** http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf (176 pp, ~14 MB, downloaded & parsed)
- **SEDEMA cambio-climático portal:** http://www.data.sedema.cdmx.gob.mx/cambioclimaticocdmx/emisiones_cdmx.html (note: expired TLS cert; reachable over http)

**Why this benchmark:** It is the most recent official SEDEMA GHG inventory, it reports a **CDMX-only** total (the 16 alcaldías) distinct from the wider ZMVM/metro figure, and it gives a full category-level breakdown (Annex 3, Table 27) that can be mapped to SISEPUEDE sectors. Prefer it over 2020 (COVID-depressed activity) and 2018.

### Headline number
> "Para el año 2022, se estimó que en la CDMX se emitieron **23.5 millones de toneladas de CO2 equivalente (CO2e)** y mil 223 toneladas de carbono negro (CN)." (p.29)

Exact total (Table 3, p.30; Table 27, p.135): **23,465,427 t CO2e = 23.465 Mt CO2e** (CDMX only). Of this, 22,050,176 t is local jurisdiction and 1,415,250 t federal jurisdiction. GWP basis: IPCC potencial de calentamiento global (AR values).

## 2. ELECTRICITY SCOPE — CRITICAL FINDING: SCOPE 1 / TERRITORIAL ONLY

This inventory is a **territorial (scope 1) production-based** inventory. It does **NOT** include the emissions from the electricity CDMX imports and consumes — only the (small) generation that physically occurs inside the city. Two explicit quotes:

> **(p.15, energy-balance notes):** "El consumo de energía eléctrica es el total que demanda la CDMX, **sólo se estiman las emisiones por la generación de electricidad dentro de la ciudad.**"

> **(p.37, Tabla 4 notes, CDMXyZC):** "Se reporta el consumo de electricidad que demanda la CDMXyZC, **pero las emisiones que se generan por producir esta energía se dan fuera de la metrópoli y no se reportan en este documento.**"

Consequence for calibration:
- In-city electricity generation appears as a point-source category "Generación, transmisión y distribución de energía eléctrica" = **105,948.64 t CO2e** (0.106 Mt) — trivially small, because CDMX generates almost no power itself.
- Electricity is ~20% of the city's final energy consumption (204.21 PJ of 1,007 PJ, Tabla 4 p.37) but its upstream generation emissions (scope 2) are OUTSIDE this total.
- **If SISEPUEDE produces a consumption-based / scope-2 electricity figure, it will be substantially HIGHER than this 23.5 Mt benchmark and the two are not directly comparable.** Either (a) compare SISEPUEDE scope-1 output to this number, or (b) add an imported-electricity term to the benchmark using a CDMX consumption of electricity × Sistema Eléctrico Nacional grid emission factor before comparing to a scope-2 model output.

## 3. SEDEMA → SISEPUEDE sector mapping

SEDEMA does **not** classify by IPCC sectors (Energy / IPPU / Waste / AFOLU). It classifies by **source type**: Fuentes puntuales, Fuentes de área, Fuentes móviles, Fuentes naturales — each split into ~50 categories (Table 27, pp.134–135). The mapping below is a reconstruction from those categories; it reconciles to the official total within 3,738 t (0.016%, rounding).

| SISEPUEDE sector | Mt CO2e (2022) | Built from SEDEMA categories (Table 27) |
|---|---:|---|
| **Energy** (stationary combustion: buildings + industry + in-city power) | **5.237** | Área "Combustión" block 4.100 (habitacional 1.440, industria no regulada 2.432, comercial-institucional 0.222, equipos agrícolas 0.006) + point-source industrial combustion/process 0.729 + in-city electricity generation 0.106 + emisiones domésticas 0.277 + asados al carbón 0.026 |
| **Transport** (on-road + off-road) | **17.802** | Fuentes móviles (on-road) 16.989 + Móviles no carreteros 0.813 (aircraft 0.418, machinery 0.370, bus terminals, locomotives) |
| &nbsp;&nbsp;— on-road only | 16.989 | Fuentes móviles subtotal (72.4% of city total) |
| **IPPU** (industrial processes) | **~0.002** → **0.102** (corrected 2026-11-16) | No industrial-process bucket — industrial emissions are counted as combustion (already in Energy). **Correction:** HFCs are not only "mantenimiento de aires acondicionados habitacionales" (1.01 t HFC = 0.0018 Mt). Tabla 27 also reports **77.3 t HFC in Fuentes móviles** (vehicle A/C: autos 52.61, SUV 22.04, taxis 2.15, …) ≈ **0.1005 Mt CO2e** (GWP 1,300), which sits inside the 16.989 on-road total. SISEPUEDE models mobile A/C in IPPU (product_use_ods_refrigeration, IPCC 2.F.1), so for calibration IPPU = all HFC ≈ 0.102 Mt and Transport = 17.802 − 0.1005 = 17.701 Mt. GWP basis (back-solved from the table): AR5, CH4 28, N2O 265. |
| **Waste** (solid + wastewater) | **0.361** | "Desechos urbanos" group 0.357 (aguas residuales no tratadas 0.243, tratamiento aguas residuales 0.066, rellenos sanitarios 0.022, residuos sólidos no gestionados 0.016, tratamiento biológico 0.006) + quema a cielo abierto 0.004. Small in CO2e but = 66% of the city's CH4. |
| **AFOLU** (agriculture + livestock + fires; NO LULUCF sink) | **0.067** | Agricultura 0.007 (fertilizantes) + Ganadería 0.042 (fermentación entérica 0.041) + incendios forestales 0.018 + quemas controladas 0.001 |
| **Total** | **23.465** | Official 23,465,427 t CO2e |

Mapping caveats:
- **Off-road mobile (0.813 Mt)** — placed under Transport here; some frameworks put aviation/machinery under Energy "other". Adjust as SISEPUEDE requires; `ghg_transport_onroad` (16.989 Mt) is provided for the strict on-road comparison.
- **IPPU process emissions are absent.** SEDEMA reports industrial point sources as fuel combustion, so process CO2 (e.g. cement, chemicals) is folded into Energy. The GHG table only has CO2, CH4, N2O and HFC columns: no SF6/PFC, no N2O from product use (anesthesia, aerosols), no cement/clinker inside CDMX. The only IPPU-type benchmark is HFC (vehicle + residential A/C, ≈0.102 Mt; verified against the PDF on 2026-11-16).
- **LULUCF / land-use sinks are EXCLUDED.** The inventory note states categories excluded include "vegetación"; there is no forest-CO2-removal (negative) term. AFOLU here is source-only.

## 4. Alternative / prior inventory years (same scope-1 SEDEMA series)

| Inventory year | CDMX total (Mt CO2e) | Exact (t) | Source | Verified this pass |
|---|---:|---:|---|---|
| **2022** (chosen) | **23.465** | 23,465,427 | Inv. CDMXyZC 2022, Table 3 p.30 / Table 27 p.135 | Yes — PDF parsed |
| 2020 | 19.888 | 19,888,435 | Inv. ZMVM 2020, Table 9 p.95 (`...inventario-emisiones-cdmx-2020bis.pdf`) | Yes — PDF parsed |
| 2018 | 22.480 | 22,480,079.3 | Inv. ZMVM 2018 (SEDEMA cambio-climático portal) | Value from SEDEMA summary; not page-verified |

Trend note: 2020 dips (~COVID mobility drop, transport is 70%+ of the total); 2022 rebounds above 2018. 2022 is both the most recent and the most representative of normal-activity conditions.

## 5. Criteria-pollutant inventory (secondary)

There is **no separate** criteria-pollutant document — SEDEMA publishes criteria pollutants, toxics, and GHG together in the **same** 2022 report. Same file, same year. City-wide 2022: ~10,000 t PM10 (p. text), plus PM2.5, SO2, CO, NOx, COV, NH3 and toxics tables (Tablas 1, 8, etc.). If a standalone criteria benchmark is needed, extract from this same PDF (Tabla 1 onward, pp. ~24–29).

## 6. Other SEDEMA inventory (flag — different scope, do NOT mix)

SEDEMA also maintains a **GPC (Global Protocol for Community-Scale GHG Emission Inventories)** inventory for city-to-city comparison. GPC is **consumption/scope-2-inclusive** (it DOES count imported-electricity emissions), so its total will differ from and exceed the 23.465 Mt territorial figure. Referenced on the SEDEMA cambio-climático portal. If SISEPUEDE output is scope-2, the GPC inventory may be the more apples-to-apples benchmark — worth pulling separately.

## 7. Raw file download links (all fetched over http; some sites have expired TLS certs)

- 2022 inventory PDF: http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf
- 2020 inventory PDF: https://proyectos.sedema.cdmx.gob.mx/datos/storage/app/media/docpub/sedema/inventario-emisiones-cdmx-2020bis.pdf
- 2018 inventory PDF (flipbook memoria): http://www.aire.cdmx.gob.mx/descargas/publicaciones/flippingbook/memoria-inventario-emisiones-2018/memoria_inventario_emisiones_2018.pdf
- Inventarios ZMVM index: http://www.aire.cdmx.gob.mx/default.php?opc=Z6BhnmI%3D&dc=Zg%3D%3D
- SEDEMA "Las emisiones de la Ciudad de México": http://www.data.sedema.cdmx.gob.mx/cambioclimaticocdmx/emisiones_cdmx.html
