The package is **not ready for Lock2**. The independent **gpt-6.1-sol, high** review verified most round-1 fixes, but found a remaining bounded-execution bypass.

Review was read-only: no downloads, edits, tests, external evaluation, Table 6 opening/decoding, or C outcome access. The reported 66-test pass was checked against the ledger, not independently rerun.

- **HIGH — Verified statically: an outstanding reservation does not establish bounded execution.**  
  [src/external_eval.py:78](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:78) accepts a single unreconciled reservation matching the job name, CPU flag and argv suffix. It does not bind that reservation to the current process, a live launcher or an active watchdog.

  Concrete failure path: reserve the job, interrupt before child dispatch, then invoke `external_eval.py` directly. With a valid Lock2 commit and no start marker, the stale reservation permits first execution and C consumption without timeout or RSS enforcement. The fixture demonstrates the underlying acceptance by reserving and then calling `ee.main(root)` directly at [tests/test_external_eval.py:92](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_external_eval.py:92).

  **Required:** bind execution to its particular reservation and supervised child; reject stale reservations and unsupervised direct invocation. Normal CLI dispatch is fixed, and an existing start marker still prevents rerunning.

- **MEDIUM — Verified code omission; power-loss consequence untested: new result-directory linkage is not synced.**  
  [src/external_eval.py:99](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:99) creates `lock_s/results`, then syncs the start file and `results` directory. It never syncs `lock_s`, which owns the newly created directory entry.

  This leaves first-execution durability incomplete: loss of that parent entry could remove the start guard after outcome access. This is a durability gap, not an empirically demonstrated APFS failure.

  **Required:** durably create the results directory, including syncing its parent, before exposure—or prepare and sync it before commitment.

- **CRITICAL:** none identified.

Round-1 verification:

1. **Invalid secondaries — FIXED.** [src/external_eval.py:159](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:159) calculates p over all B replicates, counting failures against rejection in both tails. Invalid members retain their Holm slots, report null adjusted p and never reject. The 4,600/400 regression expects `2*401/5001`; protocol wording agrees.
2. **Invalid-analysis crashes — FIXED for identified paths.** [src/external_eval.py:197](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:197) structures exclusion overflow, extraction `ValueError` and invalid kernel results. Reconstruction requires validity and checks failed-replicate agreement. Stability exceptions are isolated; invalid primaries skip stability.
3. **Single execution/persistence — SUBSTANTIALLY FIXED.** [src/external_eval.py:98](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:98) uses atomic `O_EXCL`; output commits use no-overwrite links. Process interruption during temporary writing leaves the start guard and prevents silent rerun. Parent-directory durability remains unresolved.
4. **Resource enforcement — PARTIALLY FIXED.** [src/run_external_eval.py:13](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/run_external_eval.py:13) and CLI dispatch correctly select phase6_7, CPU-heavy execution, 2 GiB and 600 seconds. The reservation bypass remains.
5. **Commit coverage — EXPANDED AS REQUESTED.** [src/external_eval.py:44](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:44) includes the stated execution dependencies, scientific inputs, configurations and dependency locks. The eventual commit must also cite the passing review and its SHA.
6. **Exclusion reporting — FIXED.** Every analysis receives analyzed model/donor counts and the full exclusion list at [src/external_eval.py:199](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:199).
7. **Access wording — FIXED.** [data/exposure_log.jsonl:14](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/exposure_log.jsonl:14) preserves history and clarifies transient text parsing versus numerical access.

Phase6_7 execution requests zero model calls and does not consume the terminal-review call reserve. D_g commits before the result JSON; interruption between them leaves an incomplete execution requiring adjudication. Production runtime and APFS crash durability remain untested.

LOCK_S_REVIEW_SCORE:88; READY_FOR_LOCK2:NO