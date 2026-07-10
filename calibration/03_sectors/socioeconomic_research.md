# Socioeconomic (`gnrl`) Sector — Calibration Research Memo

**Agent:** socioeconomic-agent · **Phase 3, sector 1 of 7** · **Date:** 2026-07-03
**Governing scope:** [DECISIONS.md](../DECISIONS.md) D1 (Scope-1 territorial, benchmark year 2022).
**Priority: HIGHEST** — every other sector downscales from these drivers.

This memo records the official sources for the six `gnrl` driver columns, the CDMX
trajectory built for each, and the exact method. All URLs were retrieved **2026-07-03**.

---

## 0. Columns calibrated (real column names in the input CSV)

| Column | National 2022 (baseline CSV) | CDMX 2022 (set) | Method |
|---|---|---|---|
| `population_gnrl_urban` | 104,452,121.6 | 9,219,169 | direct (CONAPO total × urban share 99.8%) |
| `population_gnrl_rural` | 23,982,180.05 | 18,475 | direct (CONAPO total × rural share 0.2%) |
| `gdp_mmm_usd` | 2,582.57 (bn USD) | 387.39 (bn USD) | share (national × 15.0%) |
| `occrateinit_gnrl_occupancy` | 3.9817 (pers/dwelling) | 3.341 | direct (Censo 2020: 9,209,944 / 2,756,319) |
| `area_gnrl_country_ha` | 196,437,500 ha | 149,430 ha | direct (INEGI 1,494.3 km²) |
| `elasticity_gnrl_rate_occupancy_to_gdppc` | -0.1 | **-0.1 (KEEP NATIONAL)** | national default, documented |

The model CSV has **56 rows spanning 2015–2070** (not 2015–2060). A full CDMX series was
built for every row from the CONAPO 2015–2070 trajectory; no extrapolation was required
because CONAPO pry23 publishes CDMX through 2070.

---

## 1. Population trajectory 2015–2070 (CONAPO pry23)

**Source:** CONAPO, *Conciliación Demográfica 1950–2019 y Proyecciones de la Población de
México 2020–2070* (pry23), open-data file `00_Pob_Mitad_1950_2070.csv` (mid-year population).
URL: https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/pry23/00_Pob_Mitad_1950_2070.csv
Publication year: 2023. Retrieved 2026-07-03 (downloaded with `curl -k`; the host serves an
incomplete TLS chain, so WebFetch failed — verified the download by row count 737,660 data
rows and column header `RENGLON,AÑO,ENTIDAD,CVE_GEO,EDAD,SEXO,POBLACION`).

**Method:** filter `ENTIDAD == "Ciudad de México"`, sum `POBLACION` over all ages and both
sexes per `AÑO`. This reproduces the Phase-1 anchors exactly: 2020 = 9,332,593; 2030 =
9,032,705; 2050 = 8,015,397 (matches `cdmx_ref_socioecon.csv`).

**Base-year anchor:** INEGI Censo 2020 enumeration = **9,209,944** (boletín 98/21,
https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_CdMx.pdf).
CONAPO 2020 mid-year (9,332,593) is a conciliated/projected series and runs ~123k above the
raw census count. **Decision:** use the CONAPO series for the trajectory shape and levels
across all model years (it is the internally consistent yearly series the national baseline
also derives from), and treat the Censo 9,209,944 as the base-year cross-check. The two
differ by ~1.3%, within tolerance.

**CDMX total is declining** — 9.15M (2015) → 9.34M peak (2019) → 9.24M (2022) → 9.03M (2030)
→ 8.02M (2050) → 6.55M (2070). Selected values (persons):

| Year | CDMX total | Year | CDMX total | Year | CDMX total |
|---|---|---|---|---|---|
| 2015 | 9,152,227 | 2030 | 9,032,705 | 2050 | 8,015,397 |
| 2020 | 9,332,593 | 2035 | 8,833,389 | 2055 | 7,683,669 |
| 2022 | 9,237,644 | 2040 | 8,609,423 | 2060 | 7,318,214 |
| 2025 | 9,183,658 | 2045 | 8,330,174 | 2070 | 6,548,490 |

The full 2015–2070 dict is embedded in `scripts/transform_socioeconomic.py` (`CDMX_POP_TOTAL`).

