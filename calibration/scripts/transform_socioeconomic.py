"""CDMX socioeconomic (`gnrl`) driver calibration — Phase 3, sector 1 of 7.

Sets ABSOLUTE CDMX values on the socioeconomic driver columns that every other
sector downscales from. Idempotent: sets absolute values, never incremental scaling.
Touches ONLY the columns listed in CHANGED; all other columns are untouched.

Columns calibrated (real names in ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv):
  population_gnrl_urban   direct  CONAPO CDMX total * urban share (0.998)
  population_gnrl_rural   direct  CONAPO CDMX total * rural share (0.002)
  gdp_mmm_usd             share   national gdp_mmm_usd * 0.150 (INEGI PIBE 2024)
  occrateinit_gnrl_occupancy  direct  Censo 2020: 9,209,944 / 2,756,319 = 3.341
  area_gnrl_country_ha    direct  INEGI 1,494.3 km2 = 149,430 ha
  elasticity_gnrl_rate_occupancy_to_gdppc  KEPT NATIONAL (-0.1), documented, not changed

See 03_sectors/socioeconomic_research.md for full sourcing.

Run:
  /Users/fabianfuentes/miniconda3/envs/ssp_mex_env/bin/python transform_socioeconomic.py \
      --io ../../ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv
"""
import lib_calib as L

AGENT = "socioeconomic-agent"

# --- Sources -----------------------------------------------------------------
SRC_CONAPO = ("CONAPO Proyecciones de Poblacion 2020-2070 (pry23) mid-year",
              "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/pry23/00_Pob_Mitad_1950_2070.csv")
SRC_CENSO = ("INEGI Censo de Poblacion y Vivienda 2020 (CDMX, boletin 98/21)",
             "https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/ResultCenso2020_CdMx.pdf")
SRC_PRES = ("INEGI Censo 2020 CDMX Presentacion de resultados (distribucion por tamano de localidad)",
            "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/cpv2020_pres_res_cdmx.pdf")
SRC_PIBE = ("INEGI PIB por Entidad Federativa (PIBE) 2024 (CDMX = 15.0% of national)",
            "https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/pibent/PIBE2024_CP.pdf")
SRC_PANORAMA = ("INEGI Panorama Sociodemografico de CDMX 2020 (superficie 1,494.3 km2)",
                "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825197827.pdf")

# --- Calibration constants ---------------------------------------------------
RURAL_SHARE = 0.002          # INEGI Censo 2020: <2,500 hab = 0.2% of CDMX population
URBAN_SHARE = 1.0 - RURAL_SHARE
GDP_SHARE = 0.150            # INEGI PIBE 2024: CDMX = 15.0% of national PIB
OCC_RATE = 9209944 / 2756319  # Censo 2020: persons / viviendas particulares habitadas = 3.3411
AREA_HA = 1494.3 * 100.0     # INEGI 1,494.3 km2 -> 149,430 ha

# CDMX total mid-year population 2015-2070, CONAPO pry23, ENTIDAD='Ciudad de Mexico',
# summed over all ages and both sexes. Reproduces Phase-1 anchors (2020/2030/2050).
CDMX_POP_TOTAL = {
    2015: 9152227, 2016: 9196836, 2017: 9246758, 2018: 9296268, 2019: 9343071,
    2020: 9332593, 2021: 9272649, 2022: 9237644, 2023: 9221637, 2024: 9204018,
    2025: 9183658, 2026: 9159966, 2027: 9132734, 2028: 9102136, 2029: 9068610,
    2030: 9032705, 2031: 8994951, 2032: 8955799, 2033: 8915667, 2034: 8874820,
    2035: 8833389, 2036: 8791338, 2037: 8748390, 2038: 8704119, 2039: 8657948,
    2040: 8609423, 2041: 8558319, 2042: 8504596, 2043: 8448448, 2044: 8390214,
    2045: 8330174, 2046: 8268758, 2047: 8206293, 2048: 8143126, 2049: 8079472,
    2050: 8015397, 2051: 7950868, 2052: 7885723, 2053: 7819671, 2054: 7752390,
    2055: 7683669, 2056: 7613377, 2057: 7541499, 2058: 7468170, 2059: 7393679,
    2060: 7318214, 2061: 7242099, 2062: 7165561, 2063: 7088816, 2064: 7012002,
    2065: 6935213, 2066: 6858398, 2067: 6781472, 2068: 6704276, 2069: 6626630,
    2070: 6548490,
}

CHANGED = [
    "population_gnrl_urban", "population_gnrl_rural", "gdp_mmm_usd",
    "occrateinit_gnrl_occupancy", "area_gnrl_country_ha",
]


