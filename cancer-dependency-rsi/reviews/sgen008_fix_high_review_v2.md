Read-only re-review: fixes improve the previous 80, but three issues prevent closure.

1. **High — C10 magnitude decision remains a substring check.** [sgen008_checks.py:55](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen008_checks.py:55) accepts `**not yes (BOUND)**` and `**yes (BOUND) rejected; final NOT_BOUND**`. I reproduced both false accepts. Sign=`no`, locked decision=`NOT_BOUND`, and the supplied contradictory fixtures are correctly rejected. Require exact equality after Markdown normalization and retain these additional negative fixtures.

2. **Medium — Cohort counts do not establish complete model membership.** [sgen008_checks.py:101](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen008_checks.py:101) now requires 148 rows and 142 patients; truncated and empty cohorts correctly fail. However, replacing `WTSI-COLO_478` with `WTSI-COLIVM_051` produces **147 unique models**, retains 142 patients, and still passes. Require unique sample IDs and exact membership against the authoritative cohort definition.

3. **Medium — Structured fresh evidence remains incomplete.** [fresh_env_evidence_v2.json:2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen008/fresh_env_evidence_v2.json:2) adds valid interpreter/lock hashes and component outcomes, but omits installation exit status/timing, per-component commands, and source/report/log hashes. Failed attempts are honestly retained under `/tmp/cdrsi_fresh`, but are not preserved as self-contained generation artifacts. Retain installation and execution records with explicit paths, hashes, elapsed times, and failure outcomes.

Verified improvements:

- Broad exposure IDs come from installed `split_manifest.json → A_development.models`; changing that input changes the computed exclusions.
- Original eligibility totals reproduce: **252 lines / 251 patients / 250 eligible patients / 251 eligible lines / 810 files**, with **148 cohort rows / 142 C patients**.
- Fresh logs/reports support completed upstream per-stage reproduction, sgen002 point/figure reproduction, OLS, and sgen008 checks. Frozen stage hashes validate.
- Interpreter and lock hashes match; installed direct dependency versions match the lock.
- I independently reproduced `evidence_report_v3.json` excluding timing and reran OLS successfully under the fresh interpreter. Upstream execution was assessed from retained evidence because its runner writes temporary artifacts.
- Interval/policy exclusions and diagnostic-only qualifications remain intact.

SGEN008_FIX_SCORE: 86