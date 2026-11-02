"""Production donor-bootstrap kernel; algorithmic fixtures exercise this same code.

No data access and no policy quality score. A synthetic calibration pass is
not evidence of coverage in the biological donor population.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.stats import rankdata
import estimators


def aggregate_models(values,donor_ids,denominator=1):
    """Same nested-model aggregation for production ranks and code fixtures."""
    values=np.asarray(values)
    if values.ndim!=2 or values.shape[1]!=len(donor_ids) or not np.isfinite(values).all():
        raise ValueError('malformed model-to-donor contributions')
    if any(d is None or not str(d).strip() or str(d).lower()=='nan' for d in donor_ids):
        raise ValueError('unresolved donor identity')
    ids=np.asarray(list(map(str,donor_ids)));donors=sorted(set(ids))
    sizes=[int(np.sum(ids==d)) for d in donors]
    if np.issubdtype(values.dtype,np.integer):
        common=math.lcm(*sizes)
        if denominator*common*len(donor_ids)>np.iinfo(np.int64).max:
            raise ValueError('nested-model integer representation would overflow')
        result=np.column_stack([values[:,ids==d].sum(axis=1)*(common//n) for d,n in zip(donors,sizes)])
        return result,donors,denominator*common
    return np.column_stack([values[:,ids==d].mean(axis=1) for d in donors]),donors,denominator


def rank_correlations(targets,lability,baseline_strength):
    Y=np.atleast_2d(np.asarray(targets,dtype=float));x=np.asarray(lability,dtype=float)
    z=np.asarray(baseline_strength,dtype=float)
    if z.ndim==1:z=z[:,None]
    if Y.shape[1]!=len(x) or z.shape[0]!=len(x):raise ValueError('incompatible fixed-gene dimensions')
    rx=estimators._rank_resid(x,z)
    rz=rankdata(z,axis=0,method='average')
    design=np.column_stack([np.ones(len(x)),rz])
    result=np.full(len(Y),np.nan)
    good=np.isfinite(Y).all(axis=1)
    if not good.any():return result
    ranks=rankdata(Y[good],axis=1,method='average')
    residual=ranks.T-design@np.linalg.lstsq(design,ranks.T,rcond=None)[0]
    residual_norm=np.linalg.norm(residual,axis=0)
    centered_norm=np.linalg.norm(ranks-ranks.mean(axis=1)[:,None],axis=1)
    valid=np.isfinite(residual).all(axis=0)&(centered_norm>1e-12)&(residual_norm>1e-12*np.maximum(1,centered_norm))
    vals=np.full(len(ranks),np.nan)
    vals[valid]=np.clip((rx@residual[:,valid])/(np.linalg.norm(rx)*residual_norm[valid]),-1,1)
    result[np.flatnonzero(good)]=vals
    return result


def means_from_sums(sums,n_donors,denominator,rank0=None):
    sums=np.asarray(sums);d_den=n_donors*denominator
    if rank0 is None:return sums/d_den
    G=sums.shape[-1]
    if np.issubdtype(sums.dtype,np.integer):
        r2=np.rint(2*np.asarray(rank0)).astype(np.int64);k=r2//2
        null_num=(2*k-G)*r2+G*(G+1)-2*k*(k+1)
        null_den=2*G*(G-1);common=math.lcm(d_den,null_den)
        factor=common//d_den
        if np.max(np.abs(sums))*factor>np.iinfo(np.int64).max//2:
            raise ValueError('null correction integer representation would overflow')
        return (sums*factor-null_num*(common//null_den))/common
    return sums/d_den-estimators.null_expected_displacement(rank0,G)


def bootstrap_profiles(profiles,lability,baseline_strength,reps=5000,seed=20261028,
                       denominator=1,rank0=None,draws=None):
    profiles=np.asarray(profiles)
    if profiles.ndim!=2 or profiles.shape[0]<3 or profiles.shape[1]<2:
        raise ValueError('need genes x at least2unique donor profiles')
    if not np.isfinite(profiles).all() or profiles.min()<0 or profiles.max()>denominator:
        raise ValueError('nonfinite or out-of-range normalized donor contributions')
    if not isinstance(reps,int) or reps<100:raise ValueError('at least100replicates required')
    n_donors=profiles.shape[1]
    point=means_from_sums(profiles.sum(axis=1),n_donors,denominator,rank0)
    try:estimate=float(rank_correlations(point,lability,baseline_strength)[0])
    except ValueError:estimate=float('nan')
    if not np.isfinite(estimate):
        return {'point_valid':False,'estimate':None,'interval_valid':False,'ci95_donor_percentile':None,
            'decision':'INCONCLUSIVE','failed_replicates':None,'total_replicates':reps,
            'invalid_reasons':['degenerate/nonfinite point estimate'],'q':None,'admissible_for_policy':False}
    if draws is None:
        draws=np.random.default_rng(seed).integers(0,n_donors,size=(reps,n_donors))
    draws=np.asarray(draws)
    if draws.shape!=(reps,n_donors) or not np.issubdtype(draws.dtype,np.integer) or draws.min()<0 or draws.max()>=n_donors:
        raise ValueError('invalid frozen donor resampling indices')
    counts=np.zeros((reps,n_donors),dtype=np.int64)
    np.add.at(counts,(np.repeat(np.arange(reps),n_donors),draws.ravel()),1)
    sums=counts@profiles.T
    means=means_from_sums(sums,n_donors,denominator,rank0)
    values=rank_correlations(means,lability,baseline_strength)
    finite=np.isfinite(values);failed=int((~finite).sum())
    ci=np.percentile(values[finite],[2.5,97.5]).tolist() if finite.any() else None
    reasons=[]
    if failed/reps>0.05:reasons.append('more than5percent failed bootstrap replicates')
    if ci is None or not np.isfinite(ci).all():reasons.append('nonfinite percentile endpoints')
    elif ci[1]-ci[0]<=0:reasons.append('zero/nonpositive interval width')
    valid=not reasons
    return {'point_valid':True,'estimate':estimate,'interval_valid':valid,
        'ci95_donor_percentile':ci if valid else None,'failed_replicates':failed,
        'total_replicates':reps,'seed':seed,'invalid_reasons':reasons,
        'zero_width_interval':bool(ci is not None and ci[1]==ci[0]),
        'q':None,'admissible_for_policy':False}
