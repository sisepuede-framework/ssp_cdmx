# Buildings & Industrial Energy (SCOE + INEN) — CDMX calibration research

Agent: buildings-industry-energy-agent (Phase 3, sector 4 of 7). Date: 2026-07-06.
Working file: `ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv` (mutated in place by
`calibration/scripts/transform_buildings_industry.py`).

## REVISION 2026-11-10 (supersedes targets/levers below where they differ)

**Mapping (SEDEMA Tabla 27, CDMX, t CO2e → SISEPUEDE):**

| SISEPUEDE | SEDEMA | t CO2e | Model 2022 |
|---|---|---:|---:|
| SCOE residential | Combustión habitacional 1,439,796 + Emisiones domésticas 276,535 | 1,716,331 | 1.757 Mt |
| SCOE commercial_municipal | Combustión comercial-institucional 222,081 + **Comercios y servicios regulados 312,015** (point) + Asados al carbón 26,102 | 560,198 | 0.560 Mt |
| INEN other_product_manufacturing + agriculture | Industria no regulada 2,431,878 + industrial point sources 417,054 + **Maquinaria 369,813** (off-road, from transport) + Equipos agrícolas 5,767 | 3,224,512 | 3.225 Mt |
| ENTC | Generación, transmisión y distribución de energía eléctrica | 105,949 | 0.000 Mt |
| FGTV | Fugas/distribución gas LP + HCNQ | 60 | 0.028 Mt |

Industrial point sources by giro (417,054 t) and the SSP category they would map to if
INEN were split (today all in OPM, since production-based categories are zeroed by
IPPU): química 78,578 → chemicals · papel 30,846 → paper · textiles 21,775 → textiles ·
metálicas básicas 16,863 → metals · plástico/hule 13,437 → plastic · minerales no
metálicos 3,560 → cement/glass/lime · derivados del petróleo 13,536 → (refining) ·
alimentos 110,873, bebidas 38,246, impresión 26,611, productos metálicos 16,688,
equipo de transporte 13,527, otras 24,432, misc ~8,083 → other_product_manufacturing.

**Commercial sign-flip bug (fixed):** SISEPUEDE projects per-GDP demand with
growth = Π(1 + e·r_gdppc). National `elasticity_scoe_enerdem_per_mmmgdp_commercial_municipal_*`
= +13.07 in 2019; r_gdppc(2019→2020) = −0.0855 (COVID) → factor −0.117 → commercial
heat demand and emissions negative 2020–2070 (−0.024 Mt in 2022; nationally −0.256
factor too). Fix in `transform_buildings_industry.py`: pre-2020 values held at the 2020
value (−0.5). Residential elasticities checked: no factor ≤ 0, kept.
Note: only the first-year value of `consumpinit_*` drives the projection (growth via
elasticities), so the "rescaled trajectory" levers act through their 2015 value.
Retuned: COM_HEAT 11.98 → 25.53 TJ/mmm, INEN OPM 168.1 → 157.69 TJ/mmm.

**Electricity demand (2026-11-10):** total CDMX final electricity was 18,540 GWh vs
11,877 GWh reference (CONACYT PLANEAS / SENER SIE 2022, secondary compilation; consistent
with the 3.4–3.6% national share used for downscaling). The 9.5 GJ/hh residential
appliance value came from "habitacional ≈ 56 PJ" read as 16% of SEDEMA's 351 PJ chart —
weak. Appliance intensities scaled ×0.5317 (residential 9.50 → 5.051 GJ/hh ≈ 1,540
kWh/hh/yr incl. electric heat; commercial 62.0 → 32.96 TJ/mmm); inen (11.9 PJ, part of
the OPM combustion mix) and trns (1.9 PJ) kept. Result: 42.757 PJ = 11,877 GWh.
Assumption to verify: sector split (res 36% / com 32% / ind 28% / trns 4%).

Open: "Emisiones domésticas" emits NH3 39,285 t + CO2 but no CH4/N2O — likely not
combustion (undefined in the PDF); ENTC in-city generation (0.106 Mt) is zero by D1.

## 1. Emission targets (SEDEMA Inventario de Emisiones CDMX 2022, t CO2e)

| Category (CDMX only) | t CO2e | Mapped to |
|---|---|---|
| Combustión habitacional (area) | 1,439,796 | SCOE residential heat |
| Emisiones domésticas (area, LP-related) | 276,535 | folded into SCOE residential heat |
| Combustión comercial-institucional (area) | 222,081 | SCOE commercial heat |
| Asados al carbón (area) | 26,102 | folded into SCOE commercial heat |
| **SCOE total target** | **1,964,514 ≈ 1.965 Mt** | |
| Industria no regulada (area) | 2,431,878 | INEN other_product_manufacturing (GDP-linked) |
| Point-source industrial combustion | 729,076 | split: local ~580 kt → GDP-linked; federal ~255 kt → prodinit (ippu-agent) |
| **INEN total target** | **3,160,954 ≈ 3.161 Mt** | |

