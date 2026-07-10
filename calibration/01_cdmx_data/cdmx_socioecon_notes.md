# CDMX Socioeconomic Reference — Downscaling Memo

Purpose: official CDMX socioeconomic drivers and CDMX shares of national totals, used to
downscale national SISEPUEDE model inputs to Ciudad de México. All values from official
sources (INEGI, CONAPO). Every figure has a source URL and year in `cdmx_ref_socioecon.csv`.

## Headline shares to use for downscaling

| Share | Value | Year | Basis |
|---|---|---|---|
| **Population share (Census)** | **7.31%** | 2020 | 9,209,944 / 126,014,024 (INEGI states 7.3%) |
| **Population share (CONAPO proj.)** | 7.28% (2020) → 6.54% (2030) → 5.46% (2050) | 2020–2050 | CONAPO mid-year, declining |
| **GDP share of national** | **15.0%** (2024); 14.8% (2023) | 2024 | INEGI PIBE — CDMX is the largest single-entity contributor |
| **Households share** | **7.83%** | 2020 | 2,756,319 / 35,219,141 viviendas particulares habitadas |
| **Manufacturing share of CDMX GDP** | subset of 9.9% secondary (services 83.5%) | 2023 | manufacturing-only not in press release — see caveat |

Recommendation: use **~7.3% for population** and **~15.0% for GDP** as the primary
downscaling denominators. For anything that scales with dwellings/housing stock, use
**~7.8%**. Note the population and GDP shares diverge strongly (CDMX is ~2x more
economically concentrated than its population share), so choose the driver that matches the
model input (activity/energy-by-value → GDP share; per-capita/residential → population share).

## Population

- **CDMX 2020 (Census enumeration):** 9,209,944 persons (52.2% women, 47.8% men).
  2nd most populous entity after Estado de México; 7.3% of national. Median age 35;
  density 6,163 hab/km². Source: INEGI Censo 2020, boletín 98/21.
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_CdMx.pdf
- **National 2020 (Census):** 126,014,024 persons; 35,219,141 viviendas particulares habitadas.
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_Nal.pdf
- **CONAPO projections (Conciliación 1950-2019 + Proyecciones 2020-2070, pry23):**
  CDMX 9,332,593 (2020) → 9,032,705 (2030) → 8,015,397 (2050). National 128,209,170 →
  138,033,990 → 146,943,948. CDMX population is **declining**; its national share falls from
  ~7.3% to ~5.5% by 2050. Computed by summing all ages/both sexes from the official CSV.
  https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/pry23/00_Pob_Mitad_1950_2070.csv
  - NOTE: CONAPO 2020 mid-year (9.33M) exceeds the Census count (9.21M) because CONAPO is a
    conciliated/projected series, not the raw enumeration. Use Census for a base-year stock,
    CONAPO for the trajectory shape.

## GDP (PIB por Entidad Federativa, PIBE, base 2018)

- **CDMX 2024:** 15.0% of national PIB — the single largest contributor. PIB precios de
  mercado, precios constantes 2018 = 3,886 mmp (miles de millones); national = 25,365 mmp.
  National nominal 2024 = 33,506,847 millones de pesos corrientes.
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/pibent/PIBE2024_CP.pdf
- **CDMX 2023:** nominal PIB = 4,717,467 millones de pesos corrientes; 14.8% of national.
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2024/PIBEF/PIBEF2023_CDMX.pdf

## Value added by sector (CDMX, 2023, valores corrientes, % of total product)

- Primary (primario): **0.0%**
- Secondary (secundario): **9.9%** — includes manufacturing + construction + utilities
- Tertiary / services (terciario): **83.5%**
- Net taxes on products (ISPN): 6.6%

CDMX is overwhelmingly a **services economy**. This matters for IPPU/industry modeling: the
industrial (secondary) footprint is small (<10% of GDP), and **manufacturing is only a portion
of that <10%**.

### Manufacturing caveat (found = no for the exact share)
The INEGI PIBE press releases give the three-way primary/secondary/tertiary split but do **not**
state the manufacturing-only VAB share for CDMX. Manufacturing (SCIAN 31-33) is a subset of the
9.9% secondary sector; the secondary sector also contains construction and utilities, so
manufacturing is strictly < 9.9% of CDMX GDP. Manufacturing VAB fell 1.2% in real terms in 2023.
To obtain the exact manufacturing-only share, pull sector 31-33 from the PIBE tabulados:
https://www.inegi.org.mx/programas/pibent/2018/ (or the interactive tabulados). This was not
resolved from press releases and is marked found=no in the CSV.

## Households / viviendas

- CDMX viviendas particulares habitadas 2020: **2,756,319**; national **35,219,141** → share **7.83%**.
  Avg 3.6 occupants/dwelling nationally.
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_CdMx.pdf

## Data provenance
- INEGI figures pulled from official boletines (PDF, saladeprensa) and the PIBE program.
- CONAPO figures computed directly from the official open-data CSV (pry23 series), not from a
  secondary summary.
