"""sgen005 upstream atlas reproduction: v1 -> v2 -> v3 -> v4 in an isolated copy.

Copies manifest-hashed inputs/code (frozen artifacts/sha256 bytes where current code
differs from a stage manifest - substitutions recorded), runs each retained builder,
compares every stage's CSVs byte-for-byte with retained outputs. The builders hardcode
their output dirs, so the isolated copy is a miniature project tree.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402

STAGES = [  # (label, builder, manifest, retained_dir)
    ('v1', 'src/build_atlas.py', 'atlas/provisional_v1/manifest.json', 'atlas/provisional_v1'),
    ('v2', 'src/build_atlas_v2.py', 'atlas/v2/manifest.json', 'atlas/v2'),
    ('v3', 'src/build_atlas_v3.py', 'atlas/v3/manifest.json', 'atlas/v3'),
    ('v4', 'src/build_atlas_v4.py', 'atlas/v4/manifest.json', 'atlas/v4'),
]


def _copy(clean: Path, rel: str, digest: str | None, subs: list):
    src = ROOT / rel
    if digest is not None and (not src.exists() or sha256_file(src) != digest):
        frozen = ROOT / 'artifacts/sha256' / digest
        if not frozen.is_file() or sha256_file(frozen) != digest:
            raise RuntimeError(f'no verified frozen bytes for changed input/code: {rel}')
        subs.append({'path': rel, 'frozen_sha256': digest})
        src = frozen
    dst = clean / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--report', default='generations/sgen005/upstream_reproduction_v5.json')
    out_path = ROOT / ap.parse_args().report
    t0 = time.monotonic()
    subs, stage_results = [], {}
    with tempfile.TemporaryDirectory(prefix='cdrsi-sgen005-') as td:
        clean = Path(td)
        # dependency closure: all manifests' inputs+code, ledger, builders, retained lock outputs
        manifests = {label: json.loads((ROOT / m).read_text()) for label, _, m, _ in STAGES}
        wanted: dict[str, str | None] = {}
        for label, man in manifests.items():
            for group in ('inputs', 'input_hashes', 'code', 'code_hashes'):
                for rel, digest in (man.get(group) or {}).items():
                    wanted[rel] = digest
        for extra in ['src/ledger.py', 'src/estimators.py', 'src/build_atlas_v2.py', 'src/build_atlas_v3.py',
                      'src/build_atlas_v4.py', 'lock_s/results/external_v1.json',
                      'lock_s/results/external_v1_gene_displacement.csv',
                      'data/raw/broad_figshare/minipool_growth_format_tests.csv',
                      'data/raw/broad_figshare/minipool_serum_status_tests.csv',
                      'atlas/v3/manifest.json']:
            wanted.setdefault(extra, None)
        for rel, digest in sorted(wanted.items()):
            _copy(clean, rel, digest, subs)
        # v1 builder writes via write(output) - invoke through a tiny driver in the clean tree
        (clean / 'ledger').mkdir(exist_ok=True)
        driver = ("import sys; sys.path.insert(0,'src'); import build_atlas; "
                  "from pathlib import Path; build_atlas.write(Path('atlas/provisional_v1_repro'))")
        cmds = [('v1', [sys.executable, '-c', driver]),
                ('v2', [sys.executable, 'src/build_atlas_v2.py']),
                ('v3', [sys.executable, 'src/build_atlas_v3.py']),
                ('v4', [sys.executable, 'src/build_atlas_v4.py'])]
        stage_hashes = {}
        for label, cmd in cmds:
            # per-stage code materialization: install THIS stage's manifest code bytes
            man = manifests[label]
            rec = {}
            for rel, digest in {**(man.get('code') or {}), **(man.get('code_hashes') or {})}.items():
                srcp = ROOT / rel
                if not srcp.exists() or sha256_file(srcp) != digest:
                    frozen = ROOT / 'artifacts/sha256' / digest
                    assert frozen.is_file() and sha256_file(frozen) == digest, (label, rel)
                    srcp = frozen
                    rec[rel] = {'expected': digest, 'source': 'frozen_artifact', 'actual': digest}
                else:
                    rec[rel] = {'expected': digest, 'source': 'current', 'actual': digest}
                dst = clean / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(srcp, dst)
                assert sha256_file(dst) == digest
            stage_hashes[label] = rec
            r = subprocess.run(cmd, cwd=clean, capture_output=True, text=True, timeout=600)
            if r.returncode != 0:
                stage_results[label] = {'pass': False, 'stage_failed': True, 'stderr_tail': r.stderr[-1200:]}
                break
            retained = dict((lbl, d) for lbl, _, _, d in STAGES)[label]
            gen_dir = 'atlas/provisional_v1_repro' if label == 'v1' else retained
            same = {}
            for f in ('genes.csv', 'exclusions.csv', 'paired_observations.csv'):
                a, b = clean / gen_dir / f, ROOT / retained / f
                same[f] = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
            stage_results[label] = {'byte_identical': same, 'pass': all(same.values())}
            if label == 'v1':  # feed GENERATED v1 (not retained copies) into v2 for a true upstream chain
                for f in ('genes.csv', 'exclusions.csv', 'paired_observations.csv'):
                    shutil.copy2(clean / gen_dir / f, clean / retained / f)
    # executed C10 numeric check (displayed-precision) + eligibility recompute
    res = json.loads((ROOT / 'lock_s/results/external_v1.json').read_text())
    c10 = (ROOT / 'reviews/c10_robustness_table_v1.md').read_text()
    cu = c10.replace('−', '-').replace('–', '-')
    want3 = [f"{res['primary']['estimate']:.3f}", f"{res['primary']['ci95_donor_percentile'][0]:.3f}", f"{res['primary']['ci95_donor_percentile'][1]:.3f}"]
    c10_ok = any(('primary' in ln.lower()) and all(s in ln for s in want3) for ln in cu.splitlines())
    # eligibility: recompute totals from retained per-line detail (not stored totals)
    _e = json.loads((ROOT / 'generations/pgen003/eligibility_recompute_v1.json').read_text())
    _md = _e.get('matched_detail', {})
    _pats = {v['patient_id'] for v in _md.values()}
    _exposed = set(_e.get('broad_exposed_lines', []))
    _overlap = set(_e.get('c_overlap_patients', []))
    _elig_pats = _pats - _overlap - {_md[k]['patient_id'] for k in _exposed if k in _md}
    _elig_lines = [k for k, v in _md.items() if v['patient_id'] in _elig_pats]
    elig_ok = (len(_md) == 252 and len(_pats) == 251 and len(_elig_pats) == 250
               and len(_elig_lines) == 251 and sum(_md[k]['files'] for k in _elig_lines) == 810)
    used = {}
    report = {'stages': stage_results, 'frozen_substitutions': subs,
              'stage_code_hashes': stage_hashes, 'components': {'c10_primary_values_in_table': bool(c10_ok), 'eligibility_retained_recompute': bool(elig_ok),
                             'synthetic_use_audit': 'generations/sgen005/synthetic_use_audit.json'},
              'all_stages_pass': len(stage_results) == 4 and all(s.get('pass') for s in stage_results.values()) and c10_ok and elig_ok,
              'wall_s': round(time.monotonic() - t0, 2),
              'note': 'Isolated input/code copy in current locked env; fresh-environment attempt recorded separately.'}
    with open(out_path, 'x') as fh:
        fh.write(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))
    return 0 if report['all_stages_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
