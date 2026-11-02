"""sgen002 reproduction: v3->v4 reproduction from retained v3 inputs + locked-estimate checks.

Uses current locked environment (not a clean-room install); inputs/code are hash-verified
against atlas/v4 manifest before copying. No outcome re-decoding beyond retained frozen outputs.
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

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402

import argparse as _ap
_ap_p = _ap.ArgumentParser(); _ap_p.add_argument('--report', default='generations/sgen002/reproduction_report_v3.json')
OUT = ROOT / _ap_p.parse_args().report


def main() -> int:
    t0 = time.monotonic()
    comps = {}
    # 1) atlas v4 chain in isolated copy: v3 genes = v2 output; rebuild v4 from retained v3 inputs.
    man = json.loads((ROOT / 'atlas/v4/manifest.json').read_text())
    for rel, digest in {**man['inputs'], **man['code']}.items():
        assert sha256_file(ROOT / rel) == digest, f'hash mismatch: {rel}'
    with tempfile.TemporaryDirectory(prefix='cdrsi-sgen002-') as td:
        clean = Path(td)
        for rel in list(man['inputs']) + list(man['code']) + ['src/ledger.py']:
            dst = clean / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        # builders resolve ROOT from file location; run v4 builder inside the clean copy
        r = subprocess.run([sys.executable, 'src/build_atlas_v4.py'], cwd=clean,
                           capture_output=True, text=True, timeout=300)
        assert r.returncode == 0, r.stderr[-1000:]
        identical = {}
        for f in ('genes.csv', 'exclusions.csv', 'paired_observations.csv'):
            identical[f] = (clean / 'atlas/v4' / f).read_bytes() == (ROOT / 'atlas/v4' / f).read_bytes()
        comps['atlas_v4_isolated_rebuild'] = {'byte_identical': identical, 'pass': all(identical.values())}
    # 2) primary point (retained coordinates)
    ext = pd.read_csv(ROOT / 'lock_s/results/external_v1_gene_displacement.csv')
    res = json.loads((ROOT / 'lock_s/results/external_v1.json').read_text())
    def rank(a): return pd.Series(a).rank(method='average').to_numpy()
    x, y, z = rank(ext['L_g']), rank(ext['D_g']), rank(np.abs(ext['AdherentMean']))
    A = np.column_stack([np.ones(len(z)), z])
    rx = x - A @ np.linalg.lstsq(A, x, rcond=None)[0]
    ry = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    rho = float(np.corrcoef(rx, ry)[0, 1])
    comps['primary_point'] = {'recomputed': rho, 'locked': res['primary']['estimate'],
                              'abs_diff': abs(rho - res['primary']['estimate']),
                              'pass': bool(abs(rho - res['primary']['estimate']) <= 1e-10 + 1e-8 * abs(res['primary']['estimate']))}
    # 3) figure byte-identical: generate in isolated temp copy, compare to retained bytes (never overwrite evidence)
    retained = sha256_file(ROOT / 'manuscript/figures/figure1_primary.svg')
    with tempfile.TemporaryDirectory(prefix='cdrsi-fig-') as td:
        fc = Path(td)
        for rel in ['src/make_figure1.py', 'lock_s/results/external_v1_gene_displacement.csv', 'lock_s/results/external_v1.json']:
            dst = fc / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT / rel, dst)
        r = subprocess.run([sys.executable, 'src/make_figure1.py'], cwd=fc, capture_output=True, text=True, timeout=120)
        gen = sha256_file(fc / 'manuscript/figures/figure1_primary.svg') if (fc / 'manuscript/figures/figure1_primary.svg').exists() else None
    comps['figure1'] = {'retained_sha256': retained, 'isolated_sha256': gen, 'pass': r.returncode == 0 and gen == retained}
    comps['scope'] = 'v3->v4 reproduction from retained v3 inputs (ledgered scope deviation: upstream v1->v2->v3 rebuild NOT implemented in this runner)'
    comps['omitted_components'] = {'upstream_atlas_rebuild': 'NOT_IMPLEMENTED_IN_RUNNER (verified separately by reviewer in-memory)',
                                   'ols_anchor': 'generations/sgen002/ols_tolerance_disposition.json', 'c10_table': 'verified by sol-high reviews',
                                   'eligibility': 'generations/pgen003/eligibility_recompute_v1.json (independently reproduced)'}
    comps['pending'] = {'donor_interval': 'PENDING: no retained donor-level arrays; requires outcome re-access (not performed)',
                        'policy_comparison': 'ABSENT: no policy cycle has run (C8/C9 unmet)',
                        'clean_room_install': 'NOT RUN: isolated input/code copy in current locked env, not a fresh environment install'}
    report = {'components': comps, 'wall_s': round(time.monotonic() - t0, 2),
              'implemented_components_pass': bool(comps['atlas_v4_isolated_rebuild']['pass'] and comps['primary_point']['pass'] and comps['figure1']['pass'])}
    with open(OUT, 'x') as fh:
        fh.write(json.dumps(report, indent=1))
    print('report sha256:', sha256_file(OUT))
    print(json.dumps(report, indent=1))
    return 0 if report['implemented_components_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
