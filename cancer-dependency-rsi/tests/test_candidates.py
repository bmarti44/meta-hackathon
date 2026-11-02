import json
from pathlib import Path
import pytest
from pydantic import ValidationError
import candidates


def proposal(origin='refinement',parents=None):
    return {'origin':origin,'parents':parents if parents is not None else [{'attempt_id':'a','contribution':'refine scope'}],
        'config':{'scope':'primary216','operator':'mean_abs_delta','adjust':'base_strength'},
        'direction_id':'d','priority':0.5,'bottleneck':'stability','evidence_attempt_ids':['a']}


def existing():
    return {k:{'attempt_id':k,'study_id':'S','evaluator_version':'v','parents':[]} for k in ['a','b']}


def test_schema_batch_and_runtime_lineage_agree():
    frozen=json.loads(Path('generations/prompts/candidate_batch_schema_v2.json').read_text())
    assert candidates.schema()==frozen and frozen['type']=='array'
    out=candidates.validate_batch([proposal()],existing(),'S','v')
    assert out[0]['parents'][0]['attempt_id']=='a'
    blend=proposal('combination',[{'attempt_id':'a','contribution':'operator'},{'attempt_id':'b','contribution':'scope'}])
    assert candidates.validate_batch([blend],existing(),'S','v')


def test_runtime_rejects_schema_and_history_violations():
    with pytest.raises(ValidationError):candidates.validate_batch(proposal(),existing(),'S','v')
    for node in [proposal('combination'),{**proposal(),'extra':'secret'},
                 {**proposal(),'evidence_attempt_ids':['hidden']},
                 {**proposal(),'config':{**proposal()['config'],'operator':'invented'}}]:
        with pytest.raises((ValueError,ValidationError)):candidates.validate_batch([node],existing(),'S','v')
    with pytest.raises(ValueError,match='version'):candidates.validate_batch([proposal()],existing(),'S','wrong')


def test_evidence_citations_require_same_study_and_evaluator():
    ex=existing();ex['foreign']={'study_id':'other','evaluator_version':'old','parents':[]}
    node=proposal();node['evidence_attempt_ids'].append('foreign')
    with pytest.raises(ValueError,match='evidence ID study/evaluator'):
        candidates.validate_batch([node],ex,'S','v')
