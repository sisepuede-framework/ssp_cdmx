# CDMX Reference Data — Energy & Transport (SISEPUEDE Calibration)

Compiled 2026-07-03. Official sources only (SENER/SIE, CFE, CRE, SEMARNAT, INEGI, SEMOVI, Metro, Metrobús). Every value carries a source URL and year. Figures marked *partial/estimate* need refinement from the underlying tabulados/CSV before final calibration use.

---

## ENERGY

### 1. Electricity consumption — CDMX
- **~11,877 GWh/year (2022)** net electricity consumption in CDMX.
- CDMX ranks ~5th–6th among the 32 entities. Leaders (2022, GWh): Nuevo León 18,749 · Estado de México 16,914 · Jalisco 13,633 · Chihuahua 13,053 · Baja California 12,380 · **CDMX 11,877**.
- **National total: 333,663 GWh (2022)**, +3.4% vs 2021 → **CDMX share ≈ 3.6%**.
- Source: CONACYT PLANEAS / SENER SIE, reported via https://www.reguladores.com.mx/blog/consumo-de-energia-electrica/
  (Note: the blog mislabels state-level units as "MWh" — the values are GWh, consistent with the national total.) Cross-check the exact figure at CONACYT PLANEAS interactive map (JS-rendered): https://energia.conacyt.mx/planeas/electricidad/consumo
- (An older CDMX-government figure of "~160,000 GWh for all activities incl. 60% transport" appears in a Global Energy piece but conflates all energy end-uses and looks unit-inflated; the 11,877 GWh electricity figure is the reliable one.)

### 2. Grid emission factor — Sistema Eléctrico Nacional (governs CDMX consumed electricity)
- **2023: 0.438 tCO2e/MWh** — CRE Aviso FE-SEN 2023: https://www.gob.mx/cms/uploads/attachment/file/895937/Aviso_FE-SEN23.pdf
- **2024: 0.444 tCO2e/MWh** (most recent) — CRE Aviso FESEN 2024: https://www.gob.mx/cms/uploads/attachment/file/980977/AvisoFESEN_2024.pdf
- 2022 was 0.435. Published annually by CRE for the Registro Nacional de Emisiones (RENE). Because CDMX imports nearly all its electricity from the SEN, this national factor is the correct one for CDMX's consumed-electricity emissions.

### 3. Fuel sales/consumption — CDMX by fuel  *(partial — entity split not extracted)*
- CDMX-level volumes for gasolinas / diésel / gas LP by entity live in SENER SIE datasets that render as CSV/JS and were not machine-readable via search. Download directly:
  - Petrolíferos by entity: https://www.datos.gob.mx/busca/dataset/volumen-de-ventas-por-tipo-de-petroliferos-y-por-entidad-federativa
  - Petrolíferos + gas licuado (internal sales): https://www.datos.gob.mx/dataset/volumen_ventas_internas_productos_petroliferos_gas_licuado
  - SENER hydrocarbons statistics (natural gas): https://estadisticashidrocarburos.energia.gob.mx/
- National context (2023): Pemex gasoline sales ~620–641 thousand bpd; national gasoline demand ~739 thousand bpd; diesel demand rising >5%.
- **Action for calibration:** pull the CDMX rows from the entity-level petrolíferos CSV to get gasolinas/diésel/gas LP volumes.

### 4. Electricity generation inside CDMX — NOT significant
- Installed large-scale (>500 kW) generation within CDMX limits: **417.4 MW** (~2020).
- Technology mix: gas turbine 77% (natural gas) · internal combustion 18.3% (diesel/gas) · steam turbine 4.5%.
- Ownership: ~75% CFE, 12% private self-supply, 7% permit-based, plus continuous-use/cogeneration.
- Source: PAN CDMX report citing CFE/CRE permits — https://bibliotecapancdmx.org.mx/wp-content/uploads/2021/11/15-Situacion-de-la-generacion-y-consumo-de-la-energia-electrica-en-la-Ciudad-de-Mexico180.pdf
- **Conclusion: CDMX is overwhelmingly a net electricity importer.** In-city generation (~0.4 GW) is minor relative to ~11,877 GWh/yr consumption. Treat consumed electricity via the national grid factor.

