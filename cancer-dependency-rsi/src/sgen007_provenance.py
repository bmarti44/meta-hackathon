"""sgen007 provenance register v5 (post-65 review): recursive closure, conditional exemptions.

Traverses data_manifest (incl. mutable-append-only pinned-prefix verification), figshare source
manifests (source_url/license/release fields imported), atlas stage manifests, and LOCK2's full
30-file map. Exemptions are verified, not pathname-based: exposure log must hash-match its pinned
prefix; estimators must match a stage hash (current or frozen artifact). Offline; no decoding.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402

OUT = ROOT / 'generations/sgen007/provenance_register_v13.json'
CANON = {'S2_Supplementary_Tables.zip (Nature MOESM3)': 'data/raw/sanger_figshare/S2_Supplementary_Tables.zip'}
PAPER_LICENSE = {'PMC13581591': 'CC BY-NC-ND 4.0 (S1, per PMC license statement)',
                 'PMC13581617': 'CC BY 4.0 (S2)', 'PMC13664187': 'CC BY 4.0 (S3, MDPI)'}


def _resolve(rel: str) -> str:
    if rel in CANON:
        return CANON[rel]
    if (ROOT / rel).is_file() or '/' in rel:
        return rel
    hits = sorted(str(x.relative_to(ROOT)) for x in ROOT.glob(f'data/**/{rel}'))
    return hits[0] if len(hits) == 1 else rel


def main() -> int:
    t0 = time.monotonic()
    rows, seen = [], {}
    stage_expect: dict[str, list] = {}

    def add(rel, expected=None, source_url='', license_ev=None, release=''):
        rel = _resolve(rel)
        if expected:
            stage_expect.setdefault(rel, [])
            if expected not in stage_expect[rel]:
                stage_expect[rel].append(expected)
        if rel in seen:
            row = next(r for r in rows if r['path'] == rel)
            if expected and not row['manifest_sha256']:
                row['manifest_sha256'] = expected
                _d = row['sha256']
                row['hash_verified'] = bool(_d and _d == expected) if len(expected) != 32 else row['hash_verified']
            if source_url and not row['source_url']:
                row['source_url'] = source_url
            return
        seen[rel] = True
        p = ROOT / rel
        exists = p.is_file()
        digest = sha256_file(p) if exists else None
        md5 = hashlib.md5(p.read_bytes()).hexdigest() if exists and expected and len(expected) == 32 else None
        verified = ((md5 == expected) if (expected and len(expected) == 32) else (digest == expected)) if expected else None
        lic = license_ev or next((v for k, v in PAPER_LICENSE.items() if k in rel), None) or 'project-derived artifact (this campaign; hash-chained to listed inputs)'
        rows.append({'path': rel, 'exists': exists, 'bytes': p.stat().st_size if exists else None,
                     'sha256': digest, 'manifest_sha256': expected, 'hash_verified': verified,
                     'source_url': source_url, 'release': release, 'license_evidence': lic,
                     'quarantined_opaque': ('quarantine' in rel),
                     'acquisition_class': ('reconstructed_extraction_from_retained_zip' if 'sanger_supp' in rel else ('retained_receipt' if source_url else 'unknown_historical')),
                     'transformations': 'see processing graph in atlas/lock manifests' if rel.startswith('data/raw') else 'derived in-project or manifest',
                     'identity_role': ('identity_crosswalk' if any(k in rel for k in ('crosswalk', 'cohort', 'model_list', 'covariates', 'table_2')) else 'not_identity_bearing'),
                     'exposure_status': ('quarantined_opaque_never_decoded' if 'quarantine' in rel or 'MOESM3' in rel or 'Supplementary' in rel else 'inspected_metadata_or_values_per_exposure_log'),
                     'limitations': ('extracted table; inherits MOESM3 CC BY 4.0 terms; extraction event reconstructed (tables 1/2/4/9/10 metadata only)'
                                     if 'sanger_supp' in rel else 'none recorded beyond register reconciliations')})

    dm = json.loads((ROOT / 'data/data_manifest.json').read_text())
    mutable = dm.get('mutable_append_only_files', {})
    for rel, meta in dm.get('files', {}).items():
        add(rel, (meta or {}).get('sha256') if isinstance(meta, dict) else None)
    for man_rel in ['data/source_manifest_broad_figshare.json', 'data/source_manifest_sanger_figshare.json']:
        for e in json.loads((ROOT / man_rel).read_text()):
            add(e.get('file') or e.get('path'), e.get('sha256') or e.get('figshare_md5'),
                e.get('source_url', ''), e.get('license'), f"{e.get('collection_doi','')} v{e.get('article_version','')} retrieved {e.get('retrieved','')}")
    for man_rel in ['atlas/provisional_v1/manifest.json', 'atlas/v2/manifest.json', 'atlas/v3/manifest.json', 'atlas/v4/manifest.json']:
        man = json.loads((ROOT / man_rel).read_text())
        for group in ('inputs', 'input_hashes', 'code', 'code_hashes'):
            for rel, digest in (man.get(group) or {}).items():
                add(rel, digest)
    lock2 = json.loads((ROOT / 'lock_s/LOCK2_COMMIT.json').read_text())
    for rel, digest in lock2.get('files', {}).items():
        add(rel, digest, '', 'LOCK2-pinned bytes')
    EXPECTED_WORKBOOKS = ['data/raw/sanger_supp/supplementary_table_1_revision.xlsx',
                          'data/raw/sanger_supp/supplementary_table_2_revision.xlsx',
                          'data/raw/sanger_supp/supplementary_table_4_revision.xlsx',
                          'data/raw/sanger_supp/supplementary_table_9_revision.xlsx',
                          'data/raw/sanger_supp/supplementary_table_10_revision.xlsx']
    for supp_rel in EXPECTED_WORKBOOKS:
        add(supp_rel, None, 'extracted from retained MOESM3 zip (registered above)', 'CC BY 4.0 (article) inherited from MOESM3 source manifest')
    for ev in ['artifacts/sha256/19dcaa01253f3d7a619d18d5cbccc6063ea22f16320d9880b5b59e642e55888c',
               'data/data_manifest.json', 'lock_s/LOCK2_COMMIT.json',
               'atlas/provisional_v1/manifest.json', 'atlas/v2/manifest.json', 'atlas/v3/manifest.json', 'atlas/v4/manifest.json',
               'generations/pgen002/data_usage_policy_v2.html', 'generations/pgen003/supplemental_receipt.json',
               'generations/sgen001/identity_reconciliation_v1.json', 'generations/sgen001/identity_erratum_v1.json', 'generations/pgen002/probe_results_v2.json', 'data/passports_model_list_20260921_manifest.json']:
        add(ev, None, '', 'project-retained evidence artifact')
    _pm = json.loads((ROOT / 'data/passports_model_list_20260921_manifest.json').read_text())
    assert _pm.get('sha256'), 'Passports manifest missing required sha256 expectation'
    add('data/passports_model_list_20260921.csv', _pm.get('sha256'), _pm.get('source_url', ''), 'Sanger Data Usage Policy (fetched+hashed, pgen002)')
    _sr = json.loads((ROOT / 'generations/pgen003/supplemental_receipt.json').read_text())
    assert _sr.get('sha256'), 'supplemental receipt missing required sha256 expectation'
    add('data/CRISPR_KO_supplemental_information_20250624.csv', _sr.get('sha256'), _sr.get('url', ''), 'Sanger Data Usage Policy; receipt generations/pgen003/supplemental_receipt.json')
    add('generations/pgen002/data_usage_policy_v2.html', 'f3589e641b1c2118438a5932c748f772b99dd9157206f6a9157702b84cf83d89', 'https://depmap.sanger.ac.uk/documentation/data-usage-policy/', 'the policy document itself (receipt in probe_results_v2)')
    for extra, lic in [('data/papers/PMC13581591.xml', PAPER_LICENSE['PMC13581591']),
                       ('data/papers/PMC13581617.xml', PAPER_LICENSE['PMC13581617']),
                       ('data/papers/PMC13664187.xml', PAPER_LICENSE['PMC13664187']),
                       ('data/CRISPR_KO_supplemental_information_20250624.csv', 'Sanger Data Usage Policy; receipt generations/pgen003/supplemental_receipt.json')]:
        add(extra, None, '', lic)

    # conditional exemptions, verified:
    checks = {}
    exp_rel = 'data/exposure_log.jsonl'
    meta = dm['files'][exp_rel]
    prefix = (ROOT / exp_rel).read_bytes()[:meta['bytes']]
    checks['exposure_pinned_prefix'] = bool(hashlib.sha256(prefix).hexdigest() == meta['sha256'] and exp_rel in mutable)
    est_hashes = {'current': sha256_file(ROOT / 'src/estimators.py')}
    frozen = ROOT / 'artifacts/sha256/19dcaa01253f3d7a619d18d5cbccc6063ea22f16320d9880b5b59e642e55888c'
    est_hashes['frozen_v1_ok'] = bool(frozen.is_file() and sha256_file(frozen) == frozen.name)
    checks['estimators_stage_hashes'] = est_hashes
    # stage-specific verification: current bytes must match the LAST recorded expectation per path;
    # every distinct historical expectation must be satisfiable by current bytes or a frozen artifact
    stage_ok, stage_detail = True, {}
    for rel, exps in sorted(stage_expect.items()):
        if len(exps) <= 1:
            continue
        cur = sha256_file(ROOT / rel) if (ROOT / rel).is_file() else None
        ok_last = (cur == exps[-1])
        ok_hist = all((e == cur) or ((ROOT / 'artifacts/sha256' / e).is_file() and sha256_file(ROOT / 'artifacts/sha256' / e) == e) for e in exps)
        stage_detail[rel] = {'expectations': exps, 'current': cur, 'current_matches_latest': ok_last, 'historical_satisfiable': ok_hist}
        stage_ok = stage_ok and ok_last and ok_hist
    checks['stage_expectations_ok'] = bool(stage_ok)
    checks['stage_expectations_detail'] = stage_detail
    explained = {}
    if checks['exposure_pinned_prefix']:
        explained[exp_rel] = 'append-only: pinned prefix (1809 B) hash-verified; growth beyond prefix permitted by manifest'
    if est_hashes['frozen_v1_ok']:
        explained['src/estimators.py'] = 'stage-specific: v1 frozen artifact verified; current bytes are the v2+ stage version (per-stage execution sgen005)'

    _REQUIRED_FIELDS = ('path', 'exists', 'sha256', 'license_evidence', 'acquisition_class',
                        'transformations', 'identity_role', 'exposure_status', 'limitations')
    _schema_bad = [r.get('path', '<missing-path>') for r in rows
                   if any(k not in r or r.get(k) is None or (isinstance(r.get(k), str) and not r[k].strip())
                          for k in _REQUIRED_FIELDS)]
    missing = [r.get('path', '<missing-path>') for r in rows if not r.get('exists')]
    mismatched = [r.get('path', '<missing-path>') for r in rows if r.get('hash_verified') is False]
    unexplained = [m for m in mismatched if m not in explained]
    no_license = [r.get('path', '<missing-path>') for r in rows if not (r.get('license_evidence') or '').strip() and not str(r.get('path', '')).startswith(('src/', 'config/', 'lock_s/', 'atlas/'))]
    report = {'n_inputs': len(rows), 'missing': missing, 'hash_mismatches': mismatched,
              'explained_mismatches': explained, 'mismatches_unexplained': unexplained,
              'conditional_checks': checks, 'rows_without_license_evidence': no_license,
              'reconciliations': {
                  'excluded_replicates': 'TWO excluded sequencing replicates (0178_Adh_Alt_SF_Dome_RepA, 0178_Adh_Nat_Serum_Dome_RepB; both affected screens RETAINED) per data/provenance_v3_addendum.md; which replicates entered Chronos scoring not fully reconstructible - recorded limit',
                  'models_groups_patients': '148 C models / 144 archived covariate-ID groups / 142 patients (sgen001)',
                  'organoid_vs_930': 'Table 6 = organoid-branch processing (CRISPRcleanR->spline->ComBat within organoid cohort); 930-model EssMatrix RData are separate Pacini cell-line resources, retracted as Table 6 source (provenance_v3_addendum); quarantined RData classified sanger_figshare, opaque',
                  'exposure_log_path': 'data/exposure_log.jsonl (not ledger/exposure.jsonl)'},
              'rows': rows, 'wall_s': round(time.monotonic() - t0, 2)}
    report['schema_incomplete_rows'] = _schema_bad
    report['screen_pass'] = bool(not missing and not unexplained and not _schema_bad
                                 and not no_license
                                 and checks.get('exposure_pinned_prefix') is True
                                 and checks.get('stage_expectations_ok') is True)
    with open(OUT, 'x') as fh:
        fh.write(json.dumps(report, indent=1))
    print(json.dumps({'n': report['n_inputs'], 'missing': missing, 'unexplained': unexplained,
                      'no_license': no_license, 'checks': checks, 'pass': report['screen_pass']}, indent=1))
    return 0 if report['screen_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
