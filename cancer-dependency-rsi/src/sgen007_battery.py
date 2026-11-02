"""sgen007 battery: install provenance-register closure into an empty dir; verify from it alone."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402


def main() -> int:
    reg = json.loads((ROOT / 'generations/sgen007/provenance_register_v13.json').read_text())
    assert reg['screen_pass']
    paths = [r['path'] for r in reg['rows']]
    assert len(paths) == len(set(paths)), 'duplicate register rows'
    assert all(r['exists'] for r in reg['rows']), 'register row marked nonexistent'
    # independently derived required set: LOCK2 file map + figshare source-manifest files, read from project (not register)
    _lk = json.loads((ROOT / 'lock_s/LOCK2_COMMIT.json').read_text())
    REQUIRED = set(_lk.get('files', {}))
    for _mf in ('data/source_manifest_broad_figshare.json', 'data/source_manifest_sanger_figshare.json'):
        for _e in json.loads((ROOT / _mf).read_text()):
            if _e.get('file'):
                REQUIRED.add(_e['file'])
    _canon = {'S2_Supplementary_Tables.zip (Nature MOESM3)': 'data/raw/sanger_figshare/S2_Supplementary_Tables.zip'}
    REQUIRED = {_canon.get(x, x) for x in REQUIRED}
    def _res(x):
        if (ROOT / x).is_file() or '/' in x: return x
        hits = sorted(str(h.relative_to(ROOT)) for h in ROOT.glob(f'data/**/{x}'))
        return hits[0] if len(hits) == 1 else x
    REQUIRED = {_res(x) for x in REQUIRED}
    REQUIRED.add('data/raw/sanger_figshare/S2_Supplementary_Tables.zip')
    _dm = json.loads((ROOT / 'data/data_manifest.json').read_text())
    REQUIRED |= set((_dm.get('files') or {}).keys())
    REQUIRED |= {'data/raw/sanger_supp/supplementary_table_1_revision.xlsx', 'data/raw/sanger_supp/supplementary_table_2_revision.xlsx', 'data/raw/sanger_supp/supplementary_table_4_revision.xlsx', 'data/raw/sanger_supp/supplementary_table_9_revision.xlsx', 'data/raw/sanger_supp/supplementary_table_10_revision.xlsx'}
    REQUIRED |= {'data/papers/PMC13581591.xml', 'data/papers/PMC13581617.xml', 'data/papers/PMC13664187.xml'}
    for _mp in ('atlas/provisional_v1/manifest.json', 'atlas/v2/manifest.json', 'atlas/v3/manifest.json', 'atlas/v4/manifest.json'):
        _man = json.loads((ROOT / _mp).read_text())
        REQUIRED.add(_mp)
        for _g in ('inputs', 'input_hashes', 'code', 'code_hashes'):
            REQUIRED |= set((_man.get(_g) or {}).keys())
    REQUIRED |= {'lock_s/LOCK2_COMMIT.json', 'artifacts/sha256/19dcaa01253f3d7a619d18d5cbccc6063ea22f16320d9880b5b59e642e55888c',
                 'data/CRISPR_KO_supplemental_information_20250624.csv', 'src/build_atlas_v3.py',
                 'data/source_manifest_broad_figshare.json', 'data/source_manifest_sanger_figshare.json',
                 'atlas/v3/manifest.json', 'data/exposure_log.jsonl',
                 'generations/pgen002/data_usage_policy_v2.html', 'generations/pgen002/probe_results_v2.json',
                 'generations/pgen003/supplemental_receipt.json', 'generations/sgen001/identity_reconciliation_v1.json',
                 'generations/sgen001/identity_erratum_v1.json', 'data/passports_model_list_20260921_manifest.json',
                 'atlas/provisional_v1/manifest.json', 'atlas/v2/manifest.json', 'atlas/v4/manifest.json',
                 'data/data_manifest.json'}
    assert REQUIRED <= set(paths), f'independent required closure missing from register: {sorted(REQUIRED - set(paths))}'
    with tempfile.TemporaryDirectory(prefix='cdrsi-sgen007-') as td:
        clean = Path(td)
        n_ok = 0
        for row in reg['rows']:
            if not row['exists']:
                continue
            dst = clean / row['path']
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row['path'], dst)
            assert sha256_file(dst) == row['sha256'], row['path']
            n_ok += 1
        # metadata counts from the installed copy only
        lib = pd.read_csv(clean / 'data/raw/broad_figshare/minipool_library_composition.csv')
        panel = int((lib['All test genes'] == True).sum())  # noqa: E712
        cov = pd.read_csv(clean / 'data/raw/sanger_figshare/data_covariates_ALL-organoids.csv')
        cohort = pd.read_csv(clean / 'lock_s/cohort.csv', dtype=str)
        # 142-patient join + library selection, from installed files only
        import re as _re
        def _norm(s): return _re.sub(r'[^A-Z0-9]', '', str(s).upper())
        _ml = pd.read_csv(clean / 'data/passports_model_list_20260921.csv', dtype=str).fillna('')
        _key = {}
        for _, r in _ml.iterrows():
            for cand in [r['model_name']] + _re.split(r'[|;]', str(r.get('synonyms') or '')):
                k = _norm(cand)
                if k: _key.setdefault(k, set()).add(str(r['patient_id']))
        _per = {}
        for s in cohort['sample_ID']:
            _hits = {h for h in _key.get(_norm(s), set()) if h.strip()}
            assert len(_hits) == 1, f'cohort model without exactly one nonempty patient: {s} -> {_hits}'
            _per[s] = next(iter(_hits))
        _pats = set(_per.values())
        _libsel = cohort['library_primary'].value_counts().to_dict()
        _split = json.loads((clean / 'data/split_manifest.json').read_text())['C_external']
        _lib_ok = all(cohort.set_index('sample_ID').loc[s, 'library_primary'] == _split['library_rule'][s] for s in cohort['sample_ID'])
        _donor_ok = all(str(cohort.set_index('sample_ID').loc[s, 'donor_ID']) == str(_split['sample_to_donor'][s]) for s in cohort['sample_ID'])
        checks = {'installed_files_hash_verified': n_ok,
                  'register_rows_existing': sum(1 for r in reg['rows'] if r['exists']),
                  'exact_installation': bool(n_ok == sum(1 for r in reg['rows'] if r['exists'])),
                  'panel_test_genes': panel,
                  'sanger_covariate_rows': int(len(cov)),
                  'cohort_models': int(len(cohort)) if cohort is not None else None,
                  'cohort_archived_groups': int(cohort['donor_ID'].nunique()),
                  'patients_joined_installed': len(_pats), 'library_selection': {k: int(v) for k, v in _libsel.items()}, 'library_per_model_matches_locked_rule': bool(_lib_ok), 'donor_per_model_matches_locked_split': bool(_donor_ok)}
        checks['moesm3_installed'] = bool((clean / 'data/raw/sanger_figshare/S2_Supplementary_Tables.zip').exists())
        checks['pass'] = bool(checks['exact_installation'] and panel == 250
                              and checks['cohort_models'] == 148 and checks['cohort_archived_groups'] == 144
                              and len(_pats) == 142 and _lib_ok and _donor_ok)
    checks['note'] = (f"Installed {checks['installed_files_hash_verified']} unique register files byte-identically "
                      f"(incl. MOESM3 zip installed={checks['moesm3_installed']} as opaque bytes); "
                      'counts/joins computed from installed files only; outcome archives copied+hashed, not decoded')
    out = ROOT / 'generations/sgen007/cache_install_battery_v10.json'
    with open(out, 'x') as fh:
        fh.write(json.dumps(checks, indent=1))
    print(json.dumps(checks, indent=1))
    return 0 if checks['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
