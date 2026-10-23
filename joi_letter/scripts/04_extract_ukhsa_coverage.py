"""Extract the latest public UKHSA prenatal coverage tables.

The 2026 workbook contains the national England row and 42 ICB rows from
April 2023 to March 2026.  The older Q1-2024 workbook is retained as a
backward-compatible fallback for a clean checkout that has not downloaded the
newer source yet.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
latest = ROOT / "data/raw/ukhsa_prenatal_coverage_q4_2026.xlsx"
legacy = ROOT / "data/raw/ukhsa_prenatal_coverage_q1_2024.xlsx"
src = latest if latest.exists() else legacy
if not src.exists():
    raise SystemExit(f"missing {latest} (or fallback {legacy})")

if src == latest:
    raw = pd.read_excel(src, sheet_name="T2_Coverage_by_ICB", header=2)
    code_col, name_col = "ICB code", "ICB name"
else:
    raw = pd.read_excel(src, sheet_name="PertussisCoveragebyICB", header=3)
    code_col, name_col = raw.columns[:2]

raw = raw.rename(columns={code_col: "icb_code", name_col: "icb_name"})
raw["icb_code"] = raw["icb_code"].astype("string").str.strip()
raw["icb_name"] = raw["icb_name"].astype("string").str.strip()
month_cols = [c for c in raw.columns[2:] if str(c).strip()]

# The latest workbook includes an England aggregate and a denominator row.
national = raw[raw["icb_code"].str.lower().eq("england")].copy()
icb = raw[
    raw["icb_code"].notna()
    & ~raw["icb_code"].str.lower().isin(["england", "total", "nan", "denominator"])
].copy()

def to_long(frame: pd.DataFrame) -> pd.DataFrame:
    long = frame.melt(
        id_vars=["icb_code", "icb_name"],
        value_vars=month_cols,
        var_name="month",
        value_name="coverage_percent",
    )
    long["coverage_percent"] = pd.to_numeric(long["coverage_percent"], errors="coerce")
    long = long.dropna(subset=["coverage_percent"])
    long["coverage_proportion"] = long["coverage_percent"] / 100
    return long

icb_long = to_long(icb)
icb_long.to_csv(ROOT / "data/derived/ukhsa_coverage_icb_long.csv", index=False)

summary = (
    icb_long.groupby("month", as_index=False)
    .agg(
        icb_count=("icb_code", "nunique"),
        coverage_min=("coverage_percent", "min"),
        coverage_median=("coverage_percent", "median"),
        coverage_max=("coverage_percent", "max"),
    )
)
summary.to_csv(ROOT / "outputs/tables/ukhsa_coverage_monthly_summary.csv", index=False)

if not national.empty:
    national_long = to_long(national).rename(
        columns={"icb_code": "geography_code", "icb_name": "geography"}
    )
    national_long.to_csv(
        ROOT / "data/derived/ukhsa_coverage_national_monthly.csv", index=False
    )

# Values reported in the annual companion report. They are intentionally kept
# separate from monthly ICB values because annual estimates use the official
# denominator and are not reconstructed by an unweighted ICB average.
annual = pd.DataFrame(
    {
        "financial_year": ["2023/24", "2024/25", "2025/26"],
        "coverage_percent": [58.6, 65.6, 73.0],
        "source": ["UKHSA HPR 18(6)", "UKHSA HPR 19(6)", "UKHSA HPR 20(7)"],
    }
)
annual.to_csv(ROOT / "data/derived/ukhsa_coverage_annual.csv", index=False)

print(summary.tail(6).to_string(index=False))
