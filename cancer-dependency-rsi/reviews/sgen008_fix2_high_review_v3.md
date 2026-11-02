Two issues remain before closure.

1. **Medium — Duplicate cohort rows still pass.** [sgen008_checks.py:94](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen008_checks.py:94) requires 148 distinct IDs but never requires every row to be unique. Appending one existing row produced `cohort_models=149`, `membership_ok=true`, and `pass=true`. Require `len(cohort_ids) == len(set(cohort_ids)) == 148`, alongside exact manifest membership, and retain an appended-duplicate negative fixture.

2. **Medium — Failure preservation remains incomplete.** [fresh_env_evidence_v3.json:21](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen008/fresh_env_evidence_v3.json:21) preserves two failures in the generation directory. However, the upstream failure acknowledged in [v2:39](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen008/fresh_env_evidence_v2.json:39)—`AssertionError: ('v1', 'src/estimators.py')`—still resides only in `/tmp/cdrsi_fresh/fresh_upstream.log`. Preserve and reference that attempt too.

Verified read-only:

- Exact magnitude equality accepts plain/bold `yes (BOUND)` and rejects both prior substring counterexamples. All five retained negative fixtures pass.
- Installed-manifest membership is enforced; changing `C_external.sample_ids` causes rejection.
- All three v3 report hashes, interpreter hash, and lock hash match. Installation timing is honestly disclosed as unavailable.
- The complete sgen008 report reproduces in memory, excluding timing. Six upstream stage hashes validate; all nine direct dependency versions match the lock; OLS passes under the fresh interpreter.
- Interval and policy limitations remain explicit.

SGEN008_FIX2_SCORE: 89