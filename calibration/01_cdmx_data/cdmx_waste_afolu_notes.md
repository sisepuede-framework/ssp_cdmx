# CDMX Reference Data — Waste & AFOLU (SISEPUEDE calibration)

Compiled 2026-07-03. Official sources only (SEDEMA, SACMEX/INEGI, CORENADR/CONAFOR, INEGI Censo Agropecuario). Every value in `cdmx_ref_waste_afolu.csv` carries source_url + year. Values not found are marked `found=no`/`NA`.

---

## WASTE

### 1. Solid waste generation (Task 1)
- **12,454 tonnes/day (2023)** — city-wide RSU generation estimated by SOBSE.
  - Basis: resident pop 9,320,906 + floating pop 2,307,469; per-capita **1.071 kg/hab/day**.
  - Annualized ≈ **4.55 million tonnes/year** (derived = 12,454 × 365).
- Trend context (SEDEMA IRS series): 12,893 t/d (2014) → 12,920 (2016) → 12,998 (2017) → 12,404 (2022) → 12,454 (2023). Roughly flat ~12.4–13.0 kt/day.
- Source: SEDEMA *Inventario de Residuos Sólidos de la CDMX 2023* — https://www.sedema.cdmx.gob.mx/storage/app/media/DGCPCA/residuos/IRS_2023_Completo.pdf

### 2. Composition (Task 2)
- City-wide the 2023 inventory reports an **organic ≈ 43% / inorganic ≈ 57%** split (organics = food + garden/pruning waste; inorganics dominated by mixed "aprovechamiento limitado").
- **Caveat (found=no for fine breakdown):** the 2023 IRS does NOT publish an aggregate city-wide physical-composition table with separate %papel/cartón, %plásticos, %vidrio, %metales. Those sub-fractions appear only in site-specific studies (hospitals, Central de Abasto, markets). Older IRS editions (2016–2017) contain finer characterization studies if the model needs a detailed physical composition vector.

### 3. Disposal / treatment split + landfill situation (Task 3) — KEY
- **77.70% → final disposal (landfill)**; only **1.19% recycled**. The gap between disposal and material recovery is the headline problem the inventory flags.
- **CDMX has NO active landfill of its own.** Bordo Poniente (the historic mega-site) closed in 2011; it now hosts a construction/demolition-waste (RCD) processing plant, not RSU disposal.
- All RSU is **exported to landfills in the Estado de México**. 2023 receipts (t/day):
  - La Cañada 2,284.42 · El Milagro 2,269.45 · Bicentenario 1,516.40 · La Perseverancia 230.92 · Naucalpan 476.25 (~6,777 t/d across the 5 sites). Gate fee ~95–182.62 MXN/tonne.
- Intermediate infrastructure (2023): transfer stations received **7,884.22 t/day**; selection/recycling plants received **3,076.82 t/day** (largest: San Juan de Aragón Fase II); composta plants received **352,825.18 t/year** of organics (−14.8% vs 2022, partly because Cuajimalpa did not report).
- Source: SEDEMA IRS 2023 (same URL as above).

### 3b. Exported waste — GPC scope-3 reporting line (2026-11-16)
- The calibrated model (SEDEMA territorial scope 1) only carries the in-territory stream
  (`qty_waso_initial_municipal_waste_tonne_per_capita` = 0.012 vs real 0.391): WASO 2022
  ≈ 0.083 Mt vs SEDEMA 0.048 Mt. Emissions from the waste CDMX landfills in Edomex are
  outside that scope, so Basura Cero levers barely register territorially.
- `tableau_postprocessing.build_waste_gpc_table` writes a separate
  `emissions_waste_gpc_scope3_<region>_<year>.csv` (same schema as the emissions table):
  in-territory landfill CH4 × F, F = 2,473,766 t/yr exported (6,777.44 t/d received by the
  5 Edomex sites, IRS 2023) ÷ BASE 2022 in-territory landfilled MSW (79,971 t) ≈ 30.9.
- Result (BASE): **1.56 Mt CO2e in 2022**, 1.75 (2030), 1.84 (2040), 1.82 (2060) —
  ~0.63 t CO2e per landfilled tonne. Food 1.05, paper 0.29, yard 0.12 Mt (2022).
