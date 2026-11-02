# pgen004d SPEC (screen 1 only) - accounting + total-local-CPU metering discriminator
Parents: W1+W2+W3+W5 (sol-xhigh gen_recombine_xhigh_v1). Ledger-locked before work.
NO raw acquisition, NO policy optimization in this screen.
Witness A (host expenditure): exhaust locally available authoritative sources for per-call
gpt-6.1-sol expenditure via codex route (CLI status/help surfaces, config presence without
secret values, receipt fields). PASS only on measured per-call expenditure or an authoritative
strict-matching contract covering generation/review/failures/retries/routing/caching entire
invocations. Token counts, list prices, equal ceilings = FAIL (established).
Witness B (total local CPU): implement prospective scoped metering OUTSIDE LOCK2-pinned bytes:
process-tree CPU for controller+descendants+failed jobs, no omission/double-count by design
(single process-group sampling), validated against known CPU burns (single + multi-process,
target: recovered within 25% at >=1 CPU-s scale; unrelated-process contamination probe).
Verdicts: BOTH_WITNESSED (proceed schema screen under new SPEC) / METERING_ONLY (route to
sgen006 per xhigh instruction) / NEITHER. Budgets: <=5 host calls total generation (this screen
uses 0-2 reviews), <=18000 CPU-s ceiling (screen target <<), 0 new transfer bytes.
