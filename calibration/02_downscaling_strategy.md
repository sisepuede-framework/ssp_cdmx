# Phase 2 — CDMX Downscaling Strategy

**Date:** 2026-07-03 · **Author:** Orchestrator
**Governing decision:** [DECISIONS.md](DECISIONS.md) D1 — validate against **SEDEMA 2022
Scope-1 territorial = 23.465 Mt CO2e**, benchmark year **2022** (model time_period 7).
**Reference data:** [01_cdmx_data/cdmx_reference_values.csv](01_cdmx_data/cdmx_reference_values.csv).

## 0. General principles

SISEPUEDE inputs fall into three kinds; the calibration method depends on the kind:

| Kind | Examples | Default treatment for CDMX |
|---|---|---|
| **Drivers** (socioeconomic) | `population_gnrl_*`, `gdp`, value added | **Direct replace** with CDMX values/trajectories |
| **Activity levels** | electricity demand, fuel demand, vkm, waste tonnage, land area, livestock heads | **Direct** where a CDMX value exists; else **share-downscale** national × share |
| **Technical factors** | `ef_*` emission factors, `frac_*` splits, efficiencies, energy densities | **Keep national** (fuel chemistry / technology identical) unless CDMX is structurally different |

**Share menu (pick the denominator that matches the variable's driver):**
- population **7.3%** (per-capita / residential / household activity)
- GDP **15.0%** (economic value / commercial activity) — note ≈2× population share
- households **7.8%** (dwelling-stock activity)
- electricity consumption **3.4%** (electricity demand)
- gasoline **6.15%**, diesel(retail) **2.23%**, LP-cylinder **8.78%** (road/fuel activity)
- vehicle fleet **10.6%** (fleet-linked activity)

**Trajectories:** CDMX population is *declining* (CONAPO: 9.33M→8.0M by 2050; share
7.3%→5.5%). Where the national series grows with population, rebuild the CDMX series
from the CONAPO CDMX trajectory rather than applying a flat share to the national curve.

**Every changed value → one row in `data_sources.csv`** (variable, subsector,
original_value_mex, new_value_cdmx, year, method, source_name, source_url, agent, date).
All changes via scripts in `calibration/scripts/` — no manual CSV edits.

---

## 1. Socioeconomic (`gnrl`) — socioeconomic-agent

| Variable group | Method | Value / source |
|---|---|---|
| Population level + trajectory | **Direct** | CDMX Censo 2020 = 9,209,944; rebuild 2015–2060 from CONAPO pry23 CDMX series (declining) |
| GDP level + trajectory | **Direct/share** | CDMX = 15.0% of national PIB (2024); use PIBE trajectory |
| Value added by sector | **Direct** | services 83.5%, secondary 9.9%, primary ~0% (2023 PIBE) |
| Households | **Direct** | 2,756,319 (Censo 2020) |

**Priority: HIGHEST** — every other sector's per-capita/GDP downscaling depends on these
being right first. Calibrate `gnrl` before all other sectors.

---

## 2. Transport (`trns`, `trde`) — transport-agent  ★ DOMINANT SECTOR (17.8 Mt, 76%)

This sector determines whether we hit the benchmark. Highest calibration priority after `gnrl`.

| Variable group | Method | Value / source |
|---|---|---|
| Vehicle fleet / stock | **Direct/share** | CDMX fleet 6,509,434 (2024, 10.6%); motos 716,400. Pull class split from VMRC microdata |
| Fuel demand (road) | **Direct** | gasoline 2.713 bn L, diesel(retail) 0.292 bn L (2024). NB retail diesel understates fleet/industrial diesel |
| Modal split / passenger activity | **Direct** | EOD 2017: public 45.1%, private 21.1%, walk 32.3%; Metro 1,057M & Metrobús 438M pax (2022) |
| passenger-km / tkm | **Estimate** | pkm not published → derive from ridership × avg trip length (document method) |
| Emission factors, fuel efficiencies | **Keep national** | vehicle tech/fuel identical |

Anchor: on-road emissions must reconcile to SEDEMA 16.99 Mt. Cross-check fuel-based
bottom-up (gasoline+diesel × EF) against SEDEMA's fleet-based figure.

---

## 3. Energy — supply (`entc`, `enfu`, `fgtv`, `enst`) — energy-supply-agent

| Subsector | Method | Notes |
|---|---|---|
| **entc** (electricity generation) | **RE-SPECIFY → in-city only** | Per D1 Scope-1: CDMX generates ~none of its power (~417 MW capacity, 99.9% imported). Constrain ENTC so generation emissions ≈ in-city only (SEDEMA 0.106 Mt). Imported-electricity emissions are OUT of scope. Electricity **demand** still needed for the energy balance but must NOT create in-territory generation emissions |
| **enfu** (fuels) | **Direct/share** | Fuel supply/demand from CNE volumes; keep energy densities & EFs national |
| **fgtv** (fugitive oil/gas) | **→ ~0** | No oil/gas extraction, refining, or processing in CDMX. Zero out fugitive activity (national baseline had 76 Mt — must vanish) |
| **enst** (storage) | **National default / minimal** | Document |

**Structural note:** the single biggest transformation vs. the national baseline is
ENTC (205→~0.1 Mt) and FGTV (76→~0 Mt). Handle via the input drivers that set in-region
generation capacity/demand-for-generation, not by post-hoc zeroing, so the model stays
internally consistent. **energy-supply-agent must document exactly how ENTC is constrained.**

---

## 4. Energy — demand (`scoe`, `inen`) — buildings-industry-energy-agent (5.2 Mt stationary)

| Subsector | Method | Notes |
|---|---|---|
| **scoe** (buildings/stationary: residential, commercial) | **Direct/share** | CDMX is services-heavy. Residential energy → population/households share (7.3–7.8%); commercial → GDP share (15.0%). Gas LP + natural gas + electricity demand from CDMX energy mix (2016 infograma: gas LP 10.4%, gas nat 7.4%, elec 23.8%) |
| **inen** (industrial energy) | **Downscale hard** | Manufacturing is <9.9% of CDMX GDP and mostly light. Downscale national INEN by CDMX manufacturing value-added share (pull SCIAN 31-33; upper bound <9.9% of 15.0% national GDP). National baseline INEN 73 Mt must shrink dramatically |
| Emission factors, efficiencies | **Keep national** | |

Anchor: scoe + inen + in-city entc + fgtv must reconcile to SEDEMA Energy 5.237 Mt.

---

## 5. IPPU (`ippu`) — ippu-agent

| Method | Notes |
|---|---|
| **→ ~0 (re-specify)** | SEDEMA reports no IPPU bucket; only F-gas (HFC from AC maintenance) ≈ 0.002 Mt. Heavy industry (cement, steel, chemicals) is OUTSIDE CDMX limits. Drive IPPU production/activity variables to ~0; keep only refrigerant/product-use F-gases scaled by population (7.3%). National baseline IPPU 168 Mt must collapse to ~0 |

---

## 6. AFOLU (`agrc`, `lvst`, `lsmm`, `lndu`, `frst`, `soil`) — afolu-agent (0.067 Mt sources)

CDMX AFOLU is small but non-zero (~half the territory is Suelo de Conservación).

| Subsector | Method | Value / source |
|---|---|---|
| **lndu** (land use) | **Direct re-specify** | Suelo de Conservación 87,297 ha; map to SISEPUEDE land-use classes (forest 26,047 ha, cropland 19,233 ha, grassland/matorral, settlements). Replace national land areas entirely |
| **frst** (forest) | **Direct** | 26,047 ha forest. NB: SEDEMA excludes LULUCF sinks → for validation, report FRST sink separately / exclude from the 23.5 Mt comparison |
| **agrc** (crops) | **Direct/share** | 19,233 ha; main crops avena forrajera, nopal (Milpa Alta), maíz. Keep crop EFs national |
| **lvst** (livestock) | **Direct** | heads: poultry 50,631, sheep 32,839, pigs 14,003, cattle 6,487 (2022) — very small |
| **lsmm** (manure mgmt) | **Direct/share** | scale with livestock heads |
| **soil** (soil mgmt) | **Direct/share** | scale with agricultural area |

Anchor: agri+livestock+fires must reconcile to SEDEMA AFOLU 0.067 Mt (sources only).

---

## 7. Waste / CircularEconomy (`waso`, `trww`, `wali`) — waste-agent (0.361 Mt)

| Subsector | Method | Value / source |
|---|---|---|
| **waso** (solid waste) | **Direct** | 12,454 t/day (~4.55 Mt/yr, 2023); organic ~43%. Disposal: **77.7% landfill, exported to Edomex (CDMX has no own landfill since Bordo Poniente closed 2011)** — key for CH4 accounting; recycling 1.19% |
| **trww** (wastewater treatment) | **Direct** | 88.7 Mm³/yr treated (2017); **only 17.9% of wastewater treated** — most drains untreated (drives CH4/N2O) |
| **wali** (liquid waste / water) | **Direct/share** | scale with population/households |
| Emission factors (MCF, DOC, etc.) | **Keep national** but **review landfill MCF** | CDMX waste goes to well-managed Edomex sanitary landfills — check managed vs unmanaged MCF |

Anchor: solid waste + wastewater must reconcile to SEDEMA Waste 0.361 Mt (CH4-dominated).

---

## 8. Sector calibration order (Phase 3)

1. **socioeconomic (gnrl)** — foundation for all downscaling. Do first.
2. **transport (trns/trde)** — 76% of the target; biggest lever.
3. **energy-supply (entc/enfu/fgtv)** — the structural re-specification (ENTC→0, FGTV→0).
4. **buildings-industry (scoe/inen)** — stationary energy 5.2 Mt.
5. **ippu** — collapse to ~0.
6. **waste** — 0.36 Mt.
7. **afolu** — 0.067 Mt + land use.

## 9. Open data gaps (flagged, non-blocking)

- Manufacturing-only value-added share (SCIAN 31-33) — needs PIBE tabulado pull (bounds INEN downscaling).
- Exact CDMX electricity GWh — verify on SENER SIE portal (currently secondary source).
- CDMX vehicle class split — INEGI VMRC OLAP cube (legacy, not machine-rendered).
- Passenger-km for Metro/Metrobús — not published; must estimate.
- Natural-gas consumption by state — CENAGAS Boletín SNG (no clean CSV).
- Waste fine composition & Suelo de Conservación per-class hectares — in graphics, not tables.
