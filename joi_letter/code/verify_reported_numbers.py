"""Verify the reported numbers of the JOI letter from first principles.

This is the entry point for anyone who wants to audit the released results
without access to the authors' parent modelling repository. It uses only the
Python standard library and reads only released files.

Three families of checks are run.

1. The reported population contrast: Farrington's screening identity. With
   coverage c as the exposure prevalence, the odds ratio estimated by the
   screening method equals the disease risk ratio, so incidence in the age
   window scales with ``1 - c * VE`` and the reduction from baseline coverage
   ``c0`` to a target ``c1`` is ``1 - (1 - c1*VE) / (1 - c0*VE)``. Every number
   in the Letter table is recomputed here and compared against the released
   ledger ``data/derived/joi_reduction_readings.csv`` and against the values
   recorded in ``reports/value_assessment.md``.

2. The mechanism diagnostic: the closed-form individual effectiveness implied
   by the transmission stack, and the case-share identities, recomputed from
   their definitions.

3. Cross-file consistency: the age-structured reductions quoted in the ledger
   are read back from the endpoint ledger written by the model run.

The script exits non-zero if any check fails, so a clean run is a numerical
audit of the release.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Inputs taken as published evidence, not estimated by this project.
BASELINE_UPTAKE = 0.730          # England 2025-26 annual antenatal coverage (UKHSA)
TARGETS = (0.75, 0.80, 0.90)     # Uniform national coverage targets
VE_DISEASE = 0.846               # Walker, infants younger than 3 months
VE_DISEASE_CI = (0.769, 0.897)
VE_ONSET_2M = 0.862              # Walker, onset before 2 months
VE_HOSPITALISATION = 0.882
VE_HOSPITALISATION_CI = (0.810, 0.927)
VE_DEATH = 0.915
VE_DEATH_CI = (0.754, 0.971)

# Mechanism-stack constants, see protocol/analysis_protocol.md.
PHI = 180.0 / 271.25
LEGACY_COMPOSITE = 1.0 - (1.0 - 0.75 * 0.55) * (1.0 - 0.75 * 0.92)

# Values recorded in reports/value_assessment.md, in percent.
EXPECTED_PERCENT = {
    ("disease", 0.75): 4.4245,
    ("disease", 0.80): 15.4856,
    ("disease", 0.90): 37.6079,
    ("disease_lo", 0.90): 29.8042,
    ("disease_hi", 0.90): 44.1757,
    ("onset", 0.75): 4.6502,
    ("onset", 0.80): 16.2756,
    ("onset", 0.90): 39.5264,
    ("hospitalisation", 0.90): 42.1,
    ("hospitalisation_lo", 0.90): 33.7,
    ("hospitalisation_hi", 0.90): 48.7,
    ("death", 0.90): 46.8,
    ("death_lo", 0.90): 28.5,
    ("death_hi", 0.90): 56.7,
}

FAILURES: list[str] = []


def reduction(c0: float, c1: float, ve: float) -> float:
    """Population reduction from baseline coverage c0 to target c1."""
    return 1.0 - (1.0 - c1 * ve) / (1.0 - c0 * ve)


def case_share_uncovered(coverage: float, ve: float) -> float:
    """Share of cases occurring among infants of unvaccinated mothers."""
    return (1.0 - coverage) / (1.0 - coverage * ve)


def individual_effectiveness(composite: float) -> float:
    """Effectiveness for one infant of a vaccinated mother in the ODE stack."""
    return 1.0 - (1.0 - 0.57 * PHI * composite) / (1.0 - 0.02 * PHI * composite)


def birth_exposure(uptake: float) -> float:
    """Reduced-form map from antenatal uptake to newborn protected entry."""
    return min(0.75, max(0.0, 0.02 + 0.55 * uptake))


def check(label: str, value: float, target: float, tol: float) -> bool:
    ok = abs(value - target) <= tol
    status = "ok" if ok else "FAIL"
    if not ok:
        FAILURES.append(f"{label}: {value} vs recorded {target}")
    print(f"  [{status}] {label:<52} {value:>10.4f}  recorded {target:>10.4f}")
    return ok


def check_report(label: str, value: float, expected: float) -> bool:
    """Compare against a value quoted in ``reports/value_assessment.md``.

    Values written to four decimals are checked tightly; those the report
    rounds to one decimal are allowed half a unit in the last place.
    """
    tol = 5e-4 if round(expected, 2) != expected else 0.05
    return check(label, value, expected, tol)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise SystemExit(f"missing released file: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def check_screening_contrast() -> None:
    print("\n1. Reported population contrast (screening identity)")

    ledger = {
        row["floor"]: row
        for row in read_csv(ROOT / "data/derived/joi_reduction_readings.csv")
        if row["reading"].startswith("Walker")
    }

    for target in TARGETS:
        key = f"{int(target * 100)}%"
        if key not in ledger:
            FAILURES.append(f"missing Walker row for {key} in reduction ledger")
            print(f"  [FAIL] {key:<52} row absent")
            continue
        row = ledger[key]
        # The released ledger stores reductions in percent.
        value = 100 * reduction(BASELINE_UPTAKE, target, VE_DISEASE)
        check(f"cases <3 months, target {key}", value, float(row["reduction"]), 1e-6)
        check(
            f"cases <3 months, target {key}, CI low",
            100 * reduction(BASELINE_UPTAKE, target, VE_DISEASE_CI[0]),
            float(row["lo"]),
            1e-6,
        )
        check(
            f"cases <3 months, target {key}, CI high",
            100 * reduction(BASELINE_UPTAKE, target, VE_DISEASE_CI[1]),
            float(row["hi"]),
            1e-6,
        )
        check_report(f"cases <3 months, target {key} vs report", value, EXPECTED_PERCENT[("disease", target)])
    check(
        "cases <3 months, target 90%, CI low vs report",
        100 * reduction(BASELINE_UPTAKE, 0.90, VE_DISEASE_CI[0]),
        EXPECTED_PERCENT[("disease_lo", 0.90)],
        0.05,
    )
    check(
        "cases <3 months, target 90%, CI high vs report",
        100 * reduction(BASELINE_UPTAKE, 0.90, VE_DISEASE_CI[1]),
        EXPECTED_PERCENT[("disease_hi", 0.90)],
        0.05,
    )

    for target in TARGETS:
        check_report(
            f"onset <2 months, target {int(target * 100)}%",
            100 * reduction(BASELINE_UPTAKE, target, VE_ONSET_2M),
            EXPECTED_PERCENT[("onset", target)],
        )

    for key, ve, ci in (
        ("hospitalisation", VE_HOSPITALISATION, VE_HOSPITALISATION_CI),
        ("death", VE_DEATH, VE_DEATH_CI),
    ):
        label = "hospitalisations" if key == "hospitalisation" else "deaths"
        check_report(
            f"{label}, target 90%",
            100 * reduction(BASELINE_UPTAKE, 0.90, ve),
            EXPECTED_PERCENT[(key, 0.90)],
        )
        check_report(
            f"{label}, target 90%, CI low",
            100 * reduction(BASELINE_UPTAKE, 0.90, ci[0]),
            EXPECTED_PERCENT[(f"{key}_lo", 0.90)],
        )
        check_report(
            f"{label}, target 90%, CI high",
            100 * reduction(BASELINE_UPTAKE, 0.90, ci[1]),
            EXPECTED_PERCENT[(f"{key}_hi", 0.90)],
        )


def check_shares_and_mechanism() -> None:
    print("\n2. Case shares and the mechanism-stack diagnostic")

    check_report(
        "uncovered share of cases at 73.0%",
        100 * case_share_uncovered(BASELINE_UPTAKE, VE_DISEASE),
        70.6,
    )
    check_report(
        "uncovered share of cases at 90%",
        100 * case_share_uncovered(0.90, VE_DISEASE),
        41.9,
    )
    check(
        "individual effectiveness, legacy composite",
        100 * individual_effectiveness(LEGACY_COMPOSITE),
        30.1781,
        5e-4,
    )
    check(
        "individual effectiveness, composite anchored to 0.846",
        100 * individual_effectiveness(0.846),
        31.2277,
        5e-4,
    )
    check("maternal waning retention phi", PHI, 0.66359447, 1e-8)
    check("legacy composite v", LEGACY_COMPOSITE, 0.817875, 1e-12)
    check("birth exposure at 73.0%", birth_exposure(BASELINE_UPTAKE), 0.4215, 1e-12)
    check("birth exposure at 90%", birth_exposure(0.90), 0.5150, 1e-12)


def check_cross_file_consistency() -> None:
    print("\n3. Cross-file consistency of the age-structured diagnostic")

    readings = {
        row["floor"]: float(row["reduction"])
        for row in read_csv(ROOT / "data/derived/joi_reduction_readings.csv")
        if row["reading"] == "Age-structured model"
    }
    endpoint = {
        float(row["coverage_pct"]): float(row["relative_reduction_cases"])
        for row in read_csv(ROOT / "data/derived/joi_factorial_absolute.csv")
        if row["anchor"] == "Legacy mapping"
        and row["scenario"].startswith("maternal_coverage_")
    }
    for target in TARGETS:
        key = f"{int(target * 100)}%"
        if key not in readings or target * 100 not in endpoint:
            FAILURES.append(f"missing age-structured row for {key}")
            print(f"  [FAIL] age-structured target {key} row absent")
            continue
        check(
            f"ledger vs endpoint run, target {key}",
            100 * endpoint[target * 100],
            readings[key],
            1e-6,
        )

    annual = read_csv(ROOT / "data/derived/ukhsa_coverage_annual.csv")
    lookup = {row["financial_year"]: float(row["coverage_percent"]) for row in annual}
    check("England 2025-26 annual uptake", lookup["2025/26"], 73.0, 1e-12)
    check_report(
        "coverage path 2023/24 to 2025/26, cases",
        100 * reduction(lookup["2023/24"] / 100, lookup["2025/26"] / 100, VE_DISEASE),
        24.2,
    )
    check_report(
        "coverage path 2024/25 to 2025/26, cases",
        100 * reduction(lookup["2024/25"] / 100, lookup["2025/26"] / 100, VE_DISEASE),
        14.1,
    )


def main() -> int:
    print("JOI letter: verification of the reported numbers")
    print(f"repository root: {ROOT}")
    check_screening_contrast()
    check_shares_and_mechanism()
    check_cross_file_consistency()
    if FAILURES:
        print(f"\n{len(FAILURES)} check(s) failed:")
        for item in FAILURES:
            print(f"  - {item}")
        return 1
    print("\nAll checks passed. The released numbers reproduce from the released inputs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
