# CDMX Fuel & Vehicle Fleet — best-sourced figures (use these over weaker duplicates)

Captured 2026-07-03. These come from agents that computed sums directly from official
CNE/INEGI CSVs — prefer over any secondary-reported numbers in cdmx_ref_energy_transport.csv.

## Fuel sales — CNE "Petrolíferos", year 2024 (most recent complete year)

| Fuel | CDMX | National | CDMX share | unit |
|---|---:|---:|---:|---|
| Gasolina (Regular+Premium) | 2,713,228,013 L (≈2.713 Mm³, ~46.6 mbd) | 44,131,210,499 L | 6.15% | L/yr |
| Diésel (retail expendio) | 291,573,054 L (≈0.292 Mm³, ~5.0 mbd) | 13,081,600,000 L | 2.23% | L/yr |
| Gas LP – cilindro | 106,060,876 kg | 1,208,659,400 kg | 8.78% | kg/yr |
| Gas LP – expendio (autogas) | 43,608,985 kg | 1,063,469,433 kg | 4.10% | kg/yr |

Caveats: gasolina/diésel are RETAIL "expendio al público" (excludes bulk diesel sold
directly to fleets/industry → CDMX diesel understated). CDMX gas LP is dominated by
**autotanque** (~32.9k ton/mo Jan-2026) which has no consolidated annual-by-state series;
cilindro (106k ton/yr) is only the cylinder portion, so true CDMX LP is materially larger.
Gas natural by state: not on datos.gob.mx as clean CSV → CENAGAS Boletín SNG.

Source: CNE/CRE Petrolíferos — https://www.datos.gob.mx/dataset/volumenes_venta_expendio_publico_petroliferos
Raw CSV: https://repodatos.atdt.gob.mx/api_update/cne/volumenes_venta_expendio_publico_petroliferos/04_volumenes_venta_expendio_petroliferos.csv

## CDMX energy mix (SEDEMA infograma, base year 2016, total 385.2 PJ)
gasolina 42.33% · diésel 12.70% · gas natural 7.41% · gas LP 10.42% · electricidad 23.78%.
Source: http://www.aire.cdmx.gob.mx/descargas/publicaciones/simat-infograma-consumo-energetico.pdf

## Vehicle fleet — INEGI VMRC 2024 (definitive)

| Item | Value | Year |
|---|---:|---|
| CDMX total fleet | 6,509,434 (10.62% of national) | 2024 |
| National total fleet | 61,262,766 | 2024 |
| CDMX motocicletas | 716,400 | 2024 |

National by-type (Dec 2024, excl. motos & oficial): Automóviles 39,567,588 (particulares
38,880,238) · Camiones pasajeros 503,183 (públicos 213,822) · Camiones/camionetas carga
12,049,713. CDMX full 3-way class split only in INEGI legacy OLAP cube (not machine-
renderable) — pull manually from VMRC 2024 microdata: https://www.inegi.org.mx/rnm/index.php/catalog/1124
Note: for CDMX, public-service cargo trucks are counted under "particular".
Source: INEGI VMRC — https://www.inegi.org.mx/temas/vehiculos/

## Electricity (consolidated)
CDMX consumption ~11,877 GWh (2022), ~3.4–3.6% of national. In-city generation ~417 MW
capacity, ~99.9% imported. Grid EF: 0.435 (2022) / 0.438 (2023) / 0.444 (2024) tCO2e/MWh
[CRE Aviso FE-SEN]. Under D1 (Scope 1) only in-city generation counts for CDMX emissions.
