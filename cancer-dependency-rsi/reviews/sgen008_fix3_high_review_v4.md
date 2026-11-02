- Membership enforces `len(cohort_ids) == len(set(cohort_ids)) == 148`. Baseline matches `evidence_report_v5.json`; an appended duplicate produces 149 rows and fails both membership and eligibility.
- `fresh_upstream_attempt1.log` preserves the upstream traceback and is referenced in `fresh_env_evidence_v3.json`.
- `tests/test_sgen008_fixtures.py`: **1 passed**. Remaining gap: it covers C10 decisions but has no retained duplicate-membership regression test; I verified that case in memory.

Review completed read-only.

SGEN008_FIX3_SCORE: 95