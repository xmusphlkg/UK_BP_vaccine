"""Build only audited letter outputs once scenario results exist."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
result=ROOT/'outputs/tables/scenario_results.csv'
if not result.exists():
    raise SystemExit('No scenario results found; do not write numerical claims into the letter.')
print('Scenario result found. Add a schema-aware renderer before publication use.')
