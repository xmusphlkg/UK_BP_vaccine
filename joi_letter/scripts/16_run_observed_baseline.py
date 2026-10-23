"""Reconstruct the Letter contrast on the observed coverage baseline.

The previous prospective runs held maternal uptake at the staged 58.56%
profile and, after the fitted log-beta path ended on 2024-12-31, let the
transmission multiplier fall back to 1. That fallback is the runaway the UK
structural contract was written to prevent. This runner keeps the fitted
history through 2024, then holds three prospective choices fixed for every
arm:

- antenatal uptake 73.0% in the current arm, the 2025-26 England annual
  estimate, with 75%, 80% and 90% applied as floors above it;
- log-transmission held at the declared baseline -0.50 from 2025-01-01;
- the pre-COVID annual term only (amplitude 0.14, phase day 300).

Both mechanism arms share that history. Walker anchoring is applied only in
the prospective window. Maternal protection is 180 days in that same window.
The fitted history keeps its own 90-day duration.

The integrated reductions from this runner are a mechanism diagnostic. The
reported coverage contrast is the screening identity in the letter: incidence
scales with 1 - coverage * VE, using Walker's window estimate directly.
The slope 0.55, the 180-day clock and the VE decomposition are not replaced
here, because each lacks a clinical estimand that can be stacked on that VE.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from copy import deepcopy
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parents[1]
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from src_python.simulation.common import (  # noqa: E402
    add_relative_reductions,
    apply_intervention_definition,
    execute_scenario_list,
    load_configs,
)
from src_python.simulation.run_exploratory_candidate_strategies import (  # noqa: E402
    _load_candidate,
    _production_candidate_config,
)
from uk_structural_seasonality import (  # noqa: E402
    apply_uk_structural_seasonality,
    seasonality_record,
)

CANDIDATE_ROOT = PARENT / "data/processed/recovered_candidate_baselines_20261008"
OBSERVED_UPTAKE = 0.730
FORECAST_LOG_BETA = -0.50
FORECAST_END = "2035-12-31"
PROTECTION_DAYS = 180.0
LEGACY_VE = {
    "maternal_VE_sus": 0.55,
    "maternal_VE_sym": 0.92,
    "maternal_relative_effect": 0.75,
}
WALKER_DISEASE_VE = 0.846
WALKER_VE = {
    "maternal_VE_sus": 0.55,
    "maternal_relative_effect": 0.75,
    "maternal_VE_sym": (
        1.0 - (1.0 - WALKER_DISEASE_VE) / (1.0 - 0.75 * 0.55)
    ) / 0.75,
}
TARGETS = (0.75, 0.80, 0.90)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hold_declared_transmission(config: dict) -> str:
    """Hold log-beta at the declared baseline after the fitted path."""

    variation = config.setdefault("transmission", {}).setdefault(
        "log_beta_time_variation", {}
    )
    periods = variation.get("periods")
    if not isinstance(periods, list) or not periods:
        raise ValueError("The candidate has no fitted log-beta path to extend.")
    last_end = max(str(period["end_date"]) for period in periods)
    if last_end != "2024-12-31":
        raise ValueError(f"Fitted log-beta path ends on {last_end}, not 2024-12-31.")
    start = "2025-01-01"
    periods.append(
        {
            "start_date": start,
            "end_date": FORECAST_END,
            "log_multiplier": FORECAST_LOG_BETA,
            "state_origin": "declared_bounded_forecast_baseline",
        }
    )
    variation["forecast_log_beta_target"] = FORECAST_LOG_BETA
    variation["forecast_reversion_rho"] = 0.0
    variation["forecast_process_contract"] = "held_declared_baseline"
    return last_end


def build_history():
    cfgs = load_configs()
    candidate, candidate_path, fit = _load_candidate(CANDIDATE_ROOT, "United_Kingdom")
    history = _production_candidate_config(
        candidate,
        country="United_Kingdom",
        candidate_path=candidate_path,
        candidate_summary=fit,
        horizon_years=9,
    )
    fitted_end = hold_declared_transmission(history)
    before = seasonality_record(history)
    apply_uk_structural_seasonality(history, include_multi_year=False)
    return history, cfgs, candidate_path, fit, before, fitted_end


def scenario_item(history, cfgs, fit, *, mechanism: str, uptake: float, floor: bool, ve: dict):
    intervention = {
        "maternal_coverage" if not floor else "maternal_coverage_min": uptake,
        "vaccine_overrides": ve,
        "natural_history_overrides": {
            "maternal_protection_duration": PROTECTION_DAYS,
        },
    }
    policy = apply_intervention_definition(
        deepcopy(history),
        intervention,
        history_config=history,
        history_vaccine_scenario="symptom_protective",
        history_resistance_scenario=cfgs["baseline"].get(
            "baseline_resistance_scenario", "country_timeline"
        ),
    )
    name = "current" if not floor else f"maternal_coverage_{int(round(uptake * 100))}"
    return {
        "config": policy,
        "analysis": "joi_letter_observed_baseline",
        "scenario": name,
        "vaccine_scenario": "symptom_protective",
        "resistance_scenario": cfgs["baseline"].get(
            "baseline_resistance_scenario", "country_timeline"
        ),
        "intervention": name,
        "metadata": {
            "country": "United_Kingdom",
            "mechanism": mechanism,
            "observed_uptake": OBSERVED_UPTAKE,
            "coverage_target": None if not floor else uptake,
            "maternal_protection_duration_days": PROTECTION_DAYS,
            "forecast_log_beta": FORECAST_LOG_BETA,
            "candidate_calibration_status": fit.get("calibration_status"),
        },
    }


def build_arm(history, cfgs, fit, *, mechanism: str, ve: dict):
    items = [
        scenario_item(
            history, cfgs, fit, mechanism=mechanism, uptake=OBSERVED_UPTAKE,
            floor=False, ve=ve,
        )
    ]
    for target in TARGETS:
        items.append(
            scenario_item(
                history, cfgs, fit, mechanism=mechanism, uptake=target,
                floor=True, ve=ve,
            )
        )
    return items


def exposure_audit(items: list[dict]) -> pd.DataFrame:
    rows = []
    for item in items:
        meta = item["config"].get("metadata", {})
        birth = item["config"]["demography"]["birth_entry"]
        rows.append(
            {
                "scenario": item["scenario"],
                "mechanism": item["metadata"]["mechanism"],
                "uptake": meta.get("maternal_vaccination_coverage"),
                "birth_exposure": meta.get("maternal_birth_exposure_coverage"),
                "birth_V": birth.get("V", birth.get("M_protected")),
                "duration": item["config"]["natural_history"]["maternal_protection_duration"],
                "source": meta.get("maternal_birth_exposure_coverage_source"),
                "prospective": bool(meta.get("prospective_policy")),
            }
        )
    return pd.DataFrame(rows)


def assert_identified(summary: pd.DataFrame, timeseries: pd.DataFrame) -> dict:
    current = summary.loc[summary["scenario"].eq("current")].iloc[0]
    exposure = float(current["maternal_birth_exposure_coverage"])
    uptake = float(current["maternal_vaccination_coverage"])
    if abs(uptake - OBSERVED_UPTAKE) > 1e-9:
        raise RuntimeError(f"Current uptake is {uptake}, not {OBSERVED_UPTAKE}.")
    if abs(exposure - 0.4215) > 1e-9:
        raise RuntimeError(f"Current birth exposure is {exposure}, not 0.4215.")
    infant = timeseries.loc[
        timeseries["age_group"].eq("infant_0_2m")
        & timeseries["scenario"].eq("current")
    ].copy()
    infant["year"] = pd.to_datetime(infant["calendar_date"]).dt.year
    annual = infant.groupby("year")["infant_cases"].sum()
    window = annual.loc[(annual.index >= 2029) & (annual.index <= 2035)]
    if window.empty or float(window.min()) <= 0.0:
        raise RuntimeError(f"Prospective infant series is empty or zero: {annual.to_dict()}")
    ratio = float(window.max() / window.min())
    if ratio > 4.0:
        raise RuntimeError(
            "Prospective 0-2-month burden still takes off after the bounded "
            f"baseline (max/min={ratio:.2f}): {window.round(1).to_dict()}"
        )
    order = ["current", "maternal_coverage_75", "maternal_coverage_80", "maternal_coverage_90"]
    endpoint = (
        timeseries.loc[timeseries["age_group"].eq("infant_0_2m")]
        .groupby("scenario")["infant_cases"].sum()
        .reindex(order)
    )
    if endpoint.isna().any() or (endpoint.diff().dropna() > 1e-6).any():
        raise RuntimeError(
            "0-2-month cases are not monotone across coverage floors: "
            f"{endpoint.round(1).to_dict()}"
        )
    return {
        "annual_2029_2035": {int(k): float(v) for k, v in window.items()},
        "max_min_ratio": ratio,
        "under3_cases": {key: float(value) for key, value in endpoint.items()},
    }


def run_arm(tag: str, items: list[dict], fit: dict, candidate_path: Path, before: dict) -> pd.DataFrame:
    ts, summary = execute_scenario_list(
        items,
        stem=f"joi_letter_{tag}",
        n_jobs=int(os.environ.get("JOI_N_JOBS", "4")),
    )
    summary = add_relative_reductions(summary, reference_scenario="current")
    check = assert_identified(summary, ts)
    out = ROOT / "outputs" / "model_runs" / tag
    out.mkdir(parents=True, exist_ok=True)
    ts.to_parquet(out / "timeseries.parquet", index=False)
    summary.to_csv(out / "summary.csv", index=False)
    metadata = {
        "observed_annual_uptake_2025_26": OBSERVED_UPTAKE,
        "birth_exposure_mapping": "clip(0.02 + 0.55 * uptake, 0, 0.75)",
        "forecast_log_beta_from_2025": FORECAST_LOG_BETA,
        "fitted_log_beta_end": "2024-12-31",
        "seasonality_before": before,
        "structural_seasonality": seasonality_record(items[0]["config"]),
        "maternal_protection_duration_days_prospective": PROTECTION_DAYS,
        "historical_maternal_protection_duration_days": 90.0,
        "path_check": check,
        "candidate_path": str(candidate_path.resolve()),
        "candidate_sha256": sha256(candidate_path),
        "candidate_calibration_status": fit.get("calibration_status"),
        "interpretation": (
            "Paired coverage contrast from the observed 73% baseline under the "
            "declared transmission bound. Not a validated national forecast."
        ),
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(tag, json.dumps(check))
    return summary


def main() -> None:
    history, cfgs, candidate_path, fit, before, fitted_end = build_history()
    legacy = build_arm(history, cfgs, fit, mechanism="legacy", ve=LEGACY_VE)
    walker = build_arm(history, cfgs, fit, mechanism="walker", ve=WALKER_VE)
    audit = pd.concat(
        [exposure_audit(legacy), exposure_audit(walker)], ignore_index=True
    )
    print(audit.to_string(index=False))
    print("fitted log-beta ends", fitted_end)
    if "--audit-only" in sys.argv:
        return
    columns = [
        "scenario", "maternal_vaccination_coverage", "maternal_birth_exposure_coverage",
        "total_infant_cases", "relative_reduction_infant_cases",
    ]
    legacy_summary = run_arm(
        "observed_baseline_legacy", legacy, fit, candidate_path, before
    )
    walker_summary = run_arm(
        "observed_baseline_walker", walker, fit, candidate_path, before
    )
    for label, frame in (("LEGACY", legacy_summary), ("WALKER", walker_summary)):
        print(label)
        print(frame[[c for c in columns if c in frame.columns]].to_string(index=False))


if __name__ == "__main__":
    main()