def _cdmx_total(year):
    """CDMX total population for a model year, guarding against gaps outside 2015-2070."""
    if year in CDMX_POP_TOTAL:
        return CDMX_POP_TOTAL[year]
    # Model rows are 2015-2070, fully covered; fall back to nearest bound defensively.
    yrs = sorted(CDMX_POP_TOTAL)
    return CDMX_POP_TOTAL[yrs[0]] if year < yrs[0] else CDMX_POP_TOTAL[yrs[-1]]


def transform(df, df_base=None):
    """Set absolute CDMX socioeconomic drivers on df, aligned to df['year']. Idempotent.

    GDP is derived from the UNTOUCHED national baseline series (df_base), not from the
    working column, so repeated runs do not compound the 15% share (idempotency).
    """
    if df_base is None:
        df_base = L.load(str(L.BASELINE))
    years = df["year"]
    total = years.map(_cdmx_total).astype(float)

    # Population: split CDMX total by the (flat) urban/rural share.
    L.set_col(df, "population_gnrl_urban", total * URBAN_SHARE)
    L.set_col(df, "population_gnrl_rural", total * RURAL_SHARE)

    # GDP: national gdp_mmm_usd series (from baseline) * CDMX share (unit-free ratio ->
    # same USD basis/units). Baseline is row-aligned to df (both 2015-2070, 56 rows);
    # align on 'year' to be robust.
    base_gdp = df_base.set_index("year")["gdp_mmm_usd"]
    nat_gdp = df["year"].map(base_gdp).astype(float)
    L.set_col(df, "gdp_mmm_usd", nat_gdp * GDP_SHARE)

    # Occupancy rate and area: flat CDMX values across all rows.
    L.set_col(df, "occrateinit_gnrl_occupancy", OCC_RATE)
    L.set_col(df, "area_gnrl_country_ha", AREA_HA)

    # elasticity_gnrl_rate_occupancy_to_gdppc: KEPT NATIONAL (-0.1). Intentionally untouched.
    return df


def main():
    args = L.cli_io()
    df_base = L.load(str(L.BASELINE))
    df = L.load(args.io)
    df = transform(df, df_base)
    L.save(df, args.io)

    # One log row per changed variable, using the 2022 CDMX value we just set.
    row2022 = df[df["year"] == 2022].iloc[0]
    total2022 = _cdmx_total(2022)

    def orig(col):
        return L.baseline_value(df_base, col, 2022)

    rows = [
        dict(variable="population_gnrl_urban", subsector="gnrl",
             original_value_mex=orig("population_gnrl_urban"),
             new_value_cdmx=round(total2022 * URBAN_SHARE, 2), year=2022,
             method="direct: CONAPO CDMX total * urban share 0.998 (Censo 2020 locality-size)",
             source_name=f"{SRC_CONAPO[0]}; {SRC_PRES[0]}",
             source_url=f"{SRC_CONAPO[1]} ; {SRC_PRES[1]}", agent=AGENT),
        dict(variable="population_gnrl_rural", subsector="gnrl",
             original_value_mex=orig("population_gnrl_rural"),
             new_value_cdmx=round(total2022 * RURAL_SHARE, 2), year=2022,
             method="direct: CONAPO CDMX total * rural share 0.002 (<2,500 hab, Censo 2020)",
             source_name=f"{SRC_CONAPO[0]}; {SRC_PRES[0]}",
             source_url=f"{SRC_CONAPO[1]} ; {SRC_PRES[1]}", agent=AGENT),
        dict(variable="gdp_mmm_usd", subsector="gnrl",
             original_value_mex=orig("gdp_mmm_usd"),
             new_value_cdmx=round(float(row2022["gdp_mmm_usd"]), 4), year=2022,
             method="share: national gdp_mmm_usd * 0.150 (CDMX GDP share, unit-free; USD basis inherited)",
             source_name=SRC_PIBE[0], source_url=SRC_PIBE[1], agent=AGENT),
        dict(variable="occrateinit_gnrl_occupancy", subsector="gnrl",
             original_value_mex=orig("occrateinit_gnrl_occupancy"),
             new_value_cdmx=round(OCC_RATE, 4), year=2022,
             method="direct: Censo 2020 persons 9,209,944 / viviendas 2,756,319",
             source_name=SRC_CENSO[0], source_url=SRC_CENSO[1], agent=AGENT),
        dict(variable="area_gnrl_country_ha", subsector="gnrl",
             original_value_mex=orig("area_gnrl_country_ha"),
             new_value_cdmx=round(AREA_HA, 2), year=2022,
             method="direct: INEGI CDMX superficie 1,494.3 km2 = 149,430 ha",
             source_name=SRC_PANORAMA[0], source_url=SRC_PANORAMA[1], agent=AGENT),
    ]
    L.log_change(rows)
    print("socioeconomic transform applied. Changed columns:", ", ".join(CHANGED))
    print("elasticity_gnrl_rate_occupancy_to_gdppc kept national (-0.1).")


if __name__ == "__main__":
    main()
