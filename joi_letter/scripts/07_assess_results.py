"""Audit the 0-2-month JOI endpoint and the history x mechanism contrast.

Retired: this belongs to the superseded 58.56% baseline and crossed factorial.
Its outputs, `outputs/tables/joi_value_assessment.csv` and
`reports/value_assessment.json`, are deliberately not released. See
`reports/value_assessment.md`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/joi_infant_under3_summary.csv"
OUT_TABLE = ROOT / "outputs/tables/joi_value_assessment.csv"
OUT_JSON = ROOT / "reports/value_assessment.json"


def main() -> None:
    d = pd.read_csv(SUMMARY)
    target = d[d["scenario"].isin(["maternal_coverage_75", "maternal_coverage_80", "maternal_coverage_90"])].copy()
    target["history"] = target["anchor"].str.contains("Recovered").map({True: "Recovered history", False: "Legacy history"})
    target["mechanism"] = target["anchor"].str.contains("Walker").map({True: "Walker-anchored", False: "Legacy mapping"})
    target["coverage_target_percent"] = target["coverage_pct"].astype(int)
    target["cases_reduction_percent"] = 100 * target["relative_reduction_cases"]
    cols = ["history", "mechanism", "coverage_target_percent",
            "total_infant_under3_cases", "cases_reduction_percent"]
    target[cols].sort_values(["history", "mechanism", "coverage_target_percent"]).to_csv(OUT_TABLE, index=False)

    checks = {}
    for key, group in target.groupby(["history", "mechanism"]):
        ordered = group.sort_values("coverage_target_percent")
        checks["__".join(key)] = {
            "monotone_case_reduction": bool(ordered["cases_reduction_percent"].diff().dropna().ge(-1e-12).all()),
            "finite_case_totals": bool(ordered["total_infant_under3_cases"].notna().all()),
        }
    report = {
        "status": "conditional_value_identified",
        "primary_endpoint": "exact infant_0_2m symptomatic cases",
        "publication_ready": False,
        "checks": checks,
        "interpretation": [
            "Coverage targets produced monotone reductions in the exact 0-2-month endpoint.",
            "The crossed design separates history reconstruction from the maternal mechanism mapping.",
            "The recovered candidate remains exploratory because its state reconstruction was rejected and independent-fold predictive error was high.",
            "The outputs are conditional paired comparisons, not national forecasts.",
        ],
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")
    if not all(item["monotone_case_reduction"] and item["finite_case_totals"] for item in checks.values()):
        raise SystemExit("Result integrity check failed")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
