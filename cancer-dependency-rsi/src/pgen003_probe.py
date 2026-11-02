"""pgen003 receipted probe (SPEC 28d9a3fb... ledger-locked before requests).

Witness A: full C patient mapping via model_list_20260921 model_name+synonyms join.
Witness B: Passports API pagination (all models, names aliases) joined to csv patient_id by SIDM,
applied to pgen002's 108 unmatched filename line keys. Metadata only; every request receipted.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generations/pgen003'
API = 'https://api.cellmodelpassports.sanger.ac.uk/models'
receipts = []


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', str(s).upper())


def get(url):
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={'User-Agent': 'cd-rsi-pgen003-probe/1.0',
                                                'Accept': 'application/vnd.api+json'})
    with urllib.request.urlopen(req, timeout=90) as r:
        body = r.read()
        receipts.append({'url': url, 'status': r.status, 'bytes': len(body),
                         'sha256': hashlib.sha256(body).hexdigest(), 'wall_s': round(time.monotonic() - t0, 3)})
    return json.loads(body)


def main() -> int:
    models = pd.read_csv(ROOT / 'data/passports_model_list_20260921.csv')
    sidm_patient = {str(i): str(p) for i, p in zip(models['model_id'], models['patient_id'])}
    sidm_broad = {}
    if 'BROAD_ID' in models.columns:
        sidm_broad = {str(i): str(b) for i, b in zip(models['model_id'], models['BROAD_ID'])}

    # Witness A: C mapping via csv names+synonyms (local, no requests)
    key = {}
    for _, r in models.iterrows():
        for cand in [r['model_name']] + re.split(r'[|;]', str(r.get('synonyms') or '')):
            k = norm(cand)
            if k:
                key.setdefault(k, set()).add(str(r['patient_id']))
    cohort = pd.read_csv(ROOT / 'lock_s/cohort.csv')
    c_res, c_unres, c_multi = {}, [], []
    for s in cohort['sample_ID']:
        pats = key.get(norm(s), set())
        if len(pats) == 1:
            c_res[s] = next(iter(pats))
        elif len(pats) > 1:
            c_multi.append(s)
        else:
            c_unres.append(s)
    c_patients = set(c_res.values())

    # Witness B: API alias harvest (paginated; sparse names only if supported by payload size)
    alias = {}
    page, total = 1, None
    while total is None or len(alias) >= 0:
        q = urllib.parse.urlencode({'page[size]': 100, 'page[number]': page})
        d = get(f'{API}?{q}')
        if total is None:
            total = d.get('meta', {}).get('count')
        data = d.get('data', [])
        if not data:
            break
        for rec in data:
            for nm in rec.get('attributes', {}).get('names', []) or []:
                alias.setdefault(norm(nm), set()).add(rec['id'])
        if page * 100 >= (total or 0):
            break
        page += 1

    p2 = json.loads((ROOT / 'generations/pgen002/probe_results_v2.json').read_text())
    unmatched = p2['unmatched_line_keys']
    resolved, amb, still = {}, [], []
    for k in unmatched:
        sids = alias.get(k, set())
        pats = {sidm_patient[s] for s in sids if s in sidm_patient}
        if len(pats) == 1:
            resolved[k] = {'patient_id': next(iter(pats)), 'sidm': sorted(sids),
                            'broad_id': sorted({sidm_broad.get(s, '') for s in sids})}
        elif len(pats) > 1:
            amb.append({'line_key': k, 'patients': sorted(pats)})
        else:
            still.append(k)

    # Recompute eligibility: pgen002 matched (251 patients) + newly resolved, minus FULL C set + Broad7
    broad7 = {'ACH-000048', 'ACH-000108', 'ACH-000178', 'ACH-001418', 'ACH-002958', 'ACH-003040', 'ACH-003052'}
    new_pats = {v['patient_id'] for v in resolved.values()}
    new_overlap = new_pats & c_patients
    new_exposed = {k for k, v in resolved.items() if broad7 & set(v['broad_id'])}
    out = {'witness_A': {'c_models': len(cohort), 'resolved': len(c_res), 'unresolved': c_unres,
                         'multi_patient': c_multi, 'unique_c_patients_passports': len(c_patients),
                         'note': 'source donor_ID space counts 144 donors; Passports patient space = 142 (142 vs 144 discrepancy disclosed; exclusion uses Passports space, the join space for raw lines)'},
           'witness_B': {'api_models_meta_count': total, 'alias_keys': len(alias),
                         'previously_unmatched': len(unmatched), 'resolved': len(resolved),
                         'ambiguous_excluded': amb, 'still_unresolved': still,
                         'resolved_detail': resolved},
           'recomputed': {'pgen002_matched_patients': p2['matched_patients'],
                          'new_patients': len(new_pats), 'new_c_overlap_patients': sorted(new_overlap),
                          'new_broad_exposed_lines': sorted(new_exposed)},
           'requests': receipts, 'n_requests': len(receipts),
           'total_probe_bytes': sum(r['bytes'] for r in receipts)}
    (OUT / 'probe_results_v1.json').write_text(json.dumps(out, indent=1))
    print(json.dumps({'A': out['witness_A'], 'B_counts': {k: out['witness_B'][k] for k in
          ('api_models_meta_count', 'alias_keys', 'previously_unmatched', 'resolved')},
          'still': len(still), 'amb': len(amb), 'recomputed': out['recomputed'],
          'n_requests': out['n_requests'], 'bytes': out['total_probe_bytes']}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
