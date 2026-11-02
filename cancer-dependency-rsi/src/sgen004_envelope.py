"""sgen004 weighting envelope (SPEC e0044a4b...). No C outcome access; retained outputs only.

Worst-case bound on patient-weighted vs archived donor-weighted displacement and the
induced rank movement. Premise verified in src/confirmatory_estimand.py: per-model normalized
displacement = |rank - rank0| / (207-1) in [0,1], averaged within donor, then across donors.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generations/sgen004/envelope_v3.json'


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', str(s).upper())


def main() -> int:
    cohort = pd.read_csv(ROOT / 'lock_s/cohort.csv', dtype=str)
    models = pd.read_csv(ROOT / 'data/passports_model_list_20260921.csv', dtype=str).fillna('')
    key = {}
    for _, r in models.iterrows():
        for cand in [r['model_name']] + re.split(r'[|;]', str(r.get('synonyms') or '')):
            k = norm(cand)
            if k:
                key.setdefault(k, set()).add(str(r['patient_id']))
    patient = {}
    for s in cohort['sample_ID']:
        pats = key.get(norm(s), set())
        assert len(pats) == 1, (s, pats)
        patient[s] = next(iter(pats))
    cohort['patient'] = cohort['sample_ID'].map(patient)
    assert cohort['donor_ID'].nunique() == 144 and cohort['patient'].nunique() == 142
    gc = cohort.groupby('donor_ID')['sample_ID'].transform('count')
    pc = cohort.groupby('patient')['sample_ID'].transform('count')
    w_a = 1.0 / (144 * gc.to_numpy(dtype=float))
    w_p = 1.0 / (142 * pc.to_numpy(dtype=float))
    tv = 0.5 * float(np.abs(w_a - w_p).sum())

    ext = pd.read_csv(ROOT / 'lock_s/results/external_v1_gene_displacement.csv')
    res = json.loads((ROOT / 'lock_s/results/external_v1.json').read_text())
    D = np.sort(ext['D_g'].to_numpy())
    n = len(D)
    # worst-case rank movement per gene under pointwise |D'-D| <= TV (both genes move toward each other)
    moves = []
    for v in D:
        moves.append(int(((D >= v - 2 * tv) & (D <= v + 2 * tv)).sum()) - 1)
    moves = np.array(moves)
    # Spearman bound: rho = 1 - 6*sum(d_i^2)/(n(n^2-1)) for simple ranks (ties make this an
    # approximation - recorded as conservative screen rationale, not an exact partial-Spearman bound).
    # Adversarial: every gene's rank difference vs L-rank shifts by up to its feasible movement
    # in the direction that most reduces |rho|. Upper bound on |Delta rho| via Cauchy-Schwarz on
    # rank vectors: |Delta rho| <= ||delta_rank_D|| / ||centered ranks|| (unit-norm correlation).
    # Residual-aware bound (review HIGH fix): partial Spearman correlates ranked residuals.
    # Denominator = norm of archived D-rank residuals after removing ranked |AdherentMean|;
    # numerator bounds residual movement by raw rank movement (residualization is a projection,
    # hence non-expansive for the D-side perturbation, while L-side residuals are unchanged).
    def rank(a): return pd.Series(a).rank(method='average').to_numpy()
    rd, rz = rank(ext['D_g']), rank(np.abs(ext['AdherentMean']))
    A = np.column_stack([np.ones(n), rz])
    resid = rd - A @ np.linalg.lstsq(A, rd, rcond=None)[0]
    resid_norm = float(np.sqrt((resid ** 2).sum()))
    delta_norm = float(np.sqrt((moves.astype(float) ** 2).sum()))
    # Normalization-correct bound (review): correlation renormalizes the perturbed residual;
    # |corr(x,y+d)-corr(x,y)| <= min(2, 2||d||/||y||). Degenerate residual -> no bound.
    rho_bound = min(2.0, 2 * delta_norm / resid_norm) if resid_norm > 0 else float('inf')
    rho_arch = float(res['primary']['estimate'])
    out = {
        'premise': 'per-model normalized displacement in [0,1] (confirmatory_estimand._profiles: |rank-rank0|/(207-1)) - VERIFIED',
        'weights': {'archived_groups': 144, 'patients': 142, 'models': 148,
                    'total_variation_half_L1': tv,
                    'max_abs_D_shift_bound': tv},
        'rank_movement': {'max_positions': int(moves.max()), 'median_positions': int(np.median(moves)),
                          'genes_with_any_crossable_neighbor': int((moves > 0).sum())},
        'spearman_envelope_screen': {
            'method': 'Cauchy-Schwarz bound with RESIDUAL norm denominator (projection non-expansive); pointwise TV box relaxation - screen only, proof branch disabled',
            'max_abs_rho_shift_bound': rho_bound,
            'archived_rho': rho_arch,
            'worst_case_rho_interval': [rho_arch - rho_bound, rho_arch + rho_bound]},
        'verdict': None}
    lo, hi = rho_arch - rho_bound, rho_arch + rho_bound
    # Proof verdict DISABLED (review HIGH): even the residual-aware bound is a relaxation
    # (pointwise TV box, not patient-feasible set). This screen can only fail to certify.
    out['verdict'] = 'ENVELOPE_TOO_WIDE' if not (abs(hi) < 0.20 and abs(lo) < 0.20 and hi < 0) else 'ENVELOPE_NOT_ESTABLISHED_PROOF_BRANCH_DISABLED'
    out['meaning'] = ('Point-estimate sign/magnitude screen only. Even on PASS this cannot certify a '
                      'patient-level interval, CI, or BOUND decision; scalar donor-kernel widening is not used. '
                      'C6 remains PARTIAL until patient-level inference exists on a new independent resource.')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, 'x') as fh:
        fh.write(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