---

## 2. Urban / rural split (INEGI Censo 2020)

**Source:** INEGI, *Censo de Población y Vivienda 2020 — Presentación de resultados, Ciudad
de México*, chart "Distribución de la población por tamaño de localidad, 2000, 2010 y 2020".
URL: https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/cpv2020_pres_res_cdmx.pdf
Publication year: 2021. Retrieved 2026-07-03 (extracted with `pdftotext -layout`).

**Distribution of CDMX population by locality size, 2020:**
- 100,000+ hab: **97.5 %**
- 15,000–49,999 hab: 1.3 %
- 2,500–14,999 hab: 0.7 %
- **Menos de 2,500 hab (RURAL): 0.2 %**  ← 599 localities under 2,500 inhabitants

INEGI's urban/rural convention: a locality is **rural if < 2,500 inhabitants** (and not a
municipal seat); **urban if ≥ 2,500**. Therefore:
- **CDMX rural share = 0.2 %** (localidades < 2,500 hab), concentrated in the Suelo de
  Conservación of Milpa Alta, Tlalpan, and the other southern alcaldías (Milpa Alta ~250
  rural settlements; Tlalpan 200 rural localities, ~14,369 rural persons in 2020).
- **CDMX urban share = 99.8 %.**

**Method:** hold the split constant (urban 0.998 / rural 0.002) and apply it to the CONAPO
total each year. At 9,209,944 (Censo) the rural share of 0.2% ≈ 18,420 persons, consistent
with the summed alcaldía rural populations (Tlalpan ~14.4k + Milpa Alta + others). Applied to
the CONAPO 2022 total (9,237,644): urban = 9,219,169; rural = 18,475.

**Note on the national baseline contrast:** the national CSV has rural at ~18–19% of
population and declining with urbanization. CDMX is essentially fully urban, so a flat 0.2%
rural is the correct structural choice rather than inheriting the national urbanization curve.

---

## 3. GDP in USD (share of national)

**Source:** INEGI, *PIB por Entidad Federativa (PIBE) 2024*.
URL: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/pibent/PIBE2024_CP.pdf
Publication year: 2025. Retrieved 2026-07-03 (Phase-1 verified; see `cdmx_ref_socioecon.csv`).
INEGI states **CDMX contributed 15.0 % of national PIB in 2024** (14.8 % in 2023) — the
largest single-entity share nationally. CDMX 2024 = 3,886 mmp vs national 25,365 mmp
(constant 2018 prices).

**Method chosen — flat share applied to the national series:**
`CDMX_gdp[year] = national_gdp_mmm_usd[year] * 0.150`.

- **Why flat 15.0% (not a trend):** the published PIBE share is stable (14.8% 2023 → 15.0%
  2024). CDMX's economy is structurally services-dominated (83.5% tertiary, 9.9% secondary,
  ~0% primary — PIBE 2023) and grows roughly in step with the national aggregate. A flat
  share is defensible and avoids over-fitting a share trend the model does not need. The
  population share (~7.3%) and GDP share (~15.0%) diverge strongly: CDMX is ~2× more
  economically concentrated than its population, so GDP must use its own 15% denominator, not
  the population denominator.
- **Unit / peso→USD basis:** the calibration deliberately applies a **unit-free ratio (0.15)**
  to the existing national `gdp_mmm_usd` series. Whatever USD basis the national baseline uses
  (the 2022 value 2,582.57 bn is consistent with a PPP-converted series — market-exchange
  Mexican GDP was ~1.9 tn USD in 2024 per World Bank), the CDMX output inherits **exactly the
  same basis and unit** ("billion USD"). No peso→USD conversion is performed here, precisely so
  the CDMX series stays consistent with the model's national units. CDMX 2022 =
  2,582.57 × 0.15 = **387.39 bn USD**.

Selected CDMX GDP (bn USD, = national × 0.15): 2015 = 365.79; 2022 = 387.39; 2030 = 459.72;
2050 = 785.43; 2060 = 1004.92.

---

## 4. Occupancy rate (persons per dwelling)

**Source:** INEGI Censo 2020 (población 9,209,944 / viviendas particulares habitadas
2,756,319). Boletín 98/21,
https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_CdMx.pdf
Publication year: 2021. Retrieved 2026-07-03 (Phase-1 verified; households in
`cdmx_ref_socioecon.csv`).

**Method:** direct. 9,209,944 / 2,756,319 = **3.341 persons/dwelling** (national baseline was
3.982 — CDMX households are smaller, consistent with a mature, aging, services-city
demographic). `occrateinit` is an initialization value → set flat across all rows.

---

## 5. Land area (hectares)

**Source:** INEGI, *Panorama Sociodemográfico de Ciudad de México 2020*, state distribution
page: "Superficie (km²) **1 494.3** … representa el 0.1 % del territorio nacional."
URL: https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825197827.pdf
Publication year: 2021. Retrieved 2026-07-03 (extracted with `pdftotext -layout`).
Cross-checks: INEGI Marco Geoestadístico reports 1,486.45 km² (a close variant); the round
figure commonly cited is ~1,495 km². The official INEGI Panorama figure **1,494.3 km²** is
used.

**Method:** direct. 1,494.3 km² × 100 ha/km² = **149,430 ha** (national baseline 196,437,500
ha → CDMX is 0.076% of the national area value in the model). Set flat across all rows.

---

## 6. Elasticity (kept national)

`elasticity_gnrl_rate_occupancy_to_gdppc` = **-0.1**, unchanged from the national baseline.
This is a behavioral/technical elasticity (how household occupancy responds to GDP per
capita), not a CDMX-specific stock. No CDMX-specific estimate exists and the mechanism is not
structurally different in CDMX, so per the downscaling strategy (technical factors → keep
national) it is left at the national default and documented here.

---

## 7. Data gaps / caveats flagged

1. **Census vs CONAPO base-year gap (~1.3%):** CONAPO 2020 mid-year 9,332,593 vs Censo
   enumeration 9,209,944. Trajectory uses CONAPO (internally consistent yearly series);
   accepted, within tolerance. If a sector needs the strict census base, note the −1.3%.
2. **Urban/rural split held constant at 0.998/0.002.** INEGI publishes the 2000/2010/2020
   distribution but not a projected split to 2070. The rural share has been ~stable and tiny;
   holding it flat is the conservative choice. Rural CDMX (~18k persons) is small enough that
   any drift is immaterial to downstream per-capita downscaling.
3. **GDP share flat at 15.0%.** PIBE gives 2023–2024 shares only (14.8→15.0%); no official
   long-run CDMX-share projection exists. Flat 15% applied to the national series; method =
   `downscaled_national` share. If a future PIBE shows share drift, revisit.
4. **GDP USD basis inherited, not re-derived.** The national `gdp_mmm_usd` 2022 value
   (2,582.57 bn) is higher than market-exchange USD GDP (~1.9 tn), consistent with a
   PPP/constant basis. The calibration applies a unit-free 0.15 ratio so CDMX inherits the
   same basis; no independent CDMX USD figure was substituted (would risk a unit mismatch).
5. **Area:** INEGI publishes 1,494.3 km² (Panorama) and 1,486.45 km² (Marco Geoestadístico);
   ~0.5% difference. Used 1,494.3 km² (Panorama, the socio-demographic reference).

---

## 8. Sources consulted (URL · pub year · retrieved 2026-07-03)

- CONAPO pry23 mid-year population CSV 1950–2070 — https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/pry23/00_Pob_Mitad_1950_2070.csv · 2023
- INEGI Censo 2020 CDMX boletín 98/21 (pop 9,209,944; viviendas 2,756,319) — https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_CdMx.pdf · 2021
- INEGI Censo 2020 CDMX "Presentación de resultados" (locality-size distribution, rural 0.2%) — https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/cpv2020_pres_res_cdmx.pdf · 2021
- INEGI Panorama Sociodemográfico CDMX 2020 (superficie 1,494.3 km²) — https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825197827.pdf · 2021
- INEGI PIBE 2024 (CDMX = 15.0% of national PIB) — https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/pibent/PIBE2024_CP.pdf · 2025
- INEGI PIBE 2023 CDMX (14.8%; sector split 83.5/9.9/0.0) — https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2024/PIBEF/PIBEF2023_CDMX.pdf · 2024
