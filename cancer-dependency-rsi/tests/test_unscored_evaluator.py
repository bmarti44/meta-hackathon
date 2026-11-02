import json
from pathlib import Path
import evaluator_v4


def test_all_six_roots_are_unscored_even_when_descriptively_valid():
    branches=json.loads(Path('config/episodes.json').read_text())['pilot_E0']['branches']
    for branch in branches:
        result=evaluator_v4.evaluate(branch['root_config'])
        assert result['descriptive_valid'],result['invalid_reasons']
        assert result['q'] is None and result['admissible_for_policy'] is False
        assert result['scientific_interval'] is None and result['valid_scientific_inference'] is False
    primary=evaluator_v4.evaluate(branches[0]['root_config'])
    assert abs(primary['estimate']-0.055252514705032764)<1e-12


def test_unscored_rejects_non_layer_a_and_illegal_config():
    c={'scope':'primary216','operator':'mean_abs_delta','adjust':'base_strength'}
    assert not evaluator_v4.evaluate({**c,'uses_non_layerA':True})['descriptive_valid']
    assert not evaluator_v4.evaluate({**c,'operator':'ols_fe_coef_abs'})['descriptive_valid']
    assert not evaluator_v4.evaluate({**c,'hidden':'future'})['descriptive_valid']