---

## TRANSPORT

### 5. Vehicle fleet — CDMX (INEGI VMRC 2023)
Source: INEGI Vehículos de Motor Registrados en Circulación — https://www.inegi.org.mx/programas/vehiculosmotor/ (annual catalog: https://www.inegi.org.mx/rnm/index.php/catalog/1019)

| Type | CDMX 2023 | National 2023 | CDMX share |
|---|---|---|---|
| **Total** | **6,471,738** | 58,199,293 | 11.12% |
| Automóviles | ~5,600,000 *(approx)* | — | — |
| Camiones para pasajeros | ~32,740 | 1,340,798 | 2.4% |
| Camiones/camionetas de carga | *(in tabulado)* | 12,225,685 | — |
| Motocicletas | 716,400 | 7,784,486 | 9.2% |

CDMX has the 2nd-largest fleet after Estado de México. *Automóviles and carga are approximate/national-only from search — pull exact CDMX class split from INEGI VMRC tabulados by entity.*

### 6. Modal split (reparto modal) — CDMX, EOD 2017
Source: SEMOVI PIM 2019-2024 (based on INEGI EOD 2017 ZMVM) — https://www.semovi.cdmx.gob.mx/storage/app/media/PIM-2019-2024_.pdf
- **Transporte público ~45.6%**
- **Caminando (walking) ~33.5%**
- **Automóvil particular ~20.9%** (bicycle + other in remainder)
- Sustainable modes (public transport + walking + bicycle) = **77% of CDMX trips** (80% for metro-area commutes).
- ZMVM-wide reference (INEGI EOD 2017 boletín, https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2018/EstSociodemo/OrgenDest2018_02.pdf): **34.56 million trips/typical weekday**, of which 15.57M public transport and 6.60M automobile.

### 7. Metro & Metrobús ridership (2023)
- **Metro CDMX: ~1,057 million passengers/year (2023)** — STC Metro Cifras de Operación (via INEGI): https://www.metro.cdmx.gob.mx/operacion/cifras-de-operacion (rose to ~1,241 million in 2025). 12 lines, ~226 km. Passenger-km not published.
- **Metrobús: ~427 million passengers/year (2023, estimated)** from ~35.6–35.7 million/month reported Dec 2023 — SEMOVI/Metrobús Datos Abiertos: https://datos.cdmx.gob.mx/dataset/afluencia-diaria-de-metrobus-cdmx (daily series available to compute the exact annual total). 7 BRT lines.

---

## HEADLINE NUMBERS (for quick reference)
- Electricity consumption CDMX: **11,877 GWh (2022)**, ~3.6% of national 333,663 GWh.
- Grid emission factor SEN: **0.438 tCO2e/MWh (2023)**, **0.444 (2024)**.
- In-city generation: **417 MW** only — CDMX is a net importer.
- Vehicle fleet CDMX: **6,471,738 (2023)**, 11.12% of national; motos 716,400.
- Modal split CDMX (EOD 2017): public transport **45.6%**, walking **33.5%**, car **20.9%**.
- Metro **~1,057M** pax/yr; Metrobús **~427M** pax/yr (2023).

## OPEN ITEMS (refine before final calibration)
1. CDMX fuel volumes (gasolinas/diésel/gas LP) — download entity CSV from SENER petrolíferos dataset.
2. CDMX vehicle class split (automóviles, carga) — download INEGI VMRC 2023 tabulados by entity.
3. Exact CDMX electricity GWh — confirm at CONACYT PLANEAS / SENER SIE ventas por entidad.
4. Metrobús exact 2023 annual total — sum the daily open-data series.
