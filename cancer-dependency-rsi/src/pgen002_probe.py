"""pgen002 receipted metadata probe (SPEC b9c8275d... locked in ledger before first request).

Metadata only: HEAD + zip EOCD/central-directory ranges, Passports model_list import,
Sanger data-usage policy fetch, filename->model->patient metadata join. No count values.
Every request receipted (url, range, status, headers subset, bytes, sha256, wall_s).
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generations/pgen002'
ZIP_URL = 'https://cmp.cog.sanger.ac.uk/download/Project_score_raw_counts.zip'
MODEL_URL = 'https://cog.sanger.ac.uk/cmp/download/model_list_20260921.csv'
POLICY_URL = 'https://depmap.sanger.ac.uk/documentation/data-usage-policy/'
receipts = []


def fetch(url, headers=None, save=None):
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={'User-Agent': 'cd-rsi-pgen002-probe/1.0', **(headers or {})},
                                 method='HEAD' if headers and headers.get('_head') else 'GET')
    if headers:
        headers.pop('_head', None)
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read() if req.get_method() == 'GET' else b''
        rec = {'url': url, 'method': req.get_method(), 'range': req.headers.get('Range'),
               'status': r.status, 'bytes': len(body), 'wall_s': round(time.monotonic() - t0, 3),
               'sha256': hashlib.sha256(body).hexdigest() if body else None,
               'headers': {k: v for k, v in r.headers.items()
                           if k.lower() in ('content-length', 'content-type', 'last-modified', 'etag', 'accept-ranges')}}
    receipts.append(rec)
    if save and body:
        save.parent.mkdir(parents=True, exist_ok=True)
        save.write_bytes(body)
    return body, rec


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', str(s).upper())


def main() -> int:
    # 1) zip HEAD + central directory (metadata ranges only)
    _, head = fetch(ZIP_URL, {'_head': True})
    size = int(next(v for k, v in head['headers'].items() if k.lower() == 'content-length'))
    tail, _ = fetch(ZIP_URL, {'Range': f'bytes={size - 262144}-{size - 1}'})
    i = tail.rfind(b'PK\x05\x06')
    cd_size, cd_off = struct.unpack('<I', tail[i + 12:i + 16])[0], struct.unpack('<I', tail[i + 16:i + 20])[0]
    cd, _ = fetch(ZIP_URL, {'Range': f'bytes={cd_off}-{cd_off + cd_size - 1}'})
    names, p = [], 0
    while p < len(cd) - 46 and cd[p:p + 4] == b'PK\x01\x02':
        comp, uncomp = struct.unpack('<I', cd[p + 20:p + 24])[0], struct.unpack('<I', cd[p + 24:p + 28])[0]
        nl, el, cl = struct.unpack('<HHH', cd[p + 28:p + 34])
        names.append({'name': cd[p + 46:p + 46 + nl].decode('utf-8', 'replace'), 'compressed': comp, 'uncompressed': uncomp})
        p += 46 + nl + el + cl
    (OUT / 'zip_listing_v2.json').write_text(json.dumps(names, indent=1))
    files = [n for n in names if not n['name'].endswith('/')]

    # 2) license / usage policy (fetched + hashed; text retained for review)
    policy, _ = fetch(POLICY_URL, save=OUT / 'data_usage_policy_v2.html')

    # 3) Passports model_list import under data/ with manifest
    dest = ROOT / 'data/passports_model_list_20260921.csv'
    fetch(MODEL_URL, save=dest)
    (ROOT / 'data/passports_model_list_20260921_manifest.json').write_text(json.dumps(
        {'source_url': MODEL_URL, 'file': 'data/passports_model_list_20260921.csv',
         'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(), 'bytes': dest.stat().st_size,
         'retrieved_by': 'src/pgen002_probe.py', 'content_class': 'model metadata (no outcomes)'}, indent=1))

    models = pd.read_csv(dest)
    key = {}
    for _, r in models.iterrows():
        for cand in [r.get('model_name')] + str(r.get('synonyms') or '').split('|'):
            k = norm(cand)
            if k:
                key.setdefault(k, []).append(r)
    def line_key(fn):
        base = fn.split('/')[-1].replace('.read_count.tsv.gz', '')
        m = re.split(r'_[cC]9', base, maxsplit=1)
        return norm(m[0])
    linekeys = {}
    for f in files:
        linekeys.setdefault(line_key(f['name']), []).append(f['name'])
    matched, amb, unmatched = {}, [], []
    for k, fns in sorted(linekeys.items()):
        hits = key.get(k, [])
        pats = {str(h['patient_id']) for h in hits}
        if len(pats) == 1:
            matched[k] = {'patient_id': next(iter(pats)), 'files': len(fns),
                          'broad_id': sorted({str(h.get('BROAD_ID')) for h in hits})}
        elif len(pats) > 1:
            amb.append({'line_key': k, 'patients': sorted(pats), 'files': len(fns)})
        else:
            unmatched.append(k)
    # C overlap: C sample_IDs are HCM-SANG model_names in Passports space
    cohort = pd.read_csv(ROOT / 'lock_s/cohort.csv')
    by_name = {norm(n): str(p) for n, p in zip(models['model_name'], models['patient_id'])}
    c_patients = {by_name[norm(s)] for s in cohort['sample_ID'] if norm(s) in by_name}
    broad7 = {'ACH-000048', 'ACH-000108', 'ACH-000178', 'ACH-001418', 'ACH-002958', 'ACH-003040', 'ACH-003052'}
    allp = {v['patient_id'] for v in matched.values()}
    c_overlap = allp & c_patients
    exposed = {k for k, v in matched.items() if broad7 & set(v['broad_id'])}
    eligible_patients = allp - c_patients - {matched[k]['patient_id'] for k in exposed}
    out = {'zip': {'size': size, 'members': len(names), 'count_files': len(files),
                   'member_uncompressed_sum': sum(n['uncompressed'] for n in files)},
           'lines_unique_keys': len(linekeys), 'matched_lines': len(matched),
           'ambiguous_lines': amb, 'unmatched_line_keys': unmatched,
           'matched_patients': len(allp), 'c_cohort_models_mapped_to_patients': len(c_patients),
           'c_overlap_patients': sorted(c_overlap), 'broad_minipool_exposed_lines': sorted(exposed),
           'eligible_patients_after_exclusions': len(eligible_patients),
           'policy_bytes': len(policy), 'requests': receipts,
           'total_probe_bytes': sum(r['bytes'] for r in receipts), 'n_requests': len(receipts)}
    (OUT / 'probe_results_v2.json').write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ('requests', 'unmatched_line_keys', 'ambiguous_lines')}, indent=1))
    print('unmatched:', len(unmatched), 'ambiguous:', len(amb))
    return 0


if __name__ == '__main__':
    sys.exit(main())
