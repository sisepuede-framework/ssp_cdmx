# Structural Decisions Log — CDMX Calibration

## D1 — Emissions scope & benchmark year (2026-07-03)

**Decision (by user, Orchestrator recommended Scope 2):**
- **Benchmark = SEDEMA 2022 CDMX inventory, Scope 1 / territorial = 23.465 Mt CO2e.**
- **Benchmark year = 2022** (model time_period 7; model runs 2015–2060).

**Consequences (must be honored by all sector agents):**
1. **ENTC (electricity generation):** CDMX imports ~99.9% of its electricity; Scope 1
   counts ONLY in-city generation (~0.106 Mt in the SEDEMA inventory). Therefore the
   SISEPUEDE ENTC output must be constrained to in-city generation only — CDMX is
   modeled as a near-total electricity importer, and grid/generation emissions from
   imported power are OUT of scope. Electricity decarbonization levers will be inert
   for CDMX under this convention (documented, accepted).
2. **Target total to hit within ±10%: 23.465 Mt** (range ≈ 21.1–25.8 Mt).
3. **Sector targets (Scope 1, 2022, ±15%), from SEDEMA Table 27:**
   - Transport (on-road + off-road) = 17.802 Mt  ← DOMINANT (~76%); highest-priority calibration
   - Energy (stationary combustion: bldg + industry + in-city power) = 5.237 Mt
   - Waste (solid + wastewater) = 0.361 Mt (mostly CH4)
   - AFOLU (agri + livestock + fires; NO LULUCF sink) = 0.067 Mt
   - IPPU ≈ 0.002 Mt (SEDEMA has no IPPU bucket; industry folded into combustion)
4. **SISEPUEDE→SEDEMA sector-mapping caveats:**
   - SISEPUEDE splits energy into inen/scoe/entc/fgtv; SEDEMA lumps stationary
     combustion. Map: SISEPUEDE (inen + scoe + in-city entc + fgtv) ≈ SEDEMA Energy 5.237.
   - SISEPUEDE FRST is a large negative sink nationally; SEDEMA EXCLUDES LULUCF sinks.
     For the territorial comparison, exclude the FRST sink from the CDMX total (or report
     it separately) so we compare like-for-like against the source-only SEDEMA figure.
   - SISEPUEDE IPPU should be driven to ~0 for CDMX (no heavy industry in city limits).
   - FGTV (oil/gas fugitive) → ~0 (no oil/gas production in CDMX).

**Alternative (not chosen):** Scope 2 consumption basis ≈ 28.6 Mt (23.5 + imported
electricity ~5.2 Mt = 11,877 GWh × 0.435). GPC full S1+S2+S3 = 40.5 Mt (2016). Kept on
record in case validation reconciliation needs a Scope-2 cross-check.

**Precedent check (inconclusive):** SISEPUEDE ships US-state regions (incl. Louisiana) as
region *data* (`attributes/attribute_region_states.csv`) but no explicit electricity-
trade/import logic was found in code; NemoMod models generation to meet regional demand.
Hence the decision was escalated to the user per the plan.
