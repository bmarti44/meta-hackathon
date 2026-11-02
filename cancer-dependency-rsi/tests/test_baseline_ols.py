import baseline_ols

def test_published_coefficients_reproduce_exactly():
    import pandas as pd
    ours = baseline_ols.fit()
    pub = pd.read_csv("data/raw/broad_figshare/minipool_regression_coefficients.csv", index_col=0)
    for ours_term, pub_term in baseline_ols.TERMS.items():
        diff = (ours.loc[ours_term].astype(float) - pub.loc[pub_term].astype(float)).abs().max()
        assert diff < 1e-6  # published CSV rounding; observed max 1.8e-8, (pub_term, diff)
