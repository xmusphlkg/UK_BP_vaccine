"""Fail-closed audit for the JOI letter staged inputs."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data/metadata/staged_input_manifest.json').read_text())
missing=[]; bad=[]
for row in manifest['inputs']:
    p=ROOT/row['destination']
    if row['status'] not in {'copied', 'downloaded'} or not p.exists():
        missing.append(row['destination'])
        continue
    import hashlib
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h != row['sha256']: bad.append(row['destination'])
required=['data/raw/uk_candidate_config.yaml','data/raw/maternal_coverage_processed.csv','data/raw/uk_notifications.csv']
for x in required:
    if not (ROOT/x).exists(): missing.append(x)
report={'missing':sorted(set(missing)),'hash_mismatch':bad,'status':'pass' if not missing and not bad else 'fail'}
(ROOT/'reports/input_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
sys.exit(0 if report['status']=='pass' else 1)
