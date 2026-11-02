"""Sol-xhigh-prescribed,pre-registered algorithm diagnostics. Synthetic only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
from scipy.stats import binomtest
from donor_kernel import aggregate_models,bootstrap_profiles,rank_correlations
from ledger import append_record,sha256_file

ROOT=Path(__file__).resolve().parent.parent


def prepare(folder):
    spec_path=folder/'SPEC.json';spec=json.loads(spec_path.read_text())
    path=folder/'fixtures.npz'
    if path.exists():raise RuntimeError('frozen fixture arrays already exist')
    grid=np.array([(a,b,c) for a in [-1,0,1] for b in [-1,0,1] for c in range(-11,12)])
    a,b,c=grid.T;x=69*a+23*b+c;z=c.copy()
    arrays={'lability':x.astype(float),'baseline':z.astype(float)}
    targets={}
    for sid,name,sign,target in [(0,'null',-1,0.),(1,'positive',1,.6)]:
        mu=.5+(69*b+sign*23*a+c)/412
        actual=float(rank_correlations(mu,x,z)[0])
        if abs(actual-target)>1e-12:raise ValueError('analytic population fixture target mismatch')
        cases=[]
        for outer in range(spec['outer_datasets']):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],sid,outer,11]))
            U=rng.choice([-1.,1.],144)
            V=rng.choice([-1.,1.],(144,23))
            E=rng.choice([-1.,1.],(144,207))
            D=mu[:,None]+.06*(a[:,None]*U[None,:]+V[:,c+11].T+E.T)
            if D.min()<0 or D.max()>1:raise ValueError('synthetic donor contributions outside[0,1]')
            cases.append(D)
        arrays[name]=np.array(cases);arrays[name+'_mu']=mu
        targets[name]={'exact':target,'verified_numerical':actual}
    np.savez_compressed(path,**arrays)
    manifest={'status':'FROZEN_SYNTHETIC_CODE_FIXTURES_NOT_BIOLOGY','spec_sha256':sha256_file(spec_path),
        'arrays_sha256':sha256_file(path),'targets':targets,'source_proposal_sha256':sha256_file(ROOT/'reviews/uncertainty_followup_xhigh_v1.md'),
        'code_hashes':{p:sha256_file(ROOT/p) for p in spec['code_files']}}
    (folder/'fixture_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    append_record(ROOT/'ledger/experiments.jsonl',{'kind':'synthetic_fixture_freeze','artifact':str(folder/'fixture_manifest.json'),
        'sha256':sha256_file(folder/'fixture_manifest.json'),'biology_evidence':False})
    return manifest


def run(folder):
    output=folder/'results.json'
    if output.exists():raise RuntimeError('immutable calibration output exists')
    spec=json.loads((folder/'SPEC.json').read_text());manifest=json.loads((folder/'fixture_manifest.json').read_text())
    if sha256_file(folder/'fixtures.npz')!=manifest['arrays_sha256'] or sha256_file(folder/'SPEC.json')!=manifest['spec_sha256']:
        raise ValueError('frozen fixture/spec tampered')
    for name,digest in manifest['code_hashes'].items():
        if sha256_file(ROOT/name)!=digest:raise ValueError('production code changed after freeze')
    arrays=np.load(folder/'fixtures.npz');records=[];summaries={};start=time.monotonic()
    ids=[f'd{i:03d}' for i in range(144)]
    nested_ids=ids+ids[:4]
    for sid,name in enumerate(['null','positive']):
        target=manifest['targets'][name]['exact'];covered=0;valid_count=0;group_ok=True
        for outer,D in enumerate(arrays[name]):
            boot_seed=spec['seed']+10000*(sid+1)+outer
            raw=bootstrap_profiles(D,arrays['lability'],arrays['baseline'],reps=spec['bootstrap_replicates'],seed=boot_seed)
            nested=np.column_stack([D,D[:,:4]])
            grouped,donors,denominator=aggregate_models(nested,nested_ids)
            equal=np.array_equal(grouped,D) and donors==ids and denominator==1
            duplicate=bootstrap_profiles(grouped,arrays['lability'],arrays['baseline'],reps=spec['bootstrap_replicates'],seed=boot_seed)
            equal=equal and raw==duplicate
            group_ok=group_ok and equal
            valid=bool(raw['interval_valid'])
            ci=raw['ci95_donor_percentile']
            hit=bool(valid and ci[0]<=target<=ci[1]);covered+=hit;valid_count+=valid
            records.append({'fixture':name,'outer':outer,'bootstrap_seed':boot_seed,'exact_target':target,
                'covered':hit,'nested_grouping_invariant':equal,**raw})
            if (outer+1)%10==0:
                (folder/'progress.json').write_text(json.dumps({'fixture':name,'completed':outer+1,
                    'wall_s':time.monotonic()-start})+'\n')
        interval=binomtest(covered,spec['outer_datasets']).proportion_ci(confidence_level=.95,method='exact')
        passed=valid_count==spec['outer_datasets'] and covered>=spec['coverage_count_min'] and group_ok
        summaries[name]={'status':'PASS' if passed else 'FAIL','covered':covered,'total':spec['outer_datasets'],
            'valid_intervals':valid_count,'binomial_ci95':[interval.low,interval.high],
            'nested_grouping_invariant':group_ok,'exact_target':target}
    invalid={}
    invalid['constant']=bootstrap_profiles(np.full((207,144),.5),arrays['lability'],arrays['baseline'],reps=5000)['point_valid'] is False
    try:
        bad=arrays['null'][0].copy();bad[1,1]=np.inf
        bootstrap_profiles(bad,arrays['lability'],arrays['baseline'],reps=5000)
        invalid['nonfinite']=False
    except ValueError:invalid['nonfinite']=True
    usage=resource.getrusage(resource.RUSAGE_SELF)
    result={'status':'PASS' if all(s['status']=='PASS' for s in summaries.values()) and all(invalid.values()) else 'FAIL',
        'evidence_type':'algorithmic_synthetic_diagnostic_NOT_biology_NOT_coverage_certification',
        'q':None,'admissible_for_policy':False,'summaries':summaries,'invalid_fixtures':invalid,
        'records':records,'wall_s':time.monotonic()-start,'cpu_s':usage.ru_utime+usage.ru_stime,
        'peak_rss_bytes':usage.ru_maxrss,'spec_sha256':manifest['spec_sha256'],'arrays_sha256':manifest['arrays_sha256']}
    output.write_text(json.dumps(result,indent=2)+'\n')
    append_record(ROOT/'ledger/experiments.jsonl',{'kind':'synthetic_donor_bootstrap_calibration','artifact':str(output),
        'sha256':sha256_file(output),'status':result['status'],'outer_datasets':200,'bootstrap_evaluations_including_grouping':400,
        'biology_evidence':False,'q':None,'wall_s':result['wall_s'],'cpu_s':result['cpu_s'],'peak_rss_bytes':result['peak_rss_bytes']})
    return {k:v for k,v in result.items() if k!='records'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);p.add_argument('folder',type=Path)
    a=p.parse_args();result=prepare(a.folder) if a.stage=='prepare' else run(a.folder)
    print(json.dumps(result,indent=2))
    if result.get('status')=='FAIL':raise SystemExit(1)
