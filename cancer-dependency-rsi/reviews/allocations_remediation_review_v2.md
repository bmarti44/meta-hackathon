**One low finding remains; no medium or higher findings.**

**Low — exact CLI refusal assertions remain unfixed.** [test_lineage_cli.py:24](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_lineage_cli.py:24) still uses substring checks and accepts any nonzero exit. A mocked refusal `"unrelated output directory already exists"` with exit code 17 passes. Assert complete expected messages and their exit codes.

The other scoped checks pass:

- **Single source:** shadow allocations is a symlink to `config/allocations_amended_20261029.json`, resolving to the same inode.
- **Fail closed and provenance:** probes diverting allocations, resources, or ledger resolution all raise identity errors. Ledger and lock identities match canonical paths. [This call’s reservation, line 273](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/resources.jsonl:273), ID `be811e82a2484c419cdf15ece6cb77e4`, records the correct `allocations_sha256` (`e92ddf2e…`) and `allocations_source`; prompt hash, model, and high effort match.
- **Coverage:** [test_budget_shadow_root.py](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_budget_shadow_root.py:12) covers restoration pin, canonical identities, and allocation-drift failure.
- **No regression:** all **30 LOCK2 hashes match**. An in-memory fresh-call/resume probe produces exactly one reservation and matching reconciliation through `BUDGET_ROOT`. All **63 eligible pre-amendment receipts** resume without dispatch. `allocations_sha256` remains outside `call_identity`.

Validation: two read-only pytest cases passed; drift and accounting probes ran in memory. The ledger contains 136 reservations and 135 reconciliations, without duplicates or orphans; this active call is the sole outstanding reservation. No files changed.

REMEDIATION_V2_SCORE: 98