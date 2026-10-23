"""Prepare source-data ledgers for the redesigned JOI Letter figures."""
from __future__ import annotations

from pathlib import Path
import os

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "history_matched_legacy": ROOT / "outputs/model_runs/observed_baseline_legacy/timeseries.parquet",
    "history_matched_walker": ROOT / "outputs/model_runs/observed_baseline_walker/timeseries.parquet",
}
SCENARIOS = ["current", "maternal_coverage_75", "maternal_coverage_80", "maternal_coverage_90"]
HORIZON_START = pd.Timestamp("2027-01-01")
HORIZON_END = pd.Timestamp("2035-12-31")


def scenario_timeseries() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for mechanism, path in RUNS.items():
        if not path.exists():
            raise FileNotFoundError(path)
        ts = pd.read_parquet(path)
        ts["calendar_date"] = pd.to_datetime(ts["calendar_date"])
        ts = ts.loc[
            ts["age_group"].eq("infant_0_2m")
            & ts["scenario"].isin(SCENARIOS)
            & ts["calendar_date"].between(HORIZON_START, HORIZON_END),
            ["calendar_date", "scenario", "infant_cases", "infant_infections",
             "infant_hospitalizations", "infant_deaths"],
        ].copy()
        if ts.empty:
            raise ValueError(f"No 0-2 month rows found in {path}")
        # Each calendar date is repeated for the sensitive and resistant
        # strains. Summing over strains gives the modelled event total.
        ts = (
            ts.groupby(["calendar_date", "scenario"], as_index=False)
            .sum(numeric_only=True)
            .assign(mechanism=mechanism)
        )
        frames.append(ts)
    out = pd.concat(frames, ignore_index=True)
    out["calendar_date"] = pd.to_datetime(out["calendar_date"])
    out = out.sort_values(["mechanism", "calendar_date", "scenario"])
    out.to_csv(ROOT / "data/derived/joi_scenario_timeseries.csv", index=False)
    return out


def validation_timeseries() -> pd.DataFrame:
    preferred = ROOT.parents[1] / "outputs/diagnostics/joi_structural_validation_20261021/independent_folds/United_Kingdom"
    legacy = ROOT.parents[1] / "outputs/diagnostics/matched_candidate_validation_20261008/independent_folds/United_Kingdom"
    configured = os.environ.get("JOI_VALIDATION_ROOT", "")
    base = Path(configured) if configured else (preferred if preferred.exists() else legacy)
    frames: list[pd.DataFrame] = []
    for year in (2023, 2024):
        path = base / str(year) / "fold_artifacts" / f"test_{year}" / "test_predictions.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        d = pd.read_csv(path)
        required = {"period_start", "period_end", "reported_cases", "predicted_cases"}
        if not required.issubset(d.columns):
            raise ValueError(f"Validation fold {path} is missing {sorted(required - set(d.columns))}")
        keep = d[["period_start", "period_end", "reported_cases", "predicted_cases"]].copy()
        if not pd.to_numeric(keep["predicted_cases"], errors="coerce").notna().all():
            raise ValueError(f"Validation fold {path} contains non-finite predictions")
        if (pd.to_numeric(keep["predicted_cases"], errors="coerce") < 0).any():
            raise ValueError(f"Validation fold {path} contains negative predictions")
        observed_total = float(pd.to_numeric(keep["reported_cases"], errors="raise").sum())
        predicted_total = float(pd.to_numeric(keep["predicted_cases"], errors="raise").sum())
        if observed_total <= 0.0 or predicted_total / observed_total > 10.0:
            raise ValueError(
                f"Validation fold {year} fails the forecast plausibility gate: "
                f"predicted/observed={predicted_total / max(observed_total, 1e-12):.3g}"
            )
        keep["period_start"] = pd.to_datetime(keep["period_start"])
        keep["period_end"] = pd.to_datetime(keep["period_end"])
        keep["year"] = year
        keep["residual"] = keep["reported_cases"] - keep["predicted_cases"]
        keep["relative_error"] = keep["residual"] / keep["reported_cases"].replace(0, pd.NA)
        for column in d.columns:
            if column.startswith("structural_") or column in {
                "forecast_log_beta_target", "forecast_reversion_rho"
            }:
                keep[column] = d[column].iloc[0]
        frames.append(keep)
    out = pd.concat(frames, ignore_index=True).sort_values("period_start")
    out.to_csv(ROOT / "data/derived/joi_validation_timeseries.csv", index=False)
    return out


def mechanism_grid() -> pd.DataFrame:
    # The model applies maternal_relative_effect r before combining
    # acquisition and symptom protection. The resulting grid is a transparent
    # identifiability ledger, not a fitted posterior.
    r = 0.75
    disease_ve = 0.846
    ci_low, ci_high = 0.769, 0.897
    rows = []
    for raw_sus in [i / 1000 for i in range(0, 901, 5)]:
        for raw_sym in [i / 1000 for i in range(0, 1001, 5)]:
            effective = 1 - (1 - r * raw_sus) * (1 - r * raw_sym)
            if abs(effective - disease_ve) <= 0.0015 or ci_low <= effective <= ci_high:
                rows.append(
                    {
                        "raw_ve_sus": raw_sus,
                        "raw_ve_sym": raw_sym,
                        "effective_ve_sus": r * raw_sus,
                        "effective_ve_sym": r * raw_sym,
                        "effective_disease_ve": effective,
                        "inside_95ci": ci_low <= effective <= ci_high,
                    }
                )
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "data/derived/joi_mechanism_grid.csv", index=False)
    return out


def main() -> None:
    scenario_timeseries()
    validation_timeseries()
    mechanism_grid()
    print("Prepared scenario, validation and mechanism ledgers.")


if __name__ == "__main__":
    main()
