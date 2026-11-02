"""Unscored Layer-A descriptive evaluator (Sol-xhigh directive,pre-Lock1).

Every result has q=null and admissible_for_policy=false. Fixed-gene point
statistics and model-composition sensitivity are not scientific intervals.
No permutation coverage diagnostic or interval-sharpness reward is computed.
"""
from __future__ import annotations
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from pydantic import ValidationError
from candidates import ScientificConfig
import estimators
from ledger import sha256_file

EVALUATOR_VERSION='evaluator_v4_unscored'
ROOT=estimators.ROOT


def evaluate(config:dict,seed=20261028):
    rec={'evaluator_version':EVALUATOR_VERSION,'config':{k:v for k,v in config.items() if k!='uses_non_layerA'},
        'q':None,'admissible_for_policy':False,'valid_scientific_inference':False,
        'descriptive_valid':False,'invalid_reasons':[],
        'data_layer':'A_only','outcome_class':'invalid_result'}
    def invalid(reason):
        rec['invalid_reasons'].append(reason);return rec
    if config.get('uses_non_layerA'):return invalid('non-Layer-A input forbidden')
    try:c=ScientificConfig.model_validate({k:v for k,v in config.items() if k!='uses_non_layerA'}).model_dump()
    except ValidationError as e:return invalid('illegal scientific config:'+str(e))
    rec['config']=c;rec['config_id']=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()[:16]
    meta,eff,ref=estimators.load_dev()
    scopes=json.loads((ROOT/'data/gene_scopes.json').read_text());genes=scopes[c['scope']];alias=scopes.get('alias_map',{})
    if len(set(genes))!=len(genes) or eff.index.has_duplicates or eff.columns.has_duplicates or ref.index.has_duplicates:
        return invalid('duplicate source/frozen identity')
    if len(genes)<50:return invalid('support n<50')
    missing=[g for g in genes if g not in eff.columns or alias.get(g,g) not in ref.index]
    if missing:return invalid('missing exact frozen members:'+','.join(missing))
    if not np.isfinite(eff.loc[:,genes].to_numpy(dtype=float)).all():return invalid('nonfinite original paired scores')
    deltas=estimators.format_pairs(meta,eff).loc[genes]
    by={}
    for col in deltas:by.setdefault(col.split('|')[0],[]).append(col)
    models=sorted(by)
    if len(models)!=6 or len(deltas.columns)!=7:return invalid('format support differs from frozen6models/7pairs')
    def L(draw):
        if c['operator']=='abs_mean_delta':
            return pd.concat([deltas[by[m]].mean(axis=1) for m in draw],axis=1).mean(axis=1).abs().to_numpy()
        agg=[deltas[by[m]].abs().max(axis=1) if c['operator']=='max_abs_delta' else deltas[by[m]].abs().mean(axis=1) for m in draw]
        return pd.concat(agg,axis=1).mean(axis=1).to_numpy()
    T=np.array([abs(float(ref.loc[alias.get(g,g),'MeanDifference'])) for g in genes])
    base=np.array([abs(float(ref.loc[alias.get(g,g),'AdherentMean'])) for g in genes])
    Z=None if c['adjust']=='none' else base[:,None]
    if c['adjust']=='base_plus_organoid_mean':
        org=np.array([abs(float(ref.loc[alias.get(g,g),'OrganoidsMean'])) for g in genes]);Z=np.column_stack([base,org])
    if not np.isfinite(T).all() or (Z is not None and not np.isfinite(Z).all()):return invalid('nonfinite original target/covariates')
    def estimate(x):
        if not np.isfinite(x).all():raise ValueError('nonfinite lability')
        if Z is not None:return estimators.partial_spearman(T,x,Z)
        rx=rankdata(x);ry=rankdata(T);rx=rx-rx.mean();ry=ry-ry.mean()
        if np.linalg.norm(rx)<=1e-12 or np.linalg.norm(ry)<=1e-12:raise ValueError('degenerate original ranks')
        return float(np.corrcoef(rx,ry)[0,1])
    try:
        point=estimate(L(models))
        lomo={m:estimate(L([x for x in models if x!=m])) for m in models}
    except ValueError as e:return invalid(str(e))
    if not np.isfinite([point,*lomo.values()]).all():return invalid('nonfinite descriptive statistic')
    rec.update({'descriptive_valid':True,'outcome_class':'descriptive_result','estimate':point,
        'n_genes':len(genes),'n_measured_models':6,'n_pairs':7,'n_verified_Broad_donors':None,
        'genes_sha256':hashlib.sha256(','.join(genes).encode()).hexdigest(),
        'lomo_points':lomo,'lomo_range':max(lomo.values())-min(lomo.values()),
        'stability_interpretation':'composition_sensitivity_only_no_population_inference',
        'scientific_interval':None,'scientific_interval_status':'not_identified_for_fixed_development_statistic',
        'seed_unused':'deterministic point/sensitivity calculations',
        'source_manifest_sha256':sha256_file(ROOT/'data/source_manifest_broad_figshare.json')})
    return rec