- F is fixed, so levers that cut in-territory landfill CH4 (food waste, recycling,
  compost/biogas, gas capture) cut the exported line by the same proportion.
- Assumptions: exported stream has the in-territory composition, FOD history and 20% gas
  recovery; uses the 6,777 t/d site receipts, not 77.7% × 12,454 t/d (= 9,677 t/d; the
  gap is likely rejects/transfers not reaching the 5 sites). Not added to the territorial
  totals.

### 3c. Wastewater re-specification against SEDEMA (2026-11-16)
- SEDEMA Tabla 27: aguas residuales no tratadas 243,191 + tratamiento 65,750 = **0.309 Mt**
  (CH4 9,358 t = 262 kt; N2O 177 t = 47 kt). Domestic load only (protein N, BOD);
  industrial discharges to the sewer are folded into F_IND-COM = 1.25.
- Model was 0.798 Mt (CH4 139 kt, N2O 659 kt) and grew to 1.69 Mt by 2060:
  industrial N (0.3 kg N/m3 x 1e6 m3/mmm GDP, ~51 kt N, GDP-driven) was ~78% of N, and
  SISEPUEDE applies 0.012 g N2O-N/g N both in the untreated sewer and to its effluent.
  Earlier calibration had compensated by crushing domestic BOD (45 -> 6 g/d).
- Fix (`transform_waste.py`, TRWW_FIX): industrial N density 0; industrial COD 1e-6
  (not 0: N is allocated by COD share, 0/0 = NaN wipes all N2O); untreated-with-sewerage
  N2O EF 0; untreated-no-sewerage EF 0.005 (IPCC effluent; the model uses it as the
  effluent EF for every path); BOD 0.006 -> 0.018 kg/cap/d (national MCF 0.25 kept).
- Result (BASE): TRWW 2022 **0.312 Mt** (CH4 0.266, N2O 0.046); 0.323 (2030), 0.336
  (2040), 0.344 (2060). Waste gate 0.395 vs 0.361 (+9%, OK); total 23.649 (+0.8%).
- `wali_inc_treatment_industrial` lever now has no effect (industrial stream ~0).

### 4. Wastewater (Task 4)
- **25 PTAR in operation** (15 secondary + 10 tertiary), all public/SACMEX-operated.
- **Installed capacity 5,497 l/s (~5.5 m³/s)**; **volume treated 88.7 million m³/year (~2.8 m³/s avg)** (secondary 17.7 + tertiary 71.0 Mm³). Source: INEGI cuadro entidad (SACMEX data), 2017 — https://www.inegi.org.mx/app/cuadroentidad/CDMX/2018/02/2_11
- **Treatment coverage ≈ 17.9%** of total wastewater (SACMEX, via IPDP CDMX indicator 2022) — https://indicadores.cdmx.gob.mx/dataset/cobertura-de-tratamiento-de-aguas-residuales
- PTAR operating efficiency only ~44.5% (CONAGUA 2022) — plants run below installed capacity due to aging infrastructure.
- **Wastewater generated in the ZMVM metropolitan basin ≈ 56.6 m³/s** (CONAGUA, via SACMEX). The vast majority drains untreated (mixed with stormwater) through the Gran Canal, Túnel Emisor Central, and Río El Salto. **Treated fraction is small (~18% of city wastewater).**
- Note: more recent SACMEX press cites ~1,987 l/s currently treated with plans to reach 4,555 l/s by 2030 (Cerro de la Estrella is the largest PTAR, ~1,800 l/s serving Xochimilco/Tláhuac chinampas). Use the INEGI 2017 figures as the officially tabulated baseline.

---

## AFOLU (small but non-zero — ~half of CDMX is Suelo de Conservación)

### 5. Suelo de Conservación area + breakdown (Task 5)
- **Total: 87,296.80 ha** (SEDEMA Primer Informe, cap. 03, 2011) — http://data.sedema.cdmx.gob.mx/sedema/images/archivos/noticias/primer-informe-sedema/capitulo-03.pdf
  - Widely-cited alternative: **88,442 ha = 59% of CDMX territory** (SEDEMA *Libro Suelo de Conservación*) — https://www.sedema.cdmx.gob.mx/storage/app/media/Libro_Suelo_de_Conservacion.pdf
