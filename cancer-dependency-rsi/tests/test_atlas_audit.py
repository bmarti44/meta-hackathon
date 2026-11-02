import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
import audit_data
import build_atlas
from ledger import sha256_file


def test_nested_pair_weighting_is_model_equal():
    # A has two measured pairs; B has one. A must not receive twice B's weight.
    pairs=pd.DataFrame([
        {'gene':'G','axis':'format','model_id':'A','score_a':1.,'score_b':0.,'delta_a_minus_b':1.},
        {'gene':'G','axis':'format','model_id':'A','score_a':3.,'score_b':0.,'delta_a_minus_b':3.},
        {'gene':'G','axis':'format','model_id':'B','score_a':10.,'score_b':0.,'delta_a_minus_b':10.},
    ])
    s=build_atlas.summaries(pairs,'format')['G']
    assert s['format_n_models']==2 and s['format_n_pairs']==3
    assert s['format_mean_delta_a_minus_b']==6 and s['format_observed_lability']==6
    assert s['format_n_verified_donors'] is None


def test_atlas_complete_exact_membership_and_pair_arithmetic():
    atlas,pairs=build_atlas.build()
    assert len(atlas)==250 and atlas.gene.is_unique
    assert atlas.development_primary_eligible.sum()==216
    assert atlas.confirmatory_eligible.sum()==207
    assert len(pairs)==3000
    assert np.allclose(pairs.delta_a_minus_b,pairs.score_a-pairs.score_b,rtol=0,atol=1e-14)
    assert atlas.loc[~atlas.confirmatory_eligible,'confirmatory_exclusion_reasons'].str.len().gt(0).all()
    assert atlas.external_transfer_evidence.eq('not_evaluated_Lock2_quarantine').all()
    assert atlas.invariance_equivalence_evidence.eq('not_evaluated_no_invariance_claim').all()
    assert atlas.format_n_verified_donors.isna().all()


def test_frozen_exposure_prefix_accepts_append_but_rejects_tamper(tmp_path):
    p=tmp_path/'exposures.jsonl';p.write_text('first\n')
    entry={'sha256':sha256_file(p),'bytes':p.stat().st_size}
    with p.open('a') as f:f.write('second\n')
    assert audit_data.check_file(p,entry,append_only=True)['ok']
    assert not audit_data.check_file(p,entry)['ok']
    p.write_text('wrong\nsecond\n')
    assert not audit_data.check_file(p,entry,append_only=True)['ok']


def test_real_cohort_is_donor_grouped_and_dual_library_not_independent():
    r=audit_data.cohort_audit()
    assert r['ok'],r['errors']
    assert (r['library_screen_rows'],r['screened_models'],r['eligible_models'],r['eligible_donors'])==(178,162,148,144)
    c=json.loads(Path('data/split_manifest.json').read_text())['C_external']
    assert len(c['sample_to_donor'])==148 and len(c['donor_ids'])==144
    assert sorted(set(c['sample_to_donor'].values()))==c['donor_ids']


def test_cohort_rejects_hidden_donor_overlap_and_mapping_change(tmp_path):
    import shutil
    d=tmp_path/'data';d.mkdir()
    shutil.copy('data/crosswalk_sanger_screened.csv',d)
    split=json.loads(Path('data/split_manifest.json').read_text())
    c=split['C_external']
    sample=c['sample_ids'][0]
    c['sample_to_donor'][sample]=c['excluded_broad_overlap_donors'][0]
    (d/'split_manifest.json').write_text(json.dumps(split))
    r=audit_data.cohort_audit(tmp_path)
    assert not r['ok'] and any('mapping' in e for e in r['errors'])
