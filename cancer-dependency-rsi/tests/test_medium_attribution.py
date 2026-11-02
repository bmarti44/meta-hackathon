"""Unit tests for medium-attribution utilities (bh, flag rules) on synthetic data."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import pandas as pd

from medium_attribution import bh
from medium_attribution_v2 import flag_hits


def test_bh_known_values():
    p = np.array([0.01, 0.02, 0.03, 0.5])
    q = bh(p)
    # BH: sorted p*m/rank = .04,.04,.04,.5 -> monotone from largest: .04,.04,.04,.5
    assert np.allclose(q, [0.04, 0.04, 0.04, 0.5])
    assert np.allclose(bh(np.array([1.0, 1.0])), [1.0, 1.0])


def _tab(rows):
    return pd.DataFrame(rows, index=[r["gene"] for r in rows]).drop(columns="gene")


def test_flag_rules():
    base = dict(D_org_se=0.05, A_adh_se=0.05, F_dome_se=0.05, S_tsm_se=0.05,
                D_org_p=1e-6, A_adh_p=1e-4, F_dome_p=0.5, S_tsm_p=0.5,
                D_org_q=1e-5, A_adh_q=1e-3, F_dome_q=0.8, S_tsm_q=0.8, S_tsm=0.0)
    rows = [
        # clean medium gain: A ~ D, F ~ 0
        dict(gene="MED", D_org=-0.8, A_adh=-0.75, F_dome=0.02, **base),
        # clean format gain: A ~ 0, F ~ D and significant
        dict(gene="FMT", D_org=-0.8, A_adh=-0.05, F_dome=-0.7,
             **{**base, "F_dome_p": 1e-5, "F_dome_q": 1e-4, "A_adh_p": 0.4}),
        # weak D: not a hit
        dict(gene="WEAK", D_org=-0.1, A_adh=-0.1, F_dome=0.0, **base),
        # hit but A opposite sign, F ns: unresolved
        dict(gene="UNK", D_org=-0.8, A_adh=0.3, F_dome=-0.1, **base),
        # loss reproduced in adherent: medium
        dict(gene="LOSSMED", D_org=0.6, A_adh=0.55, F_dome=0.05, **base),
    ]
    t = flag_hits(_tab(rows))
    assert t.loc["MED", "flag"] == "medium_attributable"
    assert t.loc["FMT", "flag"] == "format_candidate"
    assert t.loc["WEAK", "flag"] == "not_a_hit"
    assert t.loc["UNK", "flag"] == "unresolved"
    assert t.loc["LOSSMED", "flag"] == "medium_attributable"
    assert t.loc["MED", "ratio_A_lo"] > 0


def test_flag_symmetric_format_rule_lsm7_like():
    # LSM7-like: strong F at nominal p but genome-wide F q ~ 1 (Astra r1 #6).
    # Primary (symmetric nominal-p) rule must call format_candidate;
    # the strict-FDR variant must leave it unresolved.
    base = dict(D_org=-0.333, A_adh=-0.072, F_dome=-0.248, S_tsm=0.0,
                D_org_se=0.05, A_adh_se=0.05, F_dome_se=0.11, S_tsm_se=0.05,
                D_org_p=1e-6, A_adh_p=0.16, F_dome_p=0.037, S_tsm_p=0.5,
                D_org_q=1e-5, A_adh_q=0.4, F_dome_q=0.9999, S_tsm_q=0.8)
    t = flag_hits(_tab([dict(gene="LSM7LIKE", **base)]))
    assert t.loc["LSM7LIKE", "flag"] == "format_candidate"
    assert t.loc["LSM7LIKE", "flag_fdr"] == "unresolved"
    assert t.loc["LSM7LIKE", "ratio_F_lo"] > 0


def test_contrast2_hc3_matches_statsmodels():
    import statsmodels.api as sm
    from medium_attribution_v2 import contrast2
    rng = np.random.default_rng(3)
    n = 60
    grp = np.array([True] * 20 + [False] * 40)
    lin = pd.Series(rng.choice(["A", "B", "C"], n))
    # heteroscedastic: treated group noisier
    y = 0.5 * grp + rng.normal(0, np.where(grp, 2.0, 0.5))
    Y = pd.DataFrame({"g1": y})
    beta, se, p, n1, n0, se_hc3 = contrast2(Y, grp, lin)
    X = np.column_stack([np.ones(n), grp.astype(float),
                         pd.get_dummies(lin, drop_first=True, dtype=float).values])
    fit = sm.OLS(y, X).fit(cov_type="HC3")
    assert abs(beta["g1"] - fit.params[1]) < 1e-10
    assert abs(se_hc3["g1"] - fit.bse[1]) < 1e-8
    assert se_hc3["g1"] > se["g1"]  # HC3 inflates under group heteroscedasticity


def test_weighted_offset_ignores_missing_pairs():
    # Astra r3: NaN calibration differences must be excluded per gene
    # (gene-specific denominator), matching pandas skipna mean at w=1.
    from medium_attribution_v2_boot import weighted_offset
    d = np.array([[1.0, np.nan, 3.0], [3.0, 2.0, np.nan], [np.nan, 4.0, 9.0]])
    off = weighted_offset(d, np.ones(3))
    assert np.allclose(off, [2.0, 3.0, 6.0])
    off2 = weighted_offset(d, np.array([1.0, 1.0, 0.0]))
    assert np.allclose(off2, [2.0, 2.0, 3.0])
    # no valid pairs -> zero fallback
    off3 = weighted_offset(np.full((2, 2), np.nan), np.ones(2))
    assert np.allclose(off3, [0.0, 0.0])


def test_flag_medium_blocked_by_dominant_format():
    base = dict(D_org=-0.8, A_adh=-0.7, F_dome=-0.7, S_tsm=0.0,
                D_org_se=0.05, A_adh_se=0.05, F_dome_se=0.05, S_tsm_se=0.05,
                D_org_p=1e-6, A_adh_p=1e-4, F_dome_p=1e-5, S_tsm_p=0.5,
                D_org_q=1e-5, A_adh_q=1e-3, F_dome_q=1e-4, S_tsm_q=0.8)
    t = flag_hits(_tab([dict(gene="BOTH", **base)]))
    # both A and F reproduce D strongly: medium blocked by dominant F -> format rule needs ratio_A<0.25 -> unresolved
    assert t.loc["BOTH", "flag"] == "unresolved"
