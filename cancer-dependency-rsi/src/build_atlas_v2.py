"""Atlas v2: provisional_v1 inventory + Lock2 external per-gene displacement (descriptive, post-Lock2).

Adds, for the 207 confirmatory genes, the donor-averaged normalized displacement D_g from the single
locked external run (lock_s/results/external_v1_gene_displacement.csv), the tie-aware null expectation
E_null and D_g - E_null, and within-panel ranks. Per-gene values are descriptive coordinates of a
panel-level estimand; no per-gene inference, vulnerability or invariance claim is made. The panel-level
decision (BOUND) and its robustness limits are recorded in the manifest.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import estimators  # noqa: E402
from ledger import sha256_file  # noqa: E402

V1 = ROOT / 'atlas/provisional_v1'
OUT = ROOT / 'atlas/v2'
EXT = ROOT / 'lock_s/results/external_v1_gene_displacement.csv'
RES = ROOT / 'lock_s/results/external_v1.json'


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    genes = pd.read_csv(V1 / 'genes.csv')
    ext = pd.read_csv(EXT)
    G = len(ext)
    r0 = pd.Series(ext['AdherentMean'].to_numpy()).rank(method='average').to_numpy()
    ext['reference_rank_within_207'] = r0
    ext['E_null_displacement'] = estimators.null_expected_displacement(r0, G)
    ext['D_minus_null'] = ext['D_g'] - ext['E_null_displacement']
    ext['D_g_rank_within_207'] = ext['D_g'].rank(method='average')
    ext['L_g_rank_within_207'] = ext['L_g'].rank(method='average')
    ext = ext.rename(columns={'gene_broad': 'gene'})
    keep = ['gene', 'gene_sanger', 'D_g', 'E_null_displacement', 'D_minus_null', 'D_g_rank_within_207', 'reference_rank_within_207', 'L_g_rank_within_207']
    m = genes.merge(ext[keep].rename(columns={c: f'external_{c}' for c in keep if c != 'gene'}), on='gene', how='left')
    has = m['external_D_g'].notna()
    m.loc[has, 'external_transfer_evidence'] = 'Lock2_single_retrospective_external_measurement_Sanger_148models_144donors_descriptive_per_gene_coordinate'
    m.loc[~has, 'external_transfer_evidence'] = 'not_evaluated_not_in_confirmatory207 (' + m.loc[~has, 'confirmatory_exclusion_reasons'].fillna('see exclusions.csv') + ')'
    m['external_contradiction'] = np.where(has, 'panel_level_sign_opposite_to_positive_conjecture_magnitude_below_0.20_primary_only', 'not_evaluated')
    m['invariance_equivalence_evidence'] = 'none_no_positive_dependency_equivalence_or_assay_sensitivity_evidence'
    m['atlas_status'] = np.where(has, 'V2_POSTLOCK2_DESCRIPTIVE_EXTERNAL_COORDINATE_NOT_A_PER_GENE_CLAIM', m['atlas_status'])
    m.to_csv(OUT / 'genes.csv', index=False)
    for f in ('exclusions.csv', 'paired_observations.csv'):
        (OUT / f).write_bytes((V1 / f).read_bytes())
    res = json.loads(RES.read_text())
    manifest = {
        'status': 'V2_POSTLOCK2', 'panel_genes': int(len(m)), 'genes_with_external_coordinate': int(has.sum()),
        'panel_level_external_result': {'decision': res['decision'], 'estimate': res['primary']['estimate'], 'ci95_donor': res['primary']['ci95_donor_percentile'],
                                        'robustness': 'sign robust across secondaries/stability; magnitude bound holds for primary,S2,S3 only (S1,S4, model-cluster and gene-block ranges cross -0.20)'},
        'evidence_types': {'environment': 'Layer-A paired minipool contrasts (exploratory, adaptively reused)', 'transfer': 'single Lock2 external retrospective measurement (association component only)',
                           'biomarker': 'not evaluated in this campaign', 'prior_knowledge': 'author library classes only', 'invariance': 'none', 'causal': 'none'},
        'inputs': {str(p.relative_to(ROOT)): sha256_file(p) for p in [V1 / 'genes.csv', V1 / 'exclusions.csv', V1 / 'paired_observations.csv', EXT, RES]},
        'code': {'src/build_atlas_v2.py': sha256_file(ROOT / 'src/build_atlas_v2.py'), 'src/estimators.py': sha256_file(ROOT / 'src/estimators.py')},
        'note': 'Post-Lock2 use of C here is descriptive bookkeeping of the locked output, not new inference.'}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps({'genes': len(m), 'external': int(has.sum())}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