Cross-check vs inventory Tabla 3 (CDMX GyCEI): puntuales 835,025 t CO2e (local 580,421 /
federal 254,604), área 5,641,122 t. Local point sources are dominated by *industria
alimentaria e impresión* (= light industry → other_product_manufacturing, scales with GDP);
federal point sources are dominated by *industria química* (→ prodinit tonnage, owned by
ippu-agent). Hence GDP-linked INEN target ≈ 2,431,878 + 580,000 ≈ **3.0 Mt**; the remaining
~0.25 Mt rides on production tonnages, **pending ippu-agent**.

## 2. Fuel-mix evidence (inventory energy balance)

Tabla 4 (CDMXyZC, PJ/yr, 2022) — sector columns relevant here:

| Fuel | Habitacional | Comercios y servicios | Industria |
|---|---|---|---|
| Gas LP | 61.40 | 12.94 | 8.47 |
| Gas natural | 6.01 | 2.49 | 177.23 |
| Diésel | N/A | 0.63 | 2.25 |
| Leña / carbón vegetal | 0.54 | 0.14 | N/A |
| Coque de petróleo/carbón | N/A | N/A | 2.07 |
| Combustóleo | N/A | <0.01 | 0.08 |
| Gasolina | N/A | <0.01 | 0.10 |
| Electricidad | 58.85 | 42.81 | 95.21 |
| **Total** | **127** | **59** | **285** |

