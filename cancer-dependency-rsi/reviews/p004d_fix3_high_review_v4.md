The main accounting and cleanup fixes pass controlled probes. Two gaps remain:

1. **MEDIUM — Setup failures bypass group cleanup.** [src/tree_cpu.py:109](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/tree_cpu.py:109) starts drain threads before entering `try/finally`. Injecting `Thread.start()` failure produced **zero `killpg` calls**, leaving the launched job unmanaged. **Fix:** enter cleanup protection immediately after `Popen`; handle partially started threads during cleanup.

2. **MEDIUM — Regression coverage remains incomplete.** [tests/test_tree_cpu.py:72](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/tests/test_tree_cpu.py:72) still accepts doubled combined CPU: an injected `tree_cpu_s=0.7`, `total_local_cpu_s=1.4` passed. The six tests also lack sampling-failure-after-leader-exit coverage. **Fix:** bound the leader-exit combined total and add a failure-path test asserting `killpg` and propagation of the original error.

Verified:

- Both `pgrep` and `ps` use per-call `RUSAGE_CHILDREN` windows. A deterministic fork fixture returned **1.028 CPU-s**, rather than approximately 2.0. A real fork/wait probe using synthetic process snapshots and real sampler resource counters returned **1.192 CPU-s**, excluding **1.014 CPU-s** of job work from sampler accounting.
- Sampling failure after leader exit calls `killpg`; controlled `MeteringError`, unexpected-exception, and interruption probes passed.
- The single-process and fork tests check combined totals; the fork test rejects doubled accounting.

All six integration tests failed because sandbox restrictions block process discovery. Full live sampling accuracy remains unverified. No files changed.

METER_FIX3_SCORE: 92