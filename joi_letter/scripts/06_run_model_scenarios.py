"""Run the JOI extension scenarios using the parent model as a read-only library.

All outputs are written inside manuscript/joi_letter/. The parent model code and
its outputs are not modified. This is an exploratory, uncalibrated run until the
UK-specific validation gates are passed.
"""
from __future__ import annotations
import hashlib, json, os, sys
from copy import deepcopy
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parents[1]
if str(PARENT) not in sys.path: sys.path.insert(0,str(PARENT))
from src_python.simulation.common import (
    add_relative_reductions, apply_intervention_definition, execute_scenario_list,
    load_configs, make_config,
)
from uk_structural_seasonality import apply_uk_structural_seasonality, seasonality_record

WALKER_VE_DISEASE=0.846
# Match the model's composite disease protection approximately while keeping
# its susceptibility component explicit: 1-(1-r*VE_sus)(1-r*VE_sym)=0.846.
MATERNAL_RELATIVE_EFFECT=0.75
MATERNAL_VE_SUS=0.55
WALKER_VE_SYM=(1-(1-WALKER_VE_DISEASE)/(1-MATERNAL_RELATIVE_EFFECT*MATERNAL_VE_SUS))/MATERNAL_RELATIVE_EFFECT
SCENARIO_MATERNAL_PROTECTION_DURATION=180.0


def sha256(path: Path) -> str:
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def build_scenarios(*, anchored: bool):
    cfgs=load_configs()
    overrides={
        'natural_history': {
            'maternal_protection_duration': SCENARIO_MATERNAL_PROTECTION_DURATION,
        }
    }
    if anchored:
        overrides={
            'natural_history': {
                'maternal_protection_duration': SCENARIO_MATERNAL_PROTECTION_DURATION,
            },
            'immunity_model': {
                'maternal_VE_sus': MATERNAL_VE_SUS,
                'maternal_VE_sym': WALKER_VE_SYM,
                'maternal_relative_effect': MATERNAL_RELATIVE_EFFECT,
            },
            'natural_history': {'maternal_protection_duration': 180.0},
        }
    history=apply_uk_structural_seasonality(make_config(country_profile='United_Kingdom', config_overrides=overrides, load_calibration=False))
    scenario_ve_sus = MATERNAL_VE_SUS
    scenario_ve_sym = WALKER_VE_SYM if anchored else 0.92
    scenarios=[{
        'config': deepcopy(history), 'analysis':'joi_letter_exploratory',
        'scenario':'current', 'vaccine_scenario':'symptom_protective',
        'resistance_scenario':cfgs['baseline'].get('baseline_resistance_scenario','country_timeline'),
        'intervention':'current', 'metadata':{'country':'United_Kingdom','anchored_to_walker_ve':anchored,'coverage_target':None},
    }]
    for target in (0.75,0.80,0.90):
        intervention={'maternal_coverage_min':target,
                      'vaccine_overrides':{'maternal_VE_sus':scenario_ve_sus,'maternal_VE_sym':scenario_ve_sym,'maternal_relative_effect':MATERNAL_RELATIVE_EFFECT},
                      'natural_history_overrides':{
                          'maternal_protection_duration':
                              SCENARIO_MATERNAL_PROTECTION_DURATION,
                      }}
        policy=apply_uk_structural_seasonality(make_config(country_profile='United_Kingdom', config_overrides=overrides, load_calibration=False))
        policy=apply_intervention_definition(policy, intervention, history_config=history,
            history_vaccine_scenario='symptom_protective',
            history_resistance_scenario=cfgs['baseline'].get('baseline_resistance_scenario','country_timeline'))
        scenarios.append({'config':policy,'analysis':'joi_letter_exploratory',
            'scenario':f'maternal_coverage_{int(target*100)}', 'vaccine_scenario':'symptom_protective',
            'resistance_scenario':cfgs['baseline'].get('baseline_resistance_scenario','country_timeline'),
            'intervention':f'maternal_coverage_{int(target*100)}',
            'metadata':{'country':'United_Kingdom','anchored_to_walker_ve':anchored,'coverage_target':target}})
    return scenarios


def run(anchored: bool):
    tag='walker_anchored' if anchored else 'legacy_ve'
    scenario_ve_sym = WALKER_VE_SYM if anchored else 0.92
    scenarios=build_scenarios(anchored=anchored)
    ts, summary=execute_scenario_list(scenarios, stem=f'joi_letter_{tag}', n_jobs=int(os.environ.get('JOI_N_JOBS','4')))
    summary=add_relative_reductions(summary, reference_scenario='current')
    summary['ve_anchor']=tag
    out=ROOT/'outputs'/'model_runs'/tag; out.mkdir(parents=True,exist_ok=True)
    ts.to_parquet(out/'timeseries.parquet',index=False)
    summary.to_csv(out/'summary.csv',index=False)
    metadata={'tag':tag,'anchored_to_walker_ve':anchored,
        'walker_ve_disease':WALKER_VE_DISEASE,'maternal_ve_sus':MATERNAL_VE_SUS,
        'maternal_ve_sym_scenario':scenario_ve_sym,'maternal_relative_effect':MATERNAL_RELATIVE_EFFECT,
        'maternal_protection_duration_days':SCENARIO_MATERNAL_PROTECTION_DURATION,
        'n_scenarios':len(summary),'summary_sha256':sha256(out/'summary.csv'),
        'interpretation':'Exploratory uncalibrated England-and-Wales-labelled profile; not a national forecast.',
        'structural_seasonality': seasonality_record(scenarios[0]['config']),
    }
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return summary

if __name__=='__main__':
    all_s=[]
    for anchored in (False,True):
        s=run(anchored); all_s.append(s)
        cols=['scenario','total_infant_cases','total_infant_hospitalizations','total_infant_deaths','relative_reduction_infant_cases','maternal_vaccination_coverage','maternal_birth_exposure_coverage']
        print(('WALKER' if anchored else 'LEGACY'))
        print(s[[c for c in cols if c in s.columns]].to_string(index=False))
    combined=pd.concat(all_s,ignore_index=True)
    combined.to_csv(ROOT/'outputs/tables/joi_model_scenario_summary.csv',index=False)
