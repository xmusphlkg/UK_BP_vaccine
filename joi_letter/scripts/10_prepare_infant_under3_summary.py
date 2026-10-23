"""Aggregate the exact modelled 0–2-month endpoint for the JOI Letter.

The parent model reports an all-infant (0–11 month) summary by default. The
Letter protocol uses the 0–2-month age bin, so this small conversion keeps the
displayed endpoint aligned with the protocol without changing the model code.
It reads the scenario time series and writes a compact, auditable CSV consumed
by the ggplot2 figure renderer.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "observed_baseline_legacy": "Legacy mapping",
    "observed_baseline_walker": "Walker-anchored",
}
SCENARIOS = ["current", "maternal_coverage_75",
             "maternal_coverage_80", "maternal_coverage_90"]
# The integrator stamps one weekly bin on 2036-01-01, after the declared
# 2027–2035 policy window. That bin is about 0.04 cases and is excluded.
HORIZON_START = pd.Timestamp("2027-01-01")
HORIZON_END = pd.Timestamp("2035-12-31")
RATE_COLUMNS = {
    "infant_cases": "total_infant_under3_cases",
    "infant_hospitalizations": "total_infant_under3_hospitalizations",
    "infant_deaths": "total_infant_under3_deaths",
    "infant_infections": "total_infant_under3_infections",
}


def main() -> None:
    frames = []
    for tag, label in RUNS.items():
        path = ROOT / "outputs" / "model_runs" / tag / "timeseries.parquet"
        if not path.exists():
            raise FileNotFoundError(path)
        ts = pd.read_parquet(path)
        required = {"scenario", "age_group", *RATE_COLUMNS}
        missing = sorted(required.difference(ts.columns))
        if missing:
            raise ValueError(f"{path} is missing required columns: {missing}")
        ts["calendar_date"] = pd.to_datetime(ts["calendar_date"])
        subset = ts.loc[
            ts["age_group"].eq("infant_0_2m")
            & ts["scenario"].isin(SCENARIOS)
            & ts["calendar_date"].between(HORIZON_START, HORIZON_END)
        ].copy()
        if subset.empty:
            raise ValueError(f"{path} contains no infant_0_2m rows")
        values = subset.groupby("scenario", as_index=False)[list(RATE_COLUMNS)].sum()
        values = values.rename(columns=RATE_COLUMNS)
        values["anchor"] = label
        values["anchor_code"] = tag
        values["coverage_pct"] = values["scenario"].map(
            {"current": None, "maternal_coverage_75": 75.0,
             "maternal_coverage_80": 80.0, "maternal_coverage_90": 90.0}
        )
        for column in RATE_COLUMNS.values():
            values[column] = values[column].astype(float)
            if not values[column].map(pd.notna).all() or (values[column] < 0).any():
                raise ValueError(f"Invalid values in {column} for {tag}")
        current = values.loc[values["scenario"].eq("current")]
        if len(current) != 1:
            raise ValueError(f"{tag} must contain one current row")
        for column in RATE_COLUMNS.values():
            baseline = float(current.iloc[0][column])
            values[f"relative_reduction_{column.removeprefix('total_infant_under3_')}"] = (
                1.0 - values[column] / baseline
            )
        frames.append(values)

    result = pd.concat(frames, ignore_index=True)
    result = result.sort_values(["anchor_code", "coverage_pct"], na_position="first")
    output = ROOT / "data" / "derived" / "joi_infant_under3_summary.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Wrote {output} ({len(result)} rows)")


if __name__ == "__main__":
    main()