CDMX-only balance (§1.1): 351 PJ total; transporte 49%, industria 26% (≈91 PJ, "en su
mayoría gas natural"), habitacional 16% (≈56 PJ, "predominando electricidad y gas LP"),
comercios ≈ remainder.

Derived CDMX structural facts:
- Residential combustion is **LP-dominant (≈91% of hab. gas), NG ≈9%, firewood ≈0** (0.54 of
  67.95 PJ combustion = 0.8%, metro-wide; urban CDMX lower still). National baseline mix
  (solid_biomass 0.549, diesel 0.206, kerosene/gasoline 0.074 each) is structurally wrong
  for the city — replaced.
- Commerce combustion: LP 80%, NG 15%, diesel 4%, charcoal 1% (metro shares).
- Industry burns **natural gas + LP + diesel + electricity; no coal/coke/fuel-oil relevance
  in-city** (no steel or cement plants inside CDMX; coke and combustóleo in Tabla 4 sit in
  the conurbated-zone industry).

## 3. SCOE derivation (2022 anchors)

Drivers (already calibrated): households = 9.24M / 3.34 = **2.766M hh**; GDP = **387.39 mmm USD**.
SISEPUEDE SCOE mechanics: fuel_energy = demand × frac_fuel / efficfactor_fuel;
efficfactors kept national (LP/NG 0.94, diesel 0.825, electricity 3.0).
IPCC CO2 EFs used for inversion: LP 63.1, NG 56.1, diesel 74.1 kg CO2/GJ.

**Residential heat_energy.** New fracs: LP 0.80, NG 0.10, electricity 0.10 (rest 0).
Emissions per GJ of demand = 0.80/0.94×63.1 + 0.10/0.94×56.1 = 53.70 + 5.97 = **59.67 kg CO2/GJ**.
Target 1,716,331 t → H = 1.7163e9 / (2.766e6 hh × 59.67) = **10.40 GJ/hh/yr** (baseline 11.98).
Implied citywide LP = 2.766e6 × 10.40 × 0.80/0.94 = 24.5 PJ ≈ 40% of metro habitacional LP
(61.4 PJ) — consistent with CDMX's 42% share of metro population. Implied total combustion
≈ 27.6 PJ vs ≈30 PJ inferred from the CDMX-only balance. Consistent.

**Residential elec_appliances.** CDMX habitacional ≈56 PJ − 28.6 PJ (combustion + heat-elec)
≈ 27 PJ electricity → 27e6/2.766e6 ≈ 9.9; metro-share method: 58.85×0.42/2.766 ≈ 8.9.
Set **9.5 GJ/hh/yr** (baseline 11.98). No scope-1 effect (electricity upstream).

**Commercial heat_energy.** New fracs: LP 0.65, NG 0.12, diesel 0.03, electricity 0.20.
Emissions per GJ demand = 0.65/0.94×63.1 + 0.12/0.94×56.1 + 0.03/0.825×74.1
= 43.63 + 7.16 + 2.70 = **53.49 kg CO2/GJ**.
Target 248,183 t → T = 248.183e6 / (387.3855 × 53,490 kg per TJ/mmm) = **11.98 TJ/mmm-GDP**
(baseline 73.36 — the drop reflects CDMX's services-heavy, low-thermal commercial GDP and
the SEDEMA anchor of only ~0.25 Mt commercial combustion).
Implied CDMX commercial LP ≈ 3.2 PJ ≈ 25% of metro commercial LP; matches the emission ratio
0.248 Mt CDMX / ≈1.0 Mt metro commercial combustion.

**Commercial elec_appliances.** CDMX commercial electricity ≈ 21–28 PJ (50–65% of metro
42.81 PJ; CDMX-only remainder method gives ≈27 PJ). Set 24 PJ → **62.0 TJ/mmm-GDP**
(baseline 73.36). No scope-1 effect.

Predicted SCOE 2022 = 1.716 + 0.248 = **1.965 Mt** (by construction, IPCC CO2 EFs; model
CH4/N2O from combustion add <1%). Gate: 1.965 ±15% → PASS.

## 4. INEN derivation

**Agriculture & livestock (absolute PJ).** National 103.14 PJ → CDMX. SEDEMA "equipos
agrícolas" = 5,767 t CO2e (diesel machinery, 19,233 ha in Xochimilco/Tláhuac/Milpa Alta).
Keep baseline elec/fuel split but move oil→diesel (0.4771). Energy: 5,767 t /
(0.4771 × 74.1 kg/GJ) = 163,100 GJ → set **0.163 PJ** (÷632 vs national).

**other_product_manufacturing intensity (GDP-linked).** CDMX light industry (food, beverage,
printing — 677 of 845 CDMX establishments are local, predominately alimentaria/impresión).
New fuel mix: electricity 0.40, natural_gas 0.44, LP 0.10, diesel 0.06 (coal/oil/biomass → 0).
Emissions per GJ total demand = 0.44×56.1 + 0.10×63.1 + 0.06×74.1 = 24.68 + 6.31 + 4.45 =
**35.44 kg CO2/GJ**. Target 3.0 Mt → E = 3.0e9/35.44 = 84.65 PJ;
I = 84,650 TJ / (387.3855 mmm × 0.995992 scalar) = **219.4 TJ/mmm-GDP** (baseline 241.85).
Sanity: 84.65 PJ + 0.16 PJ agri ≈ 85 PJ vs inventory CDMX industria ≈91 PJ (residual is
federal/regulated industry that rides on prodinit) ✓. Electricity share 33.9 PJ ≈ 36% of
metro industrial electricity ✓.

**frac_inen_* for production categories** (cement, chemicals, electronics, glass,
lime_and_carbonite, metals, mining, paper, plastic, rubber_and_leather + recycled_*):
CDMX industry burns no coal/coke/fuel-oil → shift baseline coal+coke+oil shares into
natural_gas, keep electricity/other shares; each group re-sums to 1 (asserted).
Intensities per tonne (`consumpinit_inen_energy_tj_per_tonne_production_*`) kept national
(technology property). Production *levels* (prodinit_ippu_*) untouched — **owned by
ippu-agent**; until it collapses national tonnages to CDMX, the production part of INEN
(≈15–17 Mt CO2e with the new fuel mixes, down from ≈37 Mt) remains inflated by design.

Predicted INEN 2022 = GDP part 3.00 Mt + agri 0.006 Mt = **≈3.0 Mt** (gate 2.4–3.4 → PASS)
+ production part ≈15–17 Mt explicitly **pending ippu-agent**.

## 5. Kept national (deliberate)
- All `efficfactor_scoe_*` (device efficiencies), `elasticity_scoe_*`, `scalar_scoe_*`.
- All `consumpinit_inen_energy_tj_per_tonne_production_*` (per-tonne technology intensities).
- All `scalar_inen_energy_demand_*` (national efficiency-improvement trajectories).
- `frac_inen_*` for textiles/recycled_textiles (already 100% electricity) and wood/
  recycled_wood (baseline all-zero frac groups — left untouched).
- other_se SCOE segment (baseline consumption = 0).
- Time-shape preservation: consumpinit trajectories are rescaled by the 2022 ratio
  (target/baseline), keeping the baseline's efficiency/behavior trends to 2070.

## 6. Sources
- SEDEMA, Inventario de Emisiones de la CDMX y su Zona Conurbada 2022 (pre-extracted text):
  Tabla 3 (GyCEI CDMX), Tabla 4 (energy balance by sector/fuel), §1.1 (CDMX-only 351 PJ),
  §4.2 (industry establishment census: 845 CDMX industries, alimentaria/impresión dominant).
- IPCC 2006 GLs Vol.2 Table 2.2 default CO2 EFs (LP 63.1, NG 56.1, diesel 74.1 kg/GJ).
- calibration/DECISIONS.md; 02_downscaling_strategy.md §4; drivers from socioeconomic agent
  (pop 9.24M, occ 3.34, GDP 387.4 mmm USD, 15% of national).
