"""Atlas v4: v3 + corrected disposition semantics (v3-package review HIGH-1).

- "tested, not FDR-significant" is distinguished from "not located": every panel gene has S1 author
  format/serum test results joined, so non-significant genes say exactly that with their FDR values.
- CDK6 gains S1's glial/mesenchymal + CDKN2A-stratified dependency findings (Fig.3/Ext.Data Fig.6,
  with reported significance incl. NS cases) in addition to the S3 transfer note.
- WLS/TCF7L2/FZD5 state association is classified consistently in prior and biomarker fields.
- Legacy generic `prior_knowledge_status` reconciled to the disposition summary (no stale generic text).
Descriptive joins of published outputs only; no new outcome access or per-gene inference.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402

V3 = ROOT / 'atlas/v3'
OUT = ROOT / 'atlas/v4'
S1_WNT = {'WLS', 'TCF7L2', 'FZD5'}
CDK6_S1 = ('S1_text_separate_qualifications: glial_vs_mesenchymal_CDK6_enrichment_delta=-0.44_P=0.013_q=0.28_NONsignificant_after_multiple_testing; '
           'CDKN2A_CN_correlation_across_GBM_r=0.520_q=4.12e-5; within_glial_r=0.640_q=0.0340; '
           'drug_GR_AOC_CDKN2A_neutral_vs_loss_abemaciclib_P=7.1e-4_palbociclib_P=0.021_ribociclib_P=0.051_NS (Fig3/ExtDataFig6)')


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    m = pd.read_csv(V3 / 'genes.csv')
    assert len(m) == 250 and m['gene'].is_unique

    def prior(r):
        t = []
        t.append('S1_reported_format_sensitive_FDR<0.05_author_test' if r['prior_S1_format_FDR'] < 0.05
                 else f"S1_author_tested_format_not_FDR_significant(FDR={r['prior_S1_format_FDR']:.3g})")
        t.append('S1_reported_serum_sensitive_FDR<0.05_author_test' if r['prior_S1_serum_FDR'] < 0.05
                 else f"S1_author_tested_serum_not_FDR_significant(FDR={r['prior_S1_serum_FDR']:.3g})")
        if r['gene'] in S1_WNT:
            t.append('S1_text_WNT_dependency_correlated_PDAC_classical_MUC_state')
        if r['gene'] == 'CDK6':
            t.append(CDK6_S1)
        return ';'.join(t)

    def biomarker(r):
        t = []
        if r['gene'] in S1_WNT:
            t.append('S1_state_associated_dependency(PDAC_classical_MUC)_state_biomarker_association_reported; predictive_biomarker_utility_not_evaluated_in_this_campaign')
        if r['gene'] == 'CDK6':
            t.append('S1_CDKN2A_CN_and_glial_state_stratified_dependency_reported(see prior disposition); predictive_utility_not_evaluated_here')
            t.append('S3_text_FDR_passing_Sanger_rank_transfer_target_expression_model_estimand')
        return ';'.join(t) if t else 'not_evaluated_in_this_campaign;no_S1_S2_S3_gene_specific_biomarker_report_located_in_cached_full_texts'

    m['prior_knowledge_disposition'] = m.apply(prior, axis=1)
    m['biomarker_disposition'] = m.apply(biomarker, axis=1)
    m['prior_knowledge_status'] = m['prior_knowledge_disposition']
    m['biomarker_evidence'] = m['biomarker_disposition']
    m['atlas_status'] = m['atlas_status'].str.replace('V3_POSTLOCK2', 'V4_POSTLOCK2', regex=False)
    # sgen001 identity reconciliation: 144 locked covariate-ID groups = 142 patients; patient-weighted effects unquantified
    m['external_transfer_evidence'] = m['external_transfer_evidence'].str.replace(
        '148models_144donors', '148models_144covariateIDgroups_142patients_patient_weighting_effects_unquantified', regex=False)
    m.to_csv(OUT / 'genes.csv', index=False)
    for f in ('exclusions.csv', 'paired_observations.csv'):
        (OUT / f).write_bytes((V3 / f).read_bytes())
    v3m = json.loads((V3 / 'manifest.json').read_text())
    manifest = {**v3m, 'status': 'V4_POSTLOCK2',
        'evidence_types': {**v3m['evidence_types'],
            'prior_knowledge': 'S1 author test per gene (significant or explicitly tested-not-significant with FDR) + S1 text findings (WNT state: WLS/TCF7L2/FZD5; CDK6 glial/CDKN2A Fig3) + author library classes',
            'biomarker': 'not evaluated as predictive biomarkers in this campaign; reported state/genotype associations for WLS/TCF7L2/FZD5/CDK6 annotated as such; S2 highlighted WRN/MDM2/CCNE1 are not panel members; S3 CDK6 note is a different estimand'},
        'inputs': {str(p.relative_to(ROOT)): sha256_file(p) for p in [V3 / 'genes.csv', V3 / 'exclusions.csv', V3 / 'paired_observations.csv', V3 / 'manifest.json']},
        'code': {'src/build_atlas_v4.py': sha256_file(ROOT / 'src/build_atlas_v4.py')},
        'note': 'v4 corrects disposition semantics (review HIGH-1) + donor-identity wording per sgen001 (144 covariate-ID groups = 142 patients; patient-weighted effects unknown in size/direction); all measurements inherited unchanged.'}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps({'genes': len(m)}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
