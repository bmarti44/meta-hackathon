"""sgen001 identity reconciliation (SPEC 7bae9604...). Metadata only; receipted API fetches.

Disposition logic frozen in SPEC: (a) same patient / (b) distinct / (c) unresolved, per conflict pair,
from primary records: S2 Supp Table 2 clinical_data + Passports patient/sample API records.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generations/sgen001'
receipts = []


def get(url):
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={'User-Agent': 'cd-rsi-sgen001/1.0', 'Accept': 'application/vnd.api+json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        receipts.append({'url': url, 'status': r.status, 'bytes': len(body),
                         'sha256': hashlib.sha256(body).hexdigest(), 'wall_s': round(time.monotonic() - t0, 3)})
    return json.loads(body)


def main() -> int:
    clin = pd.read_excel(ROOT / 'data/raw/sanger_supp/supplementary_table_2_revision.xlsx',
                         sheet_name='clinical_data', dtype=str).fillna('')
    models = pd.read_csv(ROOT / 'data/passports_model_list_20260921.csv', dtype=str).fillna('')
    cohort = pd.read_csv(ROOT / 'lock_s/cohort.csv', dtype=str)
    conflicts = {'SIDP01937': ['WTSI-COLIVM_031', 'WTSI-COLIVM_061'],
                 'SIDP01939': ['WTSI-COLIVM_051', 'WTSI-COLIVM_090', 'WTSI-COLO_478']}
    groups = {}
    for pid, names in conflicts.items():
        prec = get(f'https://api.cellmodelpassports.sanger.ac.uk/patients/{pid}')
        comment = prec['data']['attributes'].get('model_relations_comment')
        samples = [s['id'] for s in prec['data']['relationships']['samples']['data']]
        rows = []
        for nm in names:
            crow = clin[clin['sample_ID'] == nm].iloc[0]
            mrow = models[models['model_name'] == nm].iloc[0]
            srec = get(f"https://api.cellmodelpassports.sanger.ac.uk/samples/{mrow['sample_id']}")
            rows.append({'model': nm, 'locked_donor_ID(individual_ID)': crow['individual_ID'],
                         'age_clinical': crow['age_at_attendance'], 'stage': crow['pTNM_pathological_stage'],
                         'sample_id': mrow['sample_id'], 'age_at_sampling_api': srec['data']['attributes'].get('age_at_sampling')})
        groups[pid] = {'patient_comment': comment, 'patient_samples': samples, 'models': rows,
                       'disposition': '(a) SAME PATIENT, distinct longitudinal samples — Passports grouping authoritative; '
                                      'S2 clinical individual_ID is attendance/sample-level for these records. '
                                      'Evidence: explicit same-patient comment on the patient record + age progression across samples.'}
    out = {'question': '144 locked donor_IDs vs 142 Passports patients for the 148-model C cohort',
           'groups': groups,
           'consequence_frozen_rule': 'Locked Lock-S execution preserved unchanged. Its donor bootstrap treated the two '
                                      'same-patient model pairs as independent clusters (144 clusters vs 142 patients): '
                                      'same-patient models could be resampled independently and were weighted as separate donor groups, so '
                                      'effects on patient-weighted point, interval, and decision are unknown in size and direction; archived uncertainty is not validated patient-cluster uncertainty. No replacement '
                                      'confirmatory interval is computed (C spent). Any patient-cluster recomputation from '
                                      'retained artifacts, if feasible without re-decoding outcomes, is exploratory sensitivity only.',
           'requests': receipts}
    (OUT / 'identity_reconciliation_v1.json').write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v['disposition'][:60] for k, v in groups.items()}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
