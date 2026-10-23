"""Reforecast the UK validation folds with the structural temporal contract.

The archived fold fits are retained as the calibration evidence.  This script
only changes the forecast layer: it restores the declared UK annual and
multi-year forcing and applies the bounded future latent-transmission target.
It writes a new diagnostic root, so the historical validation artifacts remain
auditable and are never silently replaced.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
import sys

import pandas as pd
import yaml

# Make the repository-local model importable when this script is launched from
# either the repository root or ``manuscript/joi_letter``.
REPOSITORY = Path(__file__).resolve().parents[3]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from src_python.calibration.calibrate_baseline import _calibration_predicted_means
from src_python.simulation.common import make_config
from src_python.validation.run_calibration_hindcast import (
    _forecast_runtime,
    extend_ar1_conditional_mean_path,
)


DEFAULT_SOURCE_ROOT = REPOSITORY / "outputs/diagnostics/matched_candidate_validation_20261008"
DEFAULT_OUTPUT_ROOT = REPOSITORY / "outputs/diagnostics/joi_structural_validation_20261021"
COUNTRY = "United_Kingdom"
YEARS = (2023, 2024)


def reforecast_fold(source_root: Path, output_root: Path, year: int) -> dict:
    source = (
        source_root
        / "independent_folds"
        / COUNTRY
        / str(year)
        / "fold_artifacts"
        / f"test_{year}"
    )
    config = yaml.safe_load((source / "fitted_config.yaml").read_text())
    test = pd.read_csv(source / "test_observations.csv")
    structural = make_config(
        country_profile=COUNTRY,
        load_calibration=False,
        evidence_cutoff_date=f"{year}-01-01",
    )["transmission"]
    for key in (
        "seasonal_amplitude",
        "seasonal_phase",
        "multi_year_amplitude",
        "multi_year_period_years",
        "multi_year_phase_date",
        "forecast_log_beta_target",
        "forecast_reversion_rho",
    ):
        config["transmission"][key] = deepcopy(structural[key])

    config = extend_ar1_conditional_mean_path(
        _forecast_runtime(
            COUNTRY,
            config,
            test,
            evidence_cutoff_date=f"{year}-01-01",
        ),
        through_year=year,
    )
    predicted = _calibration_predicted_means(config, test, COUNTRY)
    if len(predicted) != len(test):
        raise RuntimeError(f"{year}: prediction/observation length mismatch")
    if not pd.Series(predicted).map(pd.api.types.is_number).all():
        raise RuntimeError(f"{year}: non-numeric predictions")
    predicted = pd.Series(pd.to_numeric(predicted, errors="raise"), dtype=float)
    if not predicted.ge(0.0).all() or not predicted.notna().all():
        raise RuntimeError(f"{year}: predictions must be finite and non-negative")

    out_dir = (
        output_root
        / "independent_folds"
        / COUNTRY
        / str(year)
        / "fold_artifacts"
        / f"test_{year}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    result = test[["period_start", "period_end", "reported_cases"]].copy()
    result["predicted_cases"] = predicted
    result["structural_seasonal_amplitude"] = float(structural["seasonal_amplitude"])
    result["structural_seasonal_phase_days"] = float(structural["seasonal_phase"])
    result["structural_multi_year_amplitude"] = float(structural["multi_year_amplitude"])
    result["structural_multi_year_period_years"] = float(structural["multi_year_period_years"])
    result["structural_multi_year_phase_date"] = str(structural["multi_year_phase_date"])
    result["forecast_log_beta_target"] = float(structural["forecast_log_beta_target"])
    result["forecast_reversion_rho"] = float(structural["forecast_reversion_rho"])
    result.to_csv(out_dir / "test_predictions.csv", index=False)
    yaml.safe_dump(config, (out_dir / "conditional_mean_forecast_config.yaml").open("w"), sort_keys=False)
    metadata = {
        "country": COUNTRY,
        "test_year": int(year),
        "source_fitted_config": str(source / "fitted_config.yaml"),
        "forecast_contract": "bounded_log_beta_target_plus_annual_and_multi_year_forcing",
        "structural_forcing_source": "country_profile_pre_covid_prior",
        "structural_seasonal_amplitude": float(structural["seasonal_amplitude"]),
        "structural_seasonal_phase_days": float(structural["seasonal_phase"]),
        "structural_multi_year_amplitude": float(structural["multi_year_amplitude"]),
        "structural_multi_year_period_years": float(structural["multi_year_period_years"]),
        "structural_multi_year_phase_date": str(structural["multi_year_phase_date"]),
        "forecast_log_beta_target": float(structural["forecast_log_beta_target"]),
        "forecast_reversion_rho": float(structural["forecast_reversion_rho"]),
        "reported_total": float(result["reported_cases"].sum()),
        "predicted_total": float(result["predicted_cases"].sum()),
        "predicted_to_reported_ratio": float(result["predicted_cases"].sum() / result["reported_cases"].sum()),
    }
    (out_dir / "reforecast_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()
    records = [reforecast_fold(args.source_root, args.output_root, year) for year in YEARS]
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "reforecast_manifest.json").write_text(
        json.dumps(records, indent=2) + "\n"
    )
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
