The independent **gpt-6.1-sol, high** review finds the package **not ready for Lock2**. Both round-2 fixes are present, but continued bounded execution has a remaining failure path.

- **HIGH — Verified statically: launcher interruption can leave the evaluator running without timeout or RSS supervision.** [src/budget.py:167](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/budget.py:167) starts the evaluator with `start_new_session=True`. The monitoring loop at [src/budget.py:173](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/budget.py:173) lacks guaranteed cleanup for `KeyboardInterrupt`; process-group termination occurs only after normal loop completion.

  Concrete path: launch normally, let the child pass `require_bounded`, then press Ctrl-C in the launcher’s terminal. The launcher receives SIGINT; the child’s separate session does not. The child can continue decoding C and computing after its watchdog disappears. Nonce cleanup at [src/run_external_eval.py:28](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/run_external_eval.py:28) does not terminate the child. The parent check at [src/external_eval.py:107](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:107) occurs only once.

  **Required:** guarantee process-group termination and child reaping when monitoring is interrupted, preserve accurate interrupted accounting, and handle ordinary termination signals consistently. Add a synthetic launcher-interruption regression proving that the child and descendants stop. Existing direct-`main` interruption coverage does not exercise this failure.

- **CRITICAL:** none identified.

Round-2 fixes and retained safeguards:

1. **Reservation bypass — FIXED for the identified pre-dispatch path; verified statically.** [src/external_eval.py:82](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:82) requires the nonce hash, exactly one matching outstanding reservation, recorded launcher parent PID, and reservation freshness. The launcher generates the nonce and records only its hash.

2. **Results-directory durability — FIXED for normal creation; verified statically.** [src/external_eval.py:123](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/external_eval.py:123) syncs `lock_s` after creating `results`, then syncs the exclusive start file and containing directory before exposure.

3. **Scientific safeguards — retained.** Invalid secondaries retain their Holm slots and cannot reject; failed bootstrap replicates count against rejection; every analysis reports exclusions. Exclusive start acquisition and no-overwrite result commitment remain present.

4. **Commit coverage — adequate for the proposed commitment.** After resolving supervision, bind every `REQUIRED` file and cite the passing review with its SHA-256.

Verification was read-only: no downloads, edits, tests, Table 6 opening/decoding, or C outcome access. [ledger/resources.jsonl:102](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/resources.jsonl:102) records **68 passed in 34.25 seconds**, without timeout or memory kill; these tests were not independently rerun. The interruption finding follows from control flow and process-session semantics; it was not reproduced experimentally. Production runtime and power-loss durability remain untested.

LOCK_S_REVIEW_SCORE:89; READY_FOR_LOCK2:NO