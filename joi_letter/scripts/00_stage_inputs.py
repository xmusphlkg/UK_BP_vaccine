"""Re-stage selected parent-project inputs without modifying the parent project."""
from pathlib import Path
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parents[1]
MAP = {
    "data/processed/analysis_observations/United_Kingdom.csv": "data/raw/uk_notifications.csv",
    "data/processed/united_kingdom_scope_provenance.json": "data/metadata/uk_scope_provenance.json",
    "data/processed/maternal_immunization_coverage_processed.csv": "data/raw/maternal_coverage_processed.csv",
    "data/processed/official_baseline_completion_20260907/england_notifications_age.csv": "data/raw/england_notifications_age.csv",
    "data/processed/official_baseline_completion_20260907/england_notifications_annual.csv": "data/raw/england_notifications_annual.csv",
    "data/processed/official_baseline_completion_20260907/england_infant_deaths.csv": "data/raw/england_infant_deaths.csv",
    "data/processed/official_baseline_completion_20260907/ons_population_model_age.csv": "data/raw/england_population_model_age.csv",
    "data/processed/country_profile_inputs.csv": "data/raw/country_profile_inputs.csv",
    "data/processed/recovered_candidate_baselines_20261008/United_Kingdom/candidate_config.yaml": "data/raw/uk_candidate_config.yaml",
    "data/validated_surveillance_source_manifest.csv": "data/metadata/validated_surveillance_source_manifest.csv",
}

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

manifest=[]
for src_rel, dst_rel in MAP.items():
    src=PARENT/src_rel
    dst=ROOT/dst_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        manifest.append({'source':str(src_rel),'destination':str(dst_rel),'status':'missing'})
        continue
    shutil.copy2(src,dst)
    manifest.append({'source':str(src_rel),'destination':str(dst_rel),'status':'copied','bytes':dst.stat().st_size,'sha256':sha256(dst)})
(ROOT/'data/metadata/staged_input_manifest.json').write_text(json.dumps({'created':'2026-10-19','inputs':manifest},indent=2)+'\n')
print(json.dumps({'copied':sum(x['status']=='copied' for x in manifest),'missing':sum(x['status']=='missing' for x in manifest)},indent=2))
