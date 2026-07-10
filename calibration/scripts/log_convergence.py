#!/usr/bin/env python
"""Compute the per-sector convergence metrics from a model emissions output and
append a row to calibration/04_validation/convergence_log.csv.

Gross = sum of all subsector emission totals EXCLUDING the FRST sink (per the
approved benchmark convention: SEDEMA 2022 is source-only, 23.465 Mt).
Net    = sum including FRST.
transport_share = trns / gross.

Usage:
  python log_convergence.py --emis <baseline_<label>_emissions_by_subsector.csv> \
      --sector socioeconomic --run-id cdmx_socio --year 2022 [--notes "..."]
"""
import argparse
import csv
import datetime as dt
import pathlib

import pandas as pd

CALIB = pathlib.Path(__file__).resolve().parent.parent
LOG = CALIB / "04_validation" / "convergence_log.csv"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emis", required=True)
    ap.add_argument("--sector", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--year", type=int, default=2022)
    ap.add_argument("--notes", default="")
    a = ap.parse_args()

    df = pd.read_csv(a.emis)
    efs = [c for c in df.columns if c.startswith("emission_co2e_subsector_total_")]
    row = df[df["year"] == a.year].iloc[0]
    frst = float(row.get("emission_co2e_subsector_total_frst", 0.0))
    net = float(row[efs].sum())
    gross = net - frst
    trns = float(row.get("emission_co2e_subsector_total_trns", 0.0))
    tshare = 100.0 * trns / gross if gross else 0.0

    prev = None
    if LOG.exists():
        with open(LOG) as fh:
            rows = list(csv.DictReader(fh))
        if rows:
            prev = float(rows[-1]["total_gross_Mt"])
    delta = "" if prev is None else round(gross - prev, 2)

    newrow = {
        "sector": a.sector, "run_id": a.run_id,
        "total_gross_Mt": round(gross, 2), "total_net_Mt": round(net, 2),
        "delta_vs_previous_Mt": delta, "transport_share_pct": round(tshare, 1),
        "date": dt.date.today().isoformat(), "notes": a.notes,
    }
    cols = ["sector", "run_id", "total_gross_Mt", "total_net_Mt",
            "delta_vs_previous_Mt", "transport_share_pct", "date", "notes"]
    write_header = not LOG.exists()
    with open(LOG, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        if write_header:
            w.writeheader()
        w.writerow(newrow)
    print(f"[{a.sector}] gross={gross:.1f} Mt  net={net:.1f} Mt  "
          f"transport_share={tshare:.1f}%  delta={delta}")


if __name__ == "__main__":
    main()
