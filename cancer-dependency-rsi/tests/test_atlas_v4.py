from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_atlas_v4_dispositions():
    m = pd.read_csv(ROOT / 'atlas/v4/genes.csv').set_index('gene')
    assert len(m) == 250
    # tested-not-significant is explicit, never "no report located" for S1-tested genes
    assert not m['prior_knowledge_disposition'].str.contains('no_gene_specific_S1_report_located').any()
    nonsig = m[(m['prior_S1_format_FDR'] >= 0.05)]
    assert nonsig['prior_knowledge_disposition'].str.contains('tested_format_not_FDR_significant').all()
    # CDK6 carries both S1 Fig3 and S3 notes, consistently across fields
    assert 'CDKN2A' in m.loc['CDK6', 'prior_knowledge_disposition']
    assert 'q=0.28_NONsignificant' in m.loc['CDK6', 'prior_knowledge_disposition']
    assert 'r=0.520_q=4.12e-5' in m.loc['CDK6', 'prior_knowledge_disposition']
    assert 'r=0.640_q=0.0340' in m.loc['CDK6', 'prior_knowledge_disposition']
    assert 'q<0.005' not in m.loc['CDK6', 'prior_knowledge_disposition']
    assert 'CDKN2A' in m.loc['CDK6', 'biomarker_disposition']
    assert 'S3_text_FDR' in m.loc['CDK6', 'biomarker_disposition']
    # WNT state association consistent across prior + biomarker fields
    for g in ('WLS', 'TCF7L2', 'FZD5'):
        assert 'PDAC' in m.loc[g, 'prior_knowledge_disposition']
        assert 'state_biomarker_association_reported' in m.loc[g, 'biomarker_disposition']
    # legacy generic fields reconciled (no stale generic-only text anywhere)
    assert not m['prior_knowledge_status'].str.contains('author_library_classification_only').any()
    assert (m['prior_knowledge_status'] == m['prior_knowledge_disposition']).all()
    # FDR-significant sets unchanged from author files (v3 regression retained)
    assert set(m.index[m['prior_S1_format_FDR'] < 0.05]) == {'CTNNA1', 'ITGA3', 'ITGAV', 'ITGB1', 'NCKAP1', 'PRKCA', 'PTK2'}
    assert 'panel_level_context' in m.columns and 'external_contradiction' not in m.columns
