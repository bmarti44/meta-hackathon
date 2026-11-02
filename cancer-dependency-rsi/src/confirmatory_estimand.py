"""Pure-array implementation of the predeclared external donor estimand.

No data loading or outcome access. The eventual guarded Lock2 adapter must
supply the fixed207gene order,selected library permodel,and frozen covariates.
LFC and Chronos are compared through within-assay ranks,never subtracted.
Normalization uncertainty is not propagated; Broad covariates are fixed.
"""
from __future__ import annotations
import math
import numpy as np
import pandas as pd
from estimators import partial_spearman,null_expected_displacement


def _profiles(scores,reference,sample_ids,donor_ids,integer=False):
    """Return genes x unique-donors profiles, averaging models WITHIN donors first."""
    scores=np.asarray(scores,dtype=float);reference=np.asarray(reference,dtype=float)
    if scores.ndim!=2 or reference.shape!=(scores.shape[0],) or scores.shape[0]<3:
        raise ValueError('incompatible gene/sample/reference dimensions')
    if scores.shape[1]!=len(sample_ids) or len(sample_ids)!=len(donor_ids):
        raise ValueError('sample/donor mapping length mismatch')
    if len(set(sample_ids))!=len(sample_ids):raise ValueError('duplicate biological model IDs (select one library first)')
    if any(d is None or not str(d).strip() or str(d).lower()=='nan' for d in donor_ids):
        raise ValueError('unresolved donor identity')
    if not np.isfinite(scores).all() or not np.isfinite(reference).all():
        raise ValueError('nonfinite original scores/reference')
    rank0=pd.Series(reference).rank(method='average').to_numpy()
    ranks=pd.DataFrame(scores).rank(axis=0,method='average').to_numpy()
    if np.ptp(rank0)==0 or np.any(np.ptp(ranks,axis=0)==0):
        raise ValueError('degenerate sample or reference dependency ordering')
    # Twice average ranks are integers. Integer aggregation preserves exact
    # ties in donor means; floating summation can otherwise change ranks
    # merely by duplicating every nested model in a code fixture.
    numerator=np.rint(2*np.abs(ranks-rank0[:,None])).astype(np.int64)
    from donor_kernel import aggregate_models
    profiles,donors,denominator=aggregate_models(numerator,donor_ids,2*(len(rank0)-1))
    if integer:return profiles,donors,rank0,denominator
    return profiles/denominator,donors,rank0


def donor_displacement_profiles(scores,reference,sample_ids,donor_ids):
    return _profiles(scores,reference,sample_ids,donor_ids)


def decision(ci,delta=0.20):
    if ci is None:return 'INCONCLUSIVE'
    lo,hi=ci
    if not np.isfinite([lo,hi]).all() or lo>=hi:return 'INCONCLUSIVE'
    if lo>delta:return 'SIGNAL'
    if hi< -delta:return 'NEGATIVE'
    if lo> -delta and hi<delta:return 'BOUND'
    return 'INCONCLUSIVE'


def association(profiles,lability,baseline_strength,null_calibrated=False,rank0=None,denominator=1):
    profiles=np.asarray(profiles)
    if profiles.ndim!=2 or not np.isfinite(profiles).all():raise ValueError('nonfinite or invalid donor profiles')
    D=profiles.sum(axis=1)/(profiles.shape[1]*denominator)
    if null_calibrated:
        if rank0 is None:raise ValueError('null-calibrated sensitivity requires frozen reference ranks')
        if np.issubdtype(profiles.dtype,np.integer):
            G=len(D);r2=np.rint(2*np.asarray(rank0)).astype(np.int64);k=r2//2
            null_numerator=(2*k-G)*r2+G*(G+1)-2*k*(k+1)
            null_denominator=2*G*(G-1)
            d_denominator=profiles.shape[1]*denominator
            common=math.lcm(d_denominator,null_denominator)
            D=(profiles.sum(axis=1)*(common//d_denominator)-null_numerator*(common//null_denominator))/common
        else:
            D=D-null_expected_displacement(rank0,len(D))
    return partial_spearman(D,np.asarray(lability,dtype=float),np.asarray(baseline_strength,dtype=float))


def donor_bootstrap(scores,reference,lability,baseline_strength,sample_ids,donor_ids,
                    reps=5000,seed=20261028,null_calibrated=False):
    from donor_kernel import bootstrap_profiles
    profiles,donors,rank0,denominator=_profiles(scores,reference,sample_ids,donor_ids,integer=True)
    result=bootstrap_profiles(profiles,lability,baseline_strength,reps,seed,denominator,
                              rank0 if null_calibrated else None)
    result.update({'n_models':len(sample_ids),'n_donors':len(donors),'n_fixed_genes':len(reference),
        'resampling_unit':'unique_donor_all_nested_models_carried_together',
        'Broad_covariates_resampled':False,'normalization_uncertainty_propagated':False,
        'interpretation':'conditional_on_fixed_panel_Broad_models_and_processed_measurements'})
    result['decision']=decision(result['ci95_donor_percentile'])
    return result
