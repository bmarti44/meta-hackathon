import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_atlas_v3_annotations():
    m = pd.read_csv(ROOT / 'atlas/v3/genes.csv')
    assert len(m) == 250 and m['gene'].is_unique
    assert 'panel_level_context' in m.columns and 'external_contradiction' not in m.columns
    assert m['prior_S1_format_FDR'].notna().all() and m['prior_S1_serum_FDR'].notna().all()
    fmt = set(m.loc[m['prior_S1_format_FDR'] < 0.05, 'gene'])
    assert fmt == {'CTNNA1', 'ITGA3', 'ITGAV', 'ITGB1', 'NCKAP1', 'PRKCA', 'PTK2'}
    ser = set(m.loc[m['prior_S1_serum_FDR'] < 0.05, 'gene'])
    assert ser == {'CTNNA1', 'PPP1R15B', 'PPP2R2D', 'PTK2', 'RICTOR', 'SPTLC1', 'SPTLC2', 'SQLE'}
    by = m.set_index('gene')
    assert 'S1_text_WNT' in by.loc['FZD5', 'prior_knowledge_disposition']
    assert 'S3_text_FDR' in by.loc['CDK6', 'biomarker_disposition']
    # every row carries an explicit disposition (reported finding or explicit not-located state)
    assert m['prior_knowledge_disposition'].str.len().min() > 0
    assert m['biomarker_disposition'].str.len().min() > 0
    man = json.loads((ROOT / 'atlas/v3/manifest.json').read_text())
    assert man['annotation_counts']['S1_format_FDR<0.05'] == 7
