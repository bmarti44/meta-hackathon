import numpy as np
import pytest
from confirmatory_estimand import donor_displacement_profiles,donor_bootstrap,decision


def test_nested_models_are_averaged_before_donors():
    reference=np.array([-3.,-2.,-1.,0.])
    scores=np.column_stack([reference,reference,reference[::-1]])
    profiles,donors,rank0=donor_displacement_profiles(scores,reference,['a','b','c'],['d1','d1','d2'])
    assert donors==['d1','d2']
    assert np.array_equal(profiles[:,0],np.zeros(4))
    assert np.allclose(profiles[:,1],[1,1/3,1/3,1])
    assert np.allclose(profiles.mean(axis=1),[.5,1/6,1/6,.5])
    # Direct model averaging would incorrectly give the reversed donor1/3weight.
    transformed=donor_displacement_profiles(scores*7+5,reference,['a','b','c'],['d1','d1','d2'])[0]
    assert np.array_equal(transformed,profiles)


@pytest.mark.parametrize('null_calibrated',[False,True])
def test_bootstrap_uses_unique_donors_not_duplicate_models(null_calibrated):
    rng=np.random.default_rng(17);g=60;n=16
    reference=rng.normal(size=g);scores=rng.normal(size=(g,n))
    L=rng.uniform(size=g);base=np.abs(reference)
    args=(scores,reference,L,base,[f's{i}' for i in range(n)],[f'd{i//2}' for i in range(n)])
    first=donor_bootstrap(*args,reps=200,null_calibrated=null_calibrated)
    more=donor_bootstrap(np.repeat(scores,2,axis=1),reference,L,base,
        [f't{i}' for i in range(n*2)],np.repeat(args[-1],2).tolist(),reps=200,null_calibrated=null_calibrated)
    assert first['n_donors']==more['n_donors']==8
    assert first['estimate']==more['estimate']
    assert first['ci95_donor_percentile']==more['ci95_donor_percentile']


def test_original_data_guards_and_boundary_decisions():
    score=np.arange(12.).reshape(4,3)
    with pytest.raises(ValueError,match='duplicate'):
        donor_displacement_profiles(score,np.arange(4),['a','a','b'],['x','x','y'])
    score[1,1]=np.inf
    with pytest.raises(ValueError,match='nonfinite'):
        donor_displacement_profiles(score,np.arange(4),['a','b','c'],['x','x','y'])
    assert decision([-.19,.19])=='BOUND'
    assert decision([-.2,.19])=='INCONCLUSIVE'
    assert decision([.21,.8])=='SIGNAL'
    assert decision([-.8,-.21])=='NEGATIVE'
    assert decision([-.3,.1])=='INCONCLUSIVE'


def test_null_expected_displacement_handles_average_tied_ranks():
    from estimators import null_expected_displacement
    ranks=np.arange(1,10,.5)
    expected=np.array([np.mean(np.abs(np.arange(1,11)-r))/9 for r in ranks])
    assert np.allclose(null_expected_displacement(ranks,10),expected,rtol=0,atol=1e-15)


def test_vector_kernel_matches_independent_scalar_projection_oracle():
    from donor_kernel import rank_correlations
    from estimators import partial_spearman
    rng=np.random.default_rng(41);targets=rng.normal(size=(20,75));x=rng.normal(size=75);z=rng.normal(size=75)
    oracle=np.array([partial_spearman(y,x,z) for y in targets])
    assert np.allclose(rank_correlations(targets,x,z),oracle,rtol=0,atol=1e-12)


def test_vector_kernel_rejects_constant_ranks_despite_projection_roundoff():
    from donor_kernel import rank_correlations,bootstrap_profiles
    x=np.arange(207.);z=np.tile(np.arange(23.),9)
    assert np.isnan(rank_correlations(np.full(207,.5),x,z)[0])
    r=bootstrap_profiles(np.full((207,144),.5),x,z,reps=100)
    assert not r['point_valid'] and not r['interval_valid'] and r['decision']=='INCONCLUSIVE'


def test_rank_equivalent_tiny_scale_and_zero_width_helpers():
    reference=np.arange(4.);scores=np.column_stack([reference,reference[::-1]])
    original=donor_displacement_profiles(scores,reference,['a','b'],['d1','d2'])[0]
    tiny=donor_displacement_profiles(scores*1e-14,reference*1e-14,['a','b'],['d1','d2'])[0]
    assert np.array_equal(original,tiny)
    assert all(decision([v,v])=='INCONCLUSIVE' for v in [-.3,0,.3])
