"""Audit the observed-baseline contrast and export the 0–2-month ledger.

The letter contrast is the paired run in ``16_run_observed_baseline.py``.
The current arm is the observed 73.0% England annual uptake. Targets are
floors above that arm. This script does not rebuild the retired profile
histories or the 58.56% recovered runs.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "observed_baseline_legacy": "Legacy mapping",
    "observed_baseline_walker": "Walker-anchored",
}
SCENARIOS = ["current", "maternal_coverage_75", "maternal_coverage_80", "maternal_coverage_90"]


def coverage_audit() -> pd.DataFrame:
    rows = []
    for tag, mechanism in RUNS.items():
        path = ROOT / "outputs" / "model_runs" / tag / "summary.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        summary = pd.read_csv(path)
        keep = summary.loc[summary["scenario"].isin(SCENARIOS)].copy()
        if len(keep) != 4:
            raise ValueError(f"{tag} summary does not contain the four letter scenarios")
        for row in keep.itertuples(index=False):
            rows.append({
                "run_tag": tag,
                "mechanism": mechanism,
                "scenario": row.scenario,
                "observed_uptake": float(row.observed_uptake),
                "applied_raw_maternal_coverage": float(row.maternal_vaccination_coverage),
                "applied_birth_exposure": float(row.maternal_birth_exposure_coverage),
                "coverage_source": row.maternal_birth_exposure_coverage_source,
                "prospective_policy": bool(row.prospective_policy),
                "maternal_protection_duration_days": float(row.maternal_protection_duration_days),
                "forecast_log_beta": float(row.forecast_log_beta),
                "policy_start": "2027-01-01",
                "policy_end": "2035-12-31",
            })
    out = pd.DataFrame(rows)
    current = out.loc[out["scenario"].eq("current")]
    if not current["applied_raw_maternal_coverage"].eq(0.73).all():
        raise ValueError("Current-arm uptake is not the observed 73.0% baseline")
    if not current["applied_birth_exposure"].round(10).eq(0.4215).all():
        raise ValueError("Current-arm birth exposure is not 0.4215")
    if not out["forecast_log_beta"].eq(-0.5).all():
        raise ValueError("A letter arm is not on the declared log-transmission baseline")
    return out.sort_values(["run_tag", "scenario"])


def endpoint_ledger() -> pd.DataFrame:
    path = ROOT / "data" / "derived" / "joi_infant_under3_summary.csv"
    endpoint = pd.read_csv(path)
    endpoint = endpoint.loc[endpoint["scenario"].isin(SCENARIOS)].copy()
    if len(endpoint) != 8:
        raise ValueError("The 0–2-month summary must contain eight observed-baseline rows")
    current = endpoint.loc[
        endpoint["scenario"].eq("current"),
        ["anchor", "total_infant_under3_cases"],
    ].rename(columns={"total_infant_under3_cases": "baseline_cases"})
    endpoint = endpoint.merge(current, on="anchor", how="left")
    endpoint["cases_averted"] = endpoint["baseline_cases"] - endpoint["total_infant_under3_cases"]
    ordered = endpoint.sort_values(["anchor_code", "coverage_pct"], na_position="first")
    for anchor, block in ordered.groupby("anchor", sort=False):
        totals = block["total_infant_under3_cases"].to_numpy()
        if len(totals) != 4 or not (totals[0] > totals[1] > totals[2] > totals[3]):
            raise ValueError(f"{anchor} 0–2-month totals are not strictly decreasing")
    return ordered


def main() -> None:
    coverage = coverage_audit()
    coverage.to_csv(ROOT / "data/derived/joi_coverage_trajectory_audit.csv", index=False)
    absolute = endpoint_ledger()
    absolute.to_csv(ROOT / "data/derived/joi_factorial_absolute.csv", index=False)
    print(f"Wrote {len(coverage)} coverage audit rows and {len(absolute)} endpoint rows")
    show = absolute.loc[:, [
        "anchor", "scenario", "total_infant_under3_cases",
        "cases_averted", "relative_reduction_cases",
    ]]
    print(show.to_string(index=False))


if __name__ == "__main__":
    main()
