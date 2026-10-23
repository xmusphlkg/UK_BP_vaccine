"""Placeholder-safe scenario entry point.

The full model adapter is intentionally not silently inferred from the parent project.
Use --dry-run to verify paths; implement the exact `<3 months` mapping before running.
"""
from pathlib import Path
import argparse, json
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('--dry-run',action='store_true'); args=p.parse_args()
required=[ROOT/'data/raw/uk_candidate_config.yaml',ROOT/'data/raw/maternal_coverage_processed.csv']
missing=[str(x.relative_to(ROOT)) for x in required if not x.exists()]
result={'dry_run':args.dry_run,'required_inputs':len(required)-len(missing),'missing':missing,'status':'ready_for_adapter' if not missing else 'blocked_missing_input'}
(ROOT/'reports/scenario_runner_status.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not args.dry_run and not missing:
    raise SystemExit('Scenario adapter not yet implemented: verify age boundary and VE mapping first.')
