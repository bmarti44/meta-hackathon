"""Atlas v3: v2 + per-gene source-linked prior/biomarker dispositions (sci-package HIGH-2/MEDIUM fixes).

Annotations are descriptive joins of already-published author outputs, not new inference:
- S1 author minipool test files (figshare): per-gene format/serum coefficients and FDR for all 250 genes.
- S1 text-reported state association (WNT components vs PDAC-classical/MUC): WLS, TCF7L2, FZD5 in panel.
- S3 text-reported FDR-passing Sanger transfer targets: CDK6 in panel (MDM4, CCNE1 not in panel).
- S2 text-highlighted biomarkers WRN/MDM2/CCNE1: none in panel (recorded, not invented).
Also renames v2 per-gene `external_contradiction` -> `panel_level_context` (it was panel-level, not per-gene).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402

V2 = ROOT / 'atlas/v2'
OUT = ROOT / 'atlas/v3'
GF = ROOT / 'data/raw/broad_figshare/minipool_growth_format_tests.csv'
SS = ROOT / 'data/raw/broad_figshare/minipool_serum_status_tests.csv'
S1_WNT = {'WLS', 'TCF7L2', 'FZD5'}
S3_FDR = {'CDK6'}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    m = pd.read_csv(V2 / 'genes.csv')
    assert len(m) == 250 and m['gene'].is_unique
    m = m.rename(columns={'external_contradiction': 'panel_level_context'})
    gf = pd.read_csv(GF)[['gene', 'coefficient', 'FDR']].rename(
        columns={'coefficient': 'prior_S1_format_coef_plastic_vs_dome', 'FDR': 'prior_S1_format_FDR'})
    ss = pd.read_csv(SS)[['gene', 'coefficient', 'FDR']].rename(
        columns={'coefficient': 'prior_S1_serum_coef', 'FDR': 'prior_S1_serum_FDR'})
    m = m.merge(gf, on='gene', how='left').merge(ss, on='gene', how='left')
    assert m['prior_S1_format_FDR'].notna().all() and m['prior_S1_serum_FDR'].notna().all()

    def prior(row):
        tags = []
        if row['prior_S1_format_FDR'] < 0.05:
            tags.append('S1_reported_format_sensitive_FDR<0.05_author_test')
        if row['prior_S1_serum_FDR'] < 0.05:
            tags.append('S1_reported_serum_sensitive_FDR<0.05_author_test')
        if row['gene'] in S1_WNT:
            tags.append('S1_text_WNT_dependency_correlated_PDAC_classical_MUC')
        return ';'.join(tags) if tags else 'author_library_class_only_no_gene_specific_S1_report_located'

    def biomarker(row):
        tags = []
        if row['gene'] in S3_FDR:
            tags.append('S3_text_FDR_passing_Sanger_rank_transfer_target_expression_model_estimand')
        return ';'.join(tags) if tags else 'not_evaluated_in_this_campaign;no_S1_S2_S3_gene_specific_biomarker_report_located'

    m['prior_knowledge_disposition'] = m.apply(prior, axis=1)
    m['biomarker_disposition'] = m.apply(biomarker, axis=1)
    m['atlas_status'] = m['atlas_status'].str.replace('V2_POSTLOCK2', 'V3_POSTLOCK2', regex=False)
    m.to_csv(OUT / 'genes.csv', index=False)
    for f in ('exclusions.csv', 'paired_observations.csv'):
        (OUT / f).write_bytes((V2 / f).read_bytes())
    v2m = json.loads((V2 / 'manifest.json').read_text())
    manifest = {
        'status': 'V3_POSTLOCK2', 'panel_genes': int(len(m)),
        'genes_with_external_coordinate': v2m['genes_with_external_coordinate'],
        'panel_level_external_result': v2m['panel_level_external_result'],
        'field_dictionary': {
            'format condition_a/b': 'Dome / Plastic (held: culture medium); delta = Dome - Plastic Chronos',
            'medium condition_a/b': 'OPAC / RPMI-FBS (held: growth format); delta = OPAC - RPMI/FBS Chronos',
            'panel_level_context': 'panel-level Lock-S association context repeated for join convenience; NOT per-gene evidence',
            'prior_S1_*': 'author-published minipool test outputs (figshare), descriptive join; serum file contrasts serum vs serum-free status as released by authors',
            'prior_knowledge_disposition / biomarker_disposition': 'source-linked disposition per gene; explicit not-located/not-evaluated states, never invented findings'},
        'evidence_types': {**v2m['evidence_types'],
            'prior_knowledge': 'author library classes + S1 author test FDR per gene + S1 text state association (WLS/TCF7L2/FZD5)',
            'biomarker': 'not evaluated in this campaign; S3 CDK6 transfer note is a different (expression-model) estimand; S2 highlighted WRN/MDM2/CCNE1 are not panel members'},
        'annotation_counts': {
            'S1_format_FDR<0.05': int((m['prior_S1_format_FDR'] < 0.05).sum()),
            'S1_serum_FDR<0.05': int((m['prior_S1_serum_FDR'] < 0.05).sum()),
            'S1_WNT_in_panel': sorted(S1_WNT & set(m['gene'])), 'S3_FDR_in_panel': sorted(S3_FDR & set(m['gene']))},
        'inputs': {str(p.relative_to(ROOT)): sha256_file(p) for p in [V2 / 'genes.csv', V2 / 'exclusions.csv', V2 / 'paired_observations.csv', GF, SS]},
        'code': {'src/build_atlas_v3.py': sha256_file(ROOT / 'src/build_atlas_v3.py')},
        'note': 'Descriptive annotation of published outputs; no new C access, no per-gene inference.'}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps({'genes': len(m), **manifest['annotation_counts']}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
