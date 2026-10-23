"""Run the JOI extension against the staged UK recovered candidate.

The candidate is consumed read-only from the parent project. Outputs remain
local to this Letter project, and the run is explicitly labelled exploratory
because the parent calibration gate did not accept this candidate.
"""
from __future__ import annotations
import hashlib, json, os, sys
from copy import deepcopy
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parents[1]
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from src_python.simulation.common import (  # noqa: E402
    add_relative_reductions, apply_intervention_definition, execute_scenario_list,
    load_configs,
)
from src_python.simulation.run_exploratory_candidate_strategies import (  # noqa: E402
    _load_candidate, _production_candidate_config,
)
from uk_structural_seasonality import (  # noqa: E402
    apply_uk_structural_seasonality, seasonality_record,
)

CANDIDATE_ROOT = PARENT / "data/processed/recovered_candidate_baselines_20261008"
SCENARIO_MATERNAL_PROTECTION_DURATION = 180.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_scenarios():
    cfgs = load_configs()
    candidate, candidate_path, fit = _load_candidate(CANDIDATE_ROOT, "United_Kingdom")
    history = _production_candidate_config(
        candidate, country="United_Kingdom", candidate_path=candidate_path,
        candidate_summary=fit, horizon_years=9,
    )
    # Use one maternal-protection duration for the baseline and every target.
    # The recovered candidate's source configuration is 90 days; the Letter's
    # paired scenarios use an explicit 180-day duration override.
    history = deepcopy(history)
    history.setdefault("natural_history", {})[
        "maternal_protection_duration"
    ] = SCENARIO_MATERNAL_PROTECTION_DURATION
    # Apply before intervention copies the history. A later overwrite of the
    # outer config does not reach the stored history trajectory.
    seasonality_before = seasonality_record(history)
    apply_uk_structural_seasonality(history, include_multi_year=False)
    scenarios = [{
        "config": deepcopy(history), "analysis": "joi_letter_recovered_candidate",
        "scenario": "current", "vaccine_scenario": "symptom_protective",
        "resistance_scenario": cfgs["baseline"].get("baseline_resistance_scenario", "country_timeline"),
        "intervention": "current",
        "metadata": {"country": "United_Kingdom", "coverage_target": None,
                     "maternal_protection_duration_days":
                         SCENARIO_MATERNAL_PROTECTION_DURATION,
                     "candidate_calibration_status": fit.get("calibration_status"),
                     "candidate_calibration_accepted": bool(fit.get("calibration_accepted", False))},
        "seasonality_before": seasonality_before,
    }]
    for target in (0.75, 0.80, 0.90):
        intervention = {
            "maternal_coverage_min": target,
            "vaccine_overrides": {"maternal_VE_sus": 0.55, "maternal_VE_sym": 0.92,
                                  "maternal_relative_effect": 0.75},
            "natural_history_overrides": {
                "maternal_protection_duration":
                    SCENARIO_MATERNAL_PROTECTION_DURATION
            },
        }
        policy = apply_intervention_definition(
            deepcopy(history), intervention, history_config=history,
            history_vaccine_scenario="symptom_protective",
            history_resistance_scenario=cfgs["baseline"].get("baseline_resistance_scenario", "country_timeline"),
        )
        scenarios.append({
            "config": policy, "analysis": "joi_letter_recovered_candidate",
            "scenario": f"maternal_coverage_{int(target * 100)}",
            "vaccine_scenario": "symptom_protective",
            "resistance_scenario": cfgs["baseline"].get("baseline_resistance_scenario", "country_timeline"),
            "intervention": f"maternal_coverage_{int(target * 100)}",
            "metadata": {"country": "United_Kingdom", "coverage_target": target,
                         "maternal_protection_duration_days":
                             SCENARIO_MATERNAL_PROTECTION_DURATION,
                         "candidate_calibration_status": fit.get("calibration_status"),
                         "candidate_calibration_accepted": bool(fit.get("calibration_accepted", False))},
            "seasonality_before": seasonality_before,
        })
    return scenarios, candidate_path, fit


def main():
    scenarios, candidate_path, fit = build_scenarios()
    replaced = scenarios[0].pop("seasonality_before")
    for item in scenarios:
        item.pop("seasonality_before", None)
    ts, summary = execute_scenario_list(
        scenarios,
        stem="joi_letter_recovered_candidate",
        n_jobs=int(os.environ.get("JOI_N_JOBS", "4")),
    )
    summary = add_relative_reductions(summary, reference_scenario="current")
    summary["candidate_calibration_status"] = fit.get("calibration_status")
    summary["candidate_calibration_accepted"] = bool(fit.get("calibration_accepted", False))
    out = ROOT / "outputs/model_runs/recovered_candidate_legacy"
    out.mkdir(parents=True, exist_ok=True)
    ts.to_parquet(out / "timeseries.parquet", index=False)
    summary.to_csv(out / "summary.csv", index=False)
    metadata = {
        "candidate_path": str(candidate_path.resolve()),
        "candidate_sha256": sha256(candidate_path),
        "candidate_calibration_status": fit.get("calibration_status"),
        "candidate_calibration_accepted": bool(fit.get("calibration_accepted", False)),
        "candidate_model_to_observed_reported_incidence_ratio": fit.get("model_to_observed_reported_incidence_ratio"),
        "candidate_independent_fold_smape": {"2023": 1.8921644076832587, "2024": 1.2935818981390774},
        "maternal_protection_duration_days": SCENARIO_MATERNAL_PROTECTION_DURATION,
        "interpretation": "Exploratory recovered candidate; not a validated national forecast.",
        "candidate_seasonality_before_structural_prior": replaced,
        "structural_seasonality": seasonality_record(scenarios[0]["config"]),
        "summary_sha256": sha256(out / "summary.csv"),
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    cols = ["scenario", "total_infant_cases", "total_infant_hospitalizations", "total_infant_deaths",
            "relative_reduction_infant_cases", "maternal_vaccination_coverage"]
    print(summary[[c for c in cols if c in summary]].to_string(index=False))


if __name__ == "__main__":
    main()
