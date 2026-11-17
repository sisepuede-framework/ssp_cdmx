#!/usr/bin/env python
"""Print the 2022 CDMX vs SEDEMA sector gate table from a model emissions output.

Gross = sum of subsector totals excl. FRST sink. Sector mapping SISEPUEDE->SEDEMA
per calibration/DECISIONS.md. Gates: total +-10%, each sector +-15% (or within
0.4 Mt absolute for the ~0 sectors).
"""
import argparse
import pandas as pd

# Transport excludes maquinaria (0.370 Mt, construction off-road) -> Energy (inen)
# and vehicle A/C HFC (77.3 t HFC = 0.1005 Mt, inside SEDEMA "Fuentes móviles") -> IPPU,
# where SISEPUEDE models it (product_use_ods_refrigeration, IPCC 2.F.1).
# IPPU = all SEDEMA Tabla 27 HFC: vehicle A/C 0.1005 + residential A/C 0.0018.
OBS = {"Transport": 17.332, "Energy": 5.607, "IPPU": 0.102, "Waste": 0.361, "AFOLU": 0.067}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emis", required=True)
    ap.add_argument("--year", type=int, default=2022)
    a = ap.parse_args()
    df = pd.read_csv(a.emis)
    r = df[df["year"] == a.year].iloc[0]
    g = lambda k: float(r.get(f"emission_co2e_subsector_total_{k}", 0.0))
    mod = {
        "Transport": g("trns"),
        "Energy": g("scoe") + g("inen") + g("fgtv") + g("entc"),
        "IPPU": g("ippu"),
        "Waste": g("waso") + g("trww"),
        "AFOLU": g("agrc") + g("lvst") + g("lsmm") + g("soil"),
    }
    gross = sum(mod.values())
    print(f"\n{'Sector':12}{'Model':>9}{'SEDEMA':>9}{'Dev':>9}  gate")
    for s in OBS:
        o, m = OBS[s], mod[s]
        d = 100 * (m - o) / o if o else 0
        ok = "OK" if (abs(d) <= 15 or abs(m - o) < 0.4) else "OUT"
        print(f"{s:12}{m:9.3f}{o:9.3f}{d:+8.0f}%  {ok}")
    td = 100 * (gross - 23.465) / 23.465
    print("-" * 44)
    print(f"{'TOTAL':12}{gross:9.3f}{23.465:9.3f}{td:+8.1f}%  {'PASS' if abs(td) <= 10 else 'FAIL'}")
    print(f"transport share = {100*mod['Transport']/gross:.1f}% (target 76 +-5)\n")


if __name__ == "__main__":
    main()
