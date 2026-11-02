"""sgen008 evidence-check runner (SPEC 68869a05...).

Row-exact C10 parser with negative fixtures, eligibility recomputed from original inputs,
synthetic-audit reference validation, upstream/point/figure/OLS via retained runners.
Absent components are reported PENDING, never passed by citation.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _norm_num(s: str) -> float:
    return float(s.replace('−', '-').replace('–', '-').strip())


def parse_c10_primary(md: str) -> dict:
    """Find THE Primary decision row; return estimate + ordered interval. Raises on ambiguity."""
    rows = []
    for ln in md.splitlines():
        if not ln.strip().startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) >= 4 and cells[0].startswith('Primary') and cells[1] == 'decision':
            rows.append(cells)
    if len(rows) != 1:
        raise ValueError(f'expected exactly 1 Primary decision row, found {len(rows)}')
    cells = rows[0]
    est = _norm_num(cells[2])
    m = re.search(r'\[([^\]]+)\]', cells[3].replace('−', '-'))
    if not m:
        raise ValueError('interval bracket missing in Primary row')
    lo_s, hi_s = [x.strip() for x in m.group(1).split(',')]
    lo, hi = _norm_num(lo_s), _norm_num(hi_s)
    if not lo < hi:
        raise ValueError('interval endpoints not ordered (swapped?)')
    return {'estimate': est, 'lo': lo, 'hi': hi, 'sign_field': cells[4] if len(cells) > 4 else '',
            'magnitude_field': cells[5] if len(cells) > 5 else ''}


def check_c10(md: str, res: dict) -> bool:
    got = parse_c10_primary(md)
    exp = res['primary']
    return (abs(got['estimate'] - round(exp['estimate'], 3)) < 5e-4
            and abs(got['lo'] - round(exp['ci95_donor_percentile'][0], 3)) < 5e-4
            and abs(got['hi'] - round(exp['ci95_donor_percentile'][1], 3)) < 5e-4
            and got['sign_field'].strip().strip('*').strip().lower() == 'yes'
            and got['magnitude_field'].strip().strip('*').strip() == 'yes (BOUND)'
            and res.get('decision') == 'BOUND')


def eligibility_from_originals() -> dict:
    def norm(s):
        return re.sub(r'[^A-Z0-9]', '', str(s).upper())
    listing = json.loads((ROOT / 'generations/pgen002/zip_listing_v2.json').read_text())
    models = pd.read_csv(ROOT / 'data/passports_model_list_20260921.csv', dtype=str).fillna('')
    cohort = pd.read_csv(ROOT / 'lock_s/cohort.csv', dtype=str)
    key: dict[str, list] = {}
    for _, r in models.iterrows():
        for cand in [r['model_name']] + re.split(r'[|;]', str(r.get('synonyms') or '')):
            k = norm(cand)
            if k:
                key.setdefault(k, []).append(r)
    c_pat = set()
    for s in cohort['sample_ID']:
        pats = {str(h['patient_id']) for h in key.get(norm(s), [])}
        assert len(pats) == 1, s
        c_pat.add(next(iter(pats)))
    files = [n['name'] for n in listing if not n['name'].endswith('/')]

    def lk(fn):
        return norm(re.split(r'_[cC]9', fn.split('/')[-1].replace('.read_count.tsv.gz', ''), maxsplit=1)[0])
    linekeys: dict[str, list] = {}
    for f in files:
        linekeys.setdefault(lk(f), []).append(f)
    matched = {}
    for k in sorted(linekeys):
        hits = key.get(k, [])
        pats = {str(h['patient_id']) for h in hits}
        if len(pats) == 1:
            matched[k] = {'patient_id': next(iter(pats)),
                          'broad_id': sorted({str(h.get('BROAD_ID')) for h in hits}),
                          'files': len(linekeys[k])}
    split = json.loads((ROOT / 'data/split_manifest.json').read_text())
    broad7 = set(split['A_development']['models'])  # exposed Broad minipool models from authoritative split
    cohort_ids = list(cohort['sample_ID'])
    membership_ok = (len(cohort_ids) == len(set(cohort_ids)) == 148
                     and set(cohort_ids) == set(split['C_external']['sample_ids']))
    allp = {v['patient_id'] for v in matched.values()}
    exposed = {k for k, v in matched.items() if broad7 & set(v['broad_id'])}
    elig_p = allp - c_pat - {matched[k]['patient_id'] for k in exposed}
    elig_lines = [k for k, v in matched.items() if v['patient_id'] in elig_p]
    return {'matched_lines': len(matched), 'matched_patients': len(allp), 'c_patients': len(c_pat),
            'eligible_patients': len(elig_p), 'eligible_lines': len(elig_lines),
            'eligible_files': sum(matched[k]['files'] for k in elig_lines),
            'cohort_models': int(len(cohort)),
            'membership_ok': bool(membership_ok), 'pass': (membership_ok and len(c_pat) == 142
                     and (len(matched), len(allp), len(elig_p), len(elig_lines)) == (252, 251, 250, 251)
                     and sum(matched[k]['files'] for k in elig_lines) == 810)}


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='generations/sgen008/evidence_report_v5.json')
    out = ROOT / ap.parse_args().report
    t0 = time.monotonic()
    res = json.loads((ROOT / 'lock_s/results/external_v1.json').read_text())
    md = (ROOT / 'reviews/c10_robustness_table_v1.md').read_text()
    comps = {}
    comps['c10_row_exact'] = bool(check_c10(md, res))
    # negative fixtures must REJECT
    swapped = md.replace('[−0.175, −0.114]', '[−0.114, −0.175]', 1)
    decoy = md.replace('−0.146', '−0.999', 1) + '\nfooter decoy: −0.146 [−0.175, −0.114] BOUND\n'
    neg = {}
    neg_decision = md.replace('**yes (BOUND)**', '**no (NOT_BOUND)**', 1)
    neg_sign = md.replace('| yes | **yes (BOUND)** |', '| no | **yes (BOUND)** |', 1)
    not_exact = md.replace('**yes (BOUND)**', '**not yes (BOUND)**', 1)
    for name, bad in (('swapped_endpoints', swapped), ('footer_decoy_wrong_row', decoy),
                      ('contradictory_decision', neg_decision), ('contradictory_sign', neg_sign),
                      ('substring_decision', not_exact)):
        try:
            neg[name] = not check_c10(bad, res)
        except Exception:
            neg[name] = True
    comps['c10_negative_fixtures_rejected'] = neg
    comps['eligibility_from_originals'] = eligibility_from_originals()
    audit = json.loads((ROOT / 'generations/sgen008/synthetic_use_audit_v2.json').read_text())
    refs = [a for u in audit['mechanical_code_diagnostics'] for a in u['artifacts']]
    comps['synthetic_audit_refs_exist'] = {r: (ROOT / r.rstrip('/')).exists() for r in refs}
    comps['absent_pending'] = {'donor_patient_interval': 'PENDING (no retained arrays; outcome re-access not performed)',
                               'policy_comparison': 'ABSENT (no cycle run)'}
    ok = (comps['c10_row_exact'] and all(neg.values())
          and comps['eligibility_from_originals']['pass']
          and all(comps['synthetic_audit_refs_exist'].values()))
    report = {'components': comps, 'implemented_pass': bool(ok), 'wall_s': round(time.monotonic() - t0, 2),
              'note': 'This runner covers C10 row-exactness, eligibility-from-originals, synthetic-audit validation ONLY. Upstream/point/figure/OLS are executed by sgen005/sgen002 runners; fresh-env battery evidence is recorded in fresh_env_evidence_v2.json.'}
    with open(out, 'x') as fh:
        fh.write(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