- **Land-use classes** (SEDEMA ecosystem-diversity map legend, categorical — hectare-per-class table is presented as a map, not a clean numeric table in the accessible PDF text): Bosque de Oyamel, Bosque de Encino, Bosque de Pino, Bosque de Aile, Matorral, Pastizal, Pastizal de alta montaña, Agrícola, Vegetación inducida, Sin vegetación, Cuerpo de agua, Urbano/Infraestructura.
- Retribution/conservation schemes cover ~13,500 ha (~15.5% of SC).

### 6. Forest area (Task 6)
- **Bosques del Valle de México within SC = 26,047 ha (29.84% of Suelo de Conservación)** — pino, encino, oyamel, aile (SEDEMA Primer Informe cap.03).
- Cross-check: INEGI Censo Agropecuario 2022 reports **33,050 ha with forestry use (aprovechamiento forestal, 47.3% of rural area)** — https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/CA_Def/CA_Def2022_CDMX.pdf
- (Full CONAFOR SNIF state diagnostic PDF exists but blocked by an expired TLS cert; the two figures above are sufficient and official.)

### 7. Agriculture area + main crops (Task 7)
- INEGI Censo Agropecuario 2022 (reference period Oct 2021–Sep 2022):
  - **Superficie de uso agrícola = 19,233 ha**; agostadero/pastos/monte = 34,423 ha; agropecuario+forestal total = 58,702 ha.
  - Main crops (sembrada ha / production t):
    - **Avena forrajera** — 5,695 ha / 82,420 t (largest annual crop by area)
    - **Maíz grano blanco** — 1,994 ha / 3,305 t (plus maíz forrajero 173 ha / 2,190 t)
    - **Nopal verdura** (perennial) — 1,486 ha cultivated / 83,680 t; ~90% in Milpa Alta; ~24.2% of national nopal production (SIAP 2020). SIAP 2021 gives ~2,226 ha in Milpa Alta borough; SEDEMA Suelo book cites ~4,300 ha nopal city-wide.
    - Papa 485 ha, brócoli 317 ha, calabaza 274 ha, agave 40 ha, alfalfa 19 ha, manzana 106 ha.
  - ~90% of production is rainfed (temporal); protected agriculture ~240 ha (greenhouses etc.).

### 8. Livestock heads (Task 8) — INEGI Censo Agropecuario 2022 (existencias al 15 sep 2022)
- **Ovinos (sheep): 32,839 head** (largest category)
- **Porcinos (pigs): 14,003 head**
- **Aves (gallos/gallinas/pollos): 50,631 head**
- **Bovinos (cattle): 6,487 head**
- **Caprinos (goats): 1,393 head**
- Colmenas (beehives): 3,102 boxes
- Source: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/CA_Def/CA_Def2022_CDMX.pdf

---

## Data-quality flags
- **Waste fine composition (papel/plástico/vidrio/metal %):** NOT found as a city-wide aggregate in IRS 2023 (found=no). Use organic/inorganic split or mine older IRS editions for a detailed physical-composition vector.
- **Wastewater volumes:** best officially-tabulated figures are INEGI/SACMEX 2017 (25 plants, 5,497 l/s capacity, 88.7 Mm³/yr treated). Treated fraction ~17.9% (2022). ZMVM-generated 56.6 m³/s is metropolitan (not CDMX-only) — flag scope when using.
- **Suelo de Conservación totals:** two official figures coexist (87,296.80 ha, 2011; 88,442 ha in the SC book). Per-vegetation-class hectares are in a map graphic, not a clean numeric table in the accessible text — categorical list captured; obtain the geospatial layer (CORENADR/SEDEMA) if per-class ha are required for calibration.
- **Years differ across indicators:** waste 2023, wastewater 2017/2022, SC/forest 2011, agriculture & livestock 2022. Note vintage when calibrating.
