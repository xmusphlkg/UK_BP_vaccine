"""Declared UK seasonal contract for Letter scenarios.

The recovered candidate stored a seasonal phase near day 134. That phase
follows the 2024 reporting surge. Stable pre-COVID England and Wales
notifications peak in autumn, and the country profile therefore keeps a
structural prior: annual amplitude 0.14 with phase day 300, plus a weak
8-year cycle anchored on 2016-10-27. Prospective Letter scenarios must use
that prior. Leaving the candidate phase in place makes the UK projection
peak in summer and hides the seasonal term the validation layer claims to
apply.
"""
from __future__ import annotations

from typing import Any


STRUCTURAL_SEASONALITY: dict[str, Any] = {
    "seasonal_amplitude": 0.14,
    "seasonal_phase": 300.0,
    "multi_year_amplitude": 0.10,
    "multi_year_period_years": 8.0,
    "multi_year_phase_date": "2016-10-27",
}


def apply_uk_structural_seasonality(
    config: dict[str, Any],
    *,
    include_multi_year: bool = True,
) -> dict[str, Any]:
    """Replace transmission seasonality with the UK prior.

    ``include_multi_year`` stays on for a profile built from that prior. It
    stays off for the recovered candidate. That candidate was fitted without
    an 8-year cycle; adding the cycle on top of its reconstructed state pushes
    only the baseline across an epidemic threshold and turns a coverage
    contrast into an extinction contrast.
    """

    transmission = config.setdefault("transmission", {})
    if not isinstance(transmission, dict):
        raise ValueError("transmission settings must be a mapping")
    for key, value in STRUCTURAL_SEASONALITY.items():
        transmission[key] = value
    if not include_multi_year:
        transmission["multi_year_amplitude"] = 0.0
        transmission.pop("multi_year_phase_date", None)
    return config


def seasonality_record(config: dict[str, Any]) -> dict[str, Any]:
    """Return the seasonal terms currently stored on a configuration."""

    transmission = config.get("transmission", {})
    if not isinstance(transmission, dict):
        raise ValueError("transmission settings must be a mapping")
    return {key: transmission.get(key) for key in STRUCTURAL_SEASONALITY}
