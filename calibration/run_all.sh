#!/usr/bin/env bash
# Rebuild the CDMX SISEPUEDE input database from the untouched Mexico baseline,
# reproducibly, by chaining the per-sector transformation scripts in calibration
# order. Idempotent: each script sets absolute CDMX values on its own columns.
#
# Usage:  bash calibration/run_all.sh [--run]
#   (default) rebuild CDMX inputs only.
#   --run     also execute the SISEPUEDE model and print the 2022 gate table.
#
# Env: ssp_mex_env (NOT the env named in environment.yml — that one is broken).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="/Users/fabianfuentes/miniconda3/envs/ssp_mex_env/bin/python"
BASELINE="$REPO/calibration/reference_mexico/sisepuede_adj_inputs_MEX.baseline.csv"
WORKING="$REPO/ssp_modeling/input_data/sisepuede_adj_inputs_CDMX.csv"
SCRIPTS="$REPO/calibration/scripts"

echo "[run_all] seeding CDMX inputs from untouched Mexico baseline"
cp "$BASELINE" "$WORKING"

# calibration order (drivers first; each depends only on the baseline, so order
# is not strictly required for correctness, but this matches the documented flow)
for t in socioeconomic energy_supply transport buildings_industry waste ippu afolu; do
  echo "[run_all] applying transform_$t"
  "$PY" "$SCRIPTS/transform_$t.py" --io "$WORKING"
done
echo "[run_all] CDMX inputs rebuilt -> $WORKING"

if [[ "${1:-}" == "--run" ]]; then
  echo "[run_all] running SISEPUEDE model (energy on; ~2-3 min)"
  "$PY" "$SCRIPTS/run_baseline.py" --input "$WORKING" --label cdmx \
        --out-dir "$REPO/calibration/04_validation"
  "$PY" "$SCRIPTS/diagnose_2022.py" \
        --emis "$REPO/calibration/04_validation/baseline_cdmx_emissions_by_subsector.csv"
fi
