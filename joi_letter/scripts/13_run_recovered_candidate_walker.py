"""Run the recovered UK history with the Walker-anchored maternal mechanism.

This is the missing fourth cell for the history × mechanism cross-check used
in the redesigned Figure 2.  The history is held fixed to the recovered
candidate; only the maternal conditional mechanism is changed.
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
WALKER_VE_DISEASE = 0.846
MATERNAL_RELATIVE_EFFECT = 0.75
MATERNAL_VE_SUS = 0.55
SCENARIO_MATERNAL_PROTECTION_DURATION = 180.0
WALKER_VE_SYM = (
    1
    - (1 - WALKER_VE_DISEASE)
    / (1 - MATERNAL_RELATIVE_EFFECT * MATERNAL_VE_SUS)
) / MATERNAL_RELATIVE_EFFECT


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def build_scenarios():
    cfgs = load_configs()
    candidate, candidate_path, fit = _load_candidate(CANDIDATE_ROOT, "United_Kingdom")
    history = _production_candidate_config(
        candidate,
        country="United_Kingdom",
        candidate_path=candidate_path,
        candidate_summary=fit,
        horizon_years=9,
    )
    # Match the target mechanism and duration in the baseline so the paired
    # contrast isolates coverage under a common maternal-protection history.
    history = deepcopy(history)
    history.setdefault("natural_history", {})[
        "maternal_protection_duration"
    ] = SCENARIO_MATERNAL_PROTECTION_DURATION
    # Apply before intervention copies the history. A later overwrite of the
    # outer config does not reach the stored history trajectory.
    seasonality_before = seasonality_record(history)
    apply_uk_structural_seasonality(history, include_multi_year=False)
    immunity = history.setdefault("immunity_model", {})
    immunity["maternal_VE_sus"] = MATERNAL_VE_SUS
    immunity["maternal_VE_sym"] = WALKER_VE_SYM
    immunity["maternal_relative_effect"] = MATERNAL_RELATIVE_EFFECT
    scenarios = [{
        "config": deepcopy(history),
        "analysis": "joi_letter_recovered_candidate",
        "scenario": "current",
        "vaccine_scenario": "symptom_protective",
        "resistance_scenario": cfgs["baseline"].get(
            "baseline_resistance_scenario", "country_timeline"
        ),
        "intervention": "current",
        "metadata": {
            "country": "United_Kingdom",
            "coverage_target": None,
            "maternal_protection_duration_days":
                SCENARIO_MATERNAL_PROTECTION_DURATION,
            "mechanism": "walker_anchored",
            "candidate_calibration_status": fit.get("calibration_status"),
            "candidate_calibration_accepted": bool(
                fit.get("calibration_accepted", False)
            ),
        },
        "seasonality_before": seasonality_before,
    }]
    for target in (0.75, 0.80, 0.90):
        intervention = {
            "maternal_coverage_min": target,
            "vaccine_overrides": {
                "maternal_VE_sus": MATERNAL_VE_SUS,
                "maternal_VE_sym": WALKER_VE_SYM,
                "maternal_relative_effect": MATERNAL_RELATIVE_EFFECT,
            },
            "natural_history_overrides": {
                "maternal_protection_duration":
                    SCENARIO_MATERNAL_PROTECTION_DURATION
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
        scenarios.append({
            "config": policy,
            "analysis": "joi_letter_recovered_candidate",
            "scenario": f"maternal_coverage_{int(target * 100)}",
            "vaccine_scenario": "symptom_protective",
            "resistance_scenario": cfgs["baseline"].get(
                "baseline_resistance_scenario", "country_timeline"
            ),
            "intervention": f"maternal_coverage_{int(target * 100)}",
            "metadata": {
                "country": "United_Kingdom",
                "coverage_target": target,
                "maternal_protection_duration_days":
                    SCENARIO_MATERNAL_PROTECTION_DURATION,
                "mechanism": "walker_anchored",
                "candidate_calibration_status": fit.get("calibration_status"),
                "candidate_calibration_accepted": bool(
                    fit.get("calibration_accepted", False)
                ),
            },
        })
    return scenarios, candidate_path, fit


def main() -> None:
    scenarios, candidate_path, fit = build_scenarios()
    replaced = scenarios[0].pop("seasonality_before")
    for item in scenarios:
        item.pop("seasonality_before", None)
    ts, summary = execute_scenario_list(
        scenarios,
        stem="joi_letter_recovered_candidate_walker",
        n_jobs=int(os.environ.get("JOI_N_JOBS", "4")),
    )
    summary = add_relative_reductions(summary, reference_scenario="current")
    summary["candidate_calibration_status"] = fit.get("calibration_status")
    summary["candidate_calibration_accepted"] = bool(
        fit.get("calibration_accepted", False)
    )
    out = ROOT / "outputs/model_runs/recovered_candidate_walker"
    out.mkdir(parents=True, exist_ok=True)
    ts.to_parquet(out / "timeseries.parquet", index=False)
    summary.to_csv(out / "summary.csv", index=False)
    metadata = {
        "candidate_path": str(candidate_path.resolve()),
        "candidate_sha256": sha256(candidate_path),
        "candidate_calibration_status": fit.get("calibration_status"),
        "candidate_calibration_accepted": bool(fit.get("calibration_accepted", False)),
        "walker_ve_disease": WALKER_VE_DISEASE,
        "maternal_ve_sus": MATERNAL_VE_SUS,
        "maternal_ve_sym": WALKER_VE_SYM,
        "maternal_relative_effect": MATERNAL_RELATIVE_EFFECT,
        "maternal_protection_duration_days":
            SCENARIO_MATERNAL_PROTECTION_DURATION,
        "interpretation": (
            "Exploratory recovered candidate with Walker-anchored mechanism; "
            "not a validated national forecast."
        ),
        "candidate_seasonality_before_structural_prior": replaced,
        "structural_seasonality": seasonality_record(scenarios[0]["config"]),
        "summary_sha256": sha256(out / "summary.csv"),
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    combined_frames = []
    for run_tag in (
        "legacy_ve",
        "walker_anchored",
        "recovered_candidate_legacy",
        "recovered_candidate_walker",
    ):
        summary_path = ROOT / "outputs/model_runs" / run_tag / "summary.csv"
        if summary_path.exists():
            frame = pd.read_csv(summary_path)
            frame["run_tag"] = run_tag
            combined_frames.append(frame)
    if combined_frames:
        pd.concat(combined_frames, ignore_index=True).to_csv(
            ROOT / "outputs/tables/joi_model_scenario_summary.csv", index=False
        )
    cols = [
        "scenario",
        "total_infant_cases",
        "relative_reduction_infant_cases",
        "maternal_vaccination_coverage",
    ]
    print(summary[[c for c in cols if c in summary]].to_string(index=False))


if __name__ == "__main__":
    main()
