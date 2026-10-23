"""Validate the local JOI letter protocol and configuration without running the parent model."""
from pathlib import Path
import json, yaml

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config/letter_config.yaml'

def validate():
    cfg=yaml.safe_load(CONFIG.read_text())
    assert cfg['source_article']['doi']=='10.1016/j.jinf.2026.106836'
    targets=cfg['scenario']['maternal_coverage_targets']
    assert targets==sorted(targets) and all(0<x<1 for x in targets)
    assert cfg['scenario']['primary_endpoint']=='infant_under_3_months'
    assert cfg['scenario']['require_exact_age_boundary'] is True
    status={'status':'pass','checks':['doi','coverage_targets','endpoint_boundary']}
    (ROOT/'reports/protocol_validation.json').write_text(json.dumps(status,indent=2)+'\n')
    return status

if __name__=='__main__':
    print(json.dumps(validate(),indent=2))
