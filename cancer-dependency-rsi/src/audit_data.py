"""Cache/provenance and metadata-only cohort audit. Never parse external outcomes."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import time
from ledger import append_record, sha256_file

ROOT=Path(__file__).resolve().parent.parent


def check_file(path:Path, entry:dict, append_only=False):
    if not path.is_file():
        return {'ok':False,'error':'missing','path':str(path)}
    expected_bytes=entry['bytes']
    actual_bytes=path.stat().st_size
    if append_only:
        # A frozen prefix pins an append-only exposure ledger; later records
        # must not make the original prefix unverifiable.
        with path.open('rb') as f:
            original=f.read(expected_bytes)
        digest=hashlib.sha256(original).hexdigest()
        size_ok=actual_bytes>=expected_bytes
    else:
        digest=sha256_file(path)
        size_ok=actual_bytes==expected_bytes
    return {'ok':size_ok and digest==entry['sha256'],'path':str(path),
            'expected_sha256':entry['sha256'],'observed_sha256':digest,
            'expected_bytes':expected_bytes,'actual_bytes':actual_bytes,'append_only_prefix':append_only}


def cohort_audit(root=ROOT):
    split=json.loads((root/'data/split_manifest.json').read_text())['C_external']
    with (root/'data/crosswalk_sanger_screened.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    errors=[]
    # Rows are library screens: dual-library models legitimately repeat.
    ids=[r['sample_ID'] for r in rows]
    keys=[(r['sample_ID'],r['library']) for r in rows]
    if len(keys)!=len(set(keys)): errors.append('duplicate sample/library keys in screened crosswalk')
    by_sample={sample:[r for r in rows if r['sample_ID']==sample] for sample in set(ids)}
    if any(len({r['individual_ID'] for r in group})!=1 for group in by_sample.values()):
        errors.append('conflicting donors within one biological model')
    if any(not r['individual_ID'] or r['individual_ID'].lower()=='nan' for r in rows):
        errors.append('unresolved donor in external screened crosswalk')
    overlap={r['individual_ID'] for r in rows if r['overlap_Broad_DepMap']=='Yes'}
    eligible=[r for r in rows if r['CRISPR_available']=='Yes' and r['individual_ID'] not in overlap]
    actual_ids={r['sample_ID'] for r in eligible}
    actual_donors={r['individual_ID'] for r in eligible}
    if actual_ids!=set(split['sample_ids']): errors.append('external sample partition differs from metadata regeneration')
    if actual_donors!=set(map(str,split['donor_ids'])): errors.append('external donor partition differs from metadata regeneration')
    if len(split['sample_ids'])!=len(set(split['sample_ids'])):errors.append('duplicate frozen external sample IDs')
    if len(split['donor_ids'])!=len(set(split['donor_ids'])):errors.append('duplicate frozen external donor IDs')
    mapping=split.get('sample_to_donor')
    actual_mapping={r['sample_ID']:r['individual_ID'] for r in eligible}
    if mapping is None or {k:str(v) for k,v in mapping.items()}!=actual_mapping:
        errors.append('explicit sample-to-donor mapping missing or inconsistent')
    if actual_donors & overlap:errors.append('Broad-overlapping donor leaked into external cohort')
    if overlap!=set(map(str,split['excluded_broad_overlap_donors'])):errors.append('excluded overlapping donor set mismatch')
    if len(actual_ids)!=split['cohort_n_models'] or len(actual_donors)!=split['cohort_n_donors']:
        errors.append('external cohort counts mismatch')
    libraries=split['library_rule']
    if set(libraries)!=actual_ids:errors.append('library rules do not exactly cover cohort')
    for sample in sorted(actual_ids):
        available={r['library'] for r in by_sample[sample]}
        expected='minLib' if 'minLib' in available else 'v1_1'
        if libraries.get(sample)!=expected:errors.append(f'library rule differs: {sample}')
    return {'ok':not errors,'errors':errors,'library_screen_rows':len(rows),'screened_models':len(set(ids)),
            'eligible_models':len(actual_ids),'eligible_donors':len(actual_donors),
            'excluded_overlap_donors':len(overlap),'outcome_values_read':False}


def audit(root=ROOT):
    start=time.monotonic();checks=[];errors=[]
    data_manifest=json.loads((root/'data/data_manifest.json').read_text())
    for name,entry in data_manifest['files'].items():
        p=root/name
        # All manifest entries are project-relative; reject path traversal.
        if not p.resolve().is_relative_to(root.resolve()):
            errors.append(f'manifest path outside project: {name}');continue
        checks.append(check_file(p,entry,append_only=name=='data/exposure_log.jsonl'))
    # Check entire byte streams only. Hashing is logged as opaque-byte access
    # before opening any external outcome container, even though no values
    # are decoded, printed, ranked or analyzed.
    for manifest,base in [('data/source_manifest_broad_figshare.json','data/raw/broad_figshare'),
                          ('data/source_manifest_sanger_figshare.json','data/raw/sanger_figshare')]:
        entries=json.loads((root/manifest).read_text())
        for entry in entries:
            file=entry['file'].replace(' (Nature MOESM3)','')
            p=root/base/file
            if not p.exists() and file=='07_EssMatrix_qnorm_corrected_logFCs.RData':
                p=root/'data/quarantine'/file
            if not p.resolve().is_relative_to(root.resolve()):
                errors.append(f'source path outside project: {file}');continue
            if not all(entry.get(k) for k in ('license','source_url','retrieved','article_version')):
                errors.append(f'incomplete source provenance: {file}')
            if base.endswith('sanger_figshare') and (p.suffix.lower() in {'.rdata','.zip'}):
                append_record(root/'data/exposure_log.jsonl',{'actor':'audit_data.py','operation':'opaque_file_checksum_only',
                    'partition':'C_quarantined','path':str(p.relative_to(root)),
                    'outcome_values_decoded':False,'purpose':'verify cached release bytes against pinned manifest'})
            checks.append(check_file(p,entry))
    cohort=cohort_audit(root)
    errors += [f'hash/size failure: {c["path"]}' for c in checks if not c['ok']]
    errors += cohort['errors']
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'file_checks':checks,
        'cohort':cohort,'wall_s':time.monotonic()-start,'outcome_values_parsed':False,
        'gate_scope':'cached provenance/metadata integrity only; does not grant G0/G2 or final independence certification'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists():raise RuntimeError('audit output exists; use a new version')
    result=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    append_record(ROOT/'ledger/experiments.jsonl',{'kind':'data_integrity_audit','artifact':str(args.output),
        'sha256':sha256_file(args.output),'status':result['status'],'wall_s':result['wall_s'],'outcome_values_parsed':False})
    print(json.dumps({k:v for k,v in result.items() if k!='file_checks'},indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)
