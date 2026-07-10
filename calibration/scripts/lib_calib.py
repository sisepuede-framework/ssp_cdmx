"""Shared helpers for CDMX sector transformation scripts.

Design contract for every sector script:
- It is IDEMPOTENT: it sets ABSOLUTE CDMX values on its own columns, never
  incrementally scaling whatever is already there. Running it twice = running once.
- It mutates ONLY its sector's columns; all other columns are left untouched.
- It reads and writes the same working CDMX CSV (--io), in place.
- Every changed variable is logged to calibration/data_sources.csv via log_change().

The working file starts as a copy of the untouched Mexico baseline
(reference_mexico/sisepuede_adj_inputs_MEX.baseline.csv); run_all.sh chains the
sector scripts in calibration order.
"""
import csv
import datetime as dt
import os
import pathlib

import pandas as pd

REPO = pathlib.Path(__file__).resolve().parent.parent.parent          # repo root
CALIB = REPO / "calibration"
BASELINE = CALIB / "reference_mexico" / "sisepuede_adj_inputs_MEX.baseline.csv"
WORKING = REPO / "ssp_modeling" / "input_data" / "sisepuede_adj_inputs_CDMX.csv"
DATA_SOURCES = CALIB / "data_sources.csv"

DATA_SOURCES_COLS = ["variable", "subsector", "original_value_mex", "new_value_cdmx",
                     "year", "method", "source_name", "source_url", "agent", "date"]


def load(io_path):
    return pd.read_csv(io_path)


def save(df, io_path):
    df.to_csv(io_path, index=False)


def baseline_value(df_base, col, year=2022):
    """Original Mexico value of a column at a given year (for logging)."""
    row = df_base[df_base["year"] == year]
    if col in df_base.columns and len(row):
        return row[col].iloc[0]
    return None


def set_col(df, col, value):
    """Set an entire column to a scalar or an array-like aligned to df rows."""
    if col not in df.columns:
        raise KeyError(f"column not in inputs: {col}")
    df[col] = value
    return df


def log_change(rows):
    """Append rows (list of dicts with DATA_SOURCES_COLS keys) to data_sources.csv.

    Idempotent-friendly: removes any prior rows for the same (variable) written by
    the same agent before appending, so re-runs don't duplicate.
    """
    today = dt.date.today().isoformat()
    for r in rows:
        r.setdefault("date", today)
        for k in DATA_SOURCES_COLS:
            r.setdefault(k, "")
    existing = []
    if DATA_SOURCES.exists():
        with open(DATA_SOURCES) as fh:
            rd = csv.DictReader(fh)
            existing = [row for row in rd]
    new_vars = {(r["variable"], r["agent"]) for r in rows}
    existing = [row for row in existing if (row.get("variable"), row.get("agent")) not in new_vars]
    with open(DATA_SOURCES, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=DATA_SOURCES_COLS)
        w.writeheader()
        for row in existing + rows:
            w.writerow({k: row.get(k, "") for k in DATA_SOURCES_COLS})


def cli_io():
    """Standard --io argument for sector scripts (defaults to WORKING)."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--io", default=str(WORKING), help="working CDMX CSV (in place)")
    return ap.parse_args()
