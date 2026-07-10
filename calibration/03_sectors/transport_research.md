# Transport (trns/trde) — research memo & calibration derivation

Author: Orchestrator (direct; two subagent attempts died on the 14 MB SEDEMA PDF —
data was instead extracted locally with pdftotext). Retrieval date: 2026-07-06.

## Official anchors — SEDEMA Inventario de Emisiones CDMXyZC 2022 (CDMX-only, t CO2e)
Source: http://www.aire.cdmx.gob.mx/descargas/publicaciones/inventario-de-emisiones/inventario-emisiones-2022/inventario-emisiones-cdmx-2022.pdf
(Table 27 pp.134-135 / Table 36 p.152; fleet Table 5 p.39; extracted via pdftotext.)

| Category | t CO2e | SISEPUEDE mapping |
|---|---:|---|
| Autos particulares | 4,530,064 | road_light |
| Camionetas SUV | 2,180,141 | road_light |
| Taxis | 3,336,138 | road_light |
| Vagonetas | 451,940 | road_light |
| Motocicletas | 3,467,819 | road_light (see note) |
| Micro/midibuses | 1,029,875 | public |
| Autobuses | 954,113 | public |
| Metrobús/Mexibús | 40,591 | public |
| Carga ≤3.8t | 86,521 | road_heavy_freight |
| Tractocamiones | 310,987 | road_heavy_freight |
| Carga >3.8t | 601,090 | road_heavy_freight |
| **On-road total** | **16,989,280** | |
| Aviación (off-road) | 417,812 | aviation |
| Locomotoras (off-road) | ~25,100 | rail_freight |
| **Transport total** | **17,802,005** | |

Fleet (Table 5, CDMX+ZC): 7,636,900 total; 96% gasoline; motos 1,505,191 (725 electric);
INEGI CDMX-only fleet 6,509,434 (2024).

## Method — inverse calibration
The model chain is linear in (deminit × frac): emissions_c ∝ deminit·frac_c·occ_c⁻¹·
fuelmix·eff⁻¹·EF, with eff/EF national (kept). From the current model decomposition
(post-energy run, 2022): road_light 5.428 Mt, public 0.665, powered_bikes 0.177,
aviation 1.042, road_heavy_freight 29.940, water 9.185, rail_freight 1.174.
Per-category multipliers target/current give the calibrated products:

- Urban pool: products (pkm/cap·frac): road_light 10,916, public 3,674,
  powered_bikes 286, human 263 → deminit = **15,139 pkm/cap**, fracs
  0.7211/0.2427/0.0189/0.0173/water 0.
- occrate public 78.35 → **25** (CDMX micros dominate vkm; effective occupancy
  EOD 2017/SEMOVI ~20-30) — supplies ×3.13 of the public multiplier.
- Motorcycles: SEDEMA motos (3.468 Mt) mapped INTO road_light target (13.966 Mt
  combined) because national powered_bikes tech (55% electric, high km/L) cannot
  physically reproduce CDMX moto emissions at sane pkm; powered_bikes kept as a
  small real category (0.16 Mt) with CDMX fuel mix 99.95% gasoline (725 e-motos
  of 1.5M, Table 5).
- Regional pool: deminit 744.2 kept; fracs re-tuned: aviation 0.1324 (→0.418 Mt,
  AICM inside CDMX), road_heavy_regional 0.1403 (→0.05 Mt), road_light 0.1344,
  rail_passenger 0.5929 with fuel mix → **100% electricity** (Metro/TL/Suburbano
  electric; imported electricity out of Scope 1 per D1) → 0 combustion.
- Freight: deminit 1,081,600 → **26,496 Mtkm** (2.45% of national), fracs road
  0.9148 / rail 0.0852 / water 0 / aviation 0. Derived: road tkm = 0.999 Mt ÷
  41.2 g/tkm = 24,238 Mtkm; rail = 0.024 Mt ÷ 10.63 g/tkm = 2,258 Mtkm. No port
  in CDMX → water freight 0.

## Predicted 2022 result (back-of-envelope)
road_light 13.84+0.13 + public 2.03 + powered_bikes 0.16 + aviation 0.418 +
road_heavy_regional 0.05 + freight road 0.999 + rail_freight 0.024 ≈ **17.66 Mt**
vs SEDEMA 17.802 (−0.8%).

## Scope reconciliation (documented deviation)
pkm/cap 15,139 exceeds the national 8,772 because the SEDEMA inventory is
TERRITORIAL: it counts all driving inside CDMX (metropolitan through-traffic from
the 22M-person ZMVM, extreme taxi/moto VKT), while SISEPUEDE activity is
resident-based (pop 9.24M). The inflated per-capita activity is the explicit
reconciliation device; vehicle technology (efficiency, EF) stays national.

## Kept national
All ef_trns_*, fuelefficiency_*, elecfuelefficiency_*, elasticity_*, avgload_*,
remaining occrate_* and fuelmix groups.
