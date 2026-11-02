# sgen005 SPEC - complete attainable reproduction (terminal mandate 4)
Ledger-locked before work. No new outcomes.
1. Full atlas chain in isolated copy: build_atlas (v1 provisional) -> v2 -> v3 -> v4 from
   manifest-hashed inputs. Frozen-code route: use artifacts/sha256 retained bytes where current
   code differs from manifest hashes; every substitution recorded. PASS iff final v4 CSVs
   byte-identical to retained atlas/v4; any stage divergence reported stage-wise (no silent fix).
2. Upstream C10 + eligibility checks executed by the runner (not by citation).
3. Fresh environment: attempt `uv sync --locked` in the isolated copy (network/cache bounded
   900 s) and rerun the focused reproduction + tests under it. Failure (offline/cache) recorded
   as environment limitation, never as pass.
4. Synthetic data-use audit: label mechanical vs substantive synthetic uses (donor-kernel
   calibration = code diagnostic).
Explicitly excluded: donor/patient interval reproduction and policy comparison (absent arrays/
cycles) - C11 cannot become MET here. Report destinations exclusive-create; figure isolated.
