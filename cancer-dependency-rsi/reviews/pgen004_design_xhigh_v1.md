**Endpoint adjudication: NO as pgen002 is written. Pgen004 has a credible raw-data feasibility route, but is not ready for a real policy cycle. Continue scientific generations while resolving the named accounting witnesses.** This consultation accessed metadata and existing artifacts, not raw-count outcomes.

**1. Endpoint adjudication**

TOK = input + output is a coherent resource unit. Reporting cached input and reasoning output as subcomponents avoids double counting. However, those facts do not satisfy [handoff §11](/Users/bmarti44/github/bufferright/research/cancer_rsi_handoff.txt:303).

Three objections remain:

- **Unknown, unmatched host expenditure.** Same model and effort do not establish matching of expenditure, caching, routing, retries, or learning overhead. §11 expressly prevents a token proxy from certifying C9 while material host costs remain unknown and unmatched. Unknown expenditure is not zero expenditure.
- **The failure charge is not a conservative bound.** The largest completed same-effort call does not bound a failed call. Moreover, overcharging a fixed baseline can artificially favor the learned policy. The reported **14,566,608 TOK is a charged historical total**, containing four imputations; it is not wholly measured consumption.
- **CPU measurement is not implemented as asserted.** The current [`run_bounded` result](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/budget.py:216) records wall time and RSS, but no CPU seconds. Client-process CPU measurements also do not measure hosted inference.

The additional witness required is:

1. **Either measured host expenditure**, or an authoritative accounting/contract witness establishing that host expenditure is known and strictly matched—including learning, failures, retries, routing and caching. A documented identical fixed host charge could potentially qualify; its existence cannot be assumed.
2. **Complete prospective usage accounting.** Obtain usage for failures, or enforce a genuine bound covering the entire multi-turn invocation. The nominal 2,000,000-input/50,000-output declaration is insufficient without enforcement.
3. **Conservative treatment of remaining uncertainty.** For certification, use learned-cost upper bounds and fixed-cost lower bounds. Symmetric maximum imputation alone is insufficient.
4. **A ledger-first revised SPEC**, measuring CPU/wall and other material resources, fixing the cost allocation and uncertainty procedure, followed by Sol-high ≥90 with zero unresolved high/critical issues.

This preserves the alternative-endpoint route in [discriminator v2](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/cl_rd_raw_accounting_discriminator_v2.json). It does not waive §11 or retroactively repair pgen002.

**2. Proposed pgen004 battery**

Use a new study/evaluator identity, for example `CL-RD-RAW-207-v1`. Preserve pgen003’s FAILS-SCREEN disposition.

**Universe and partitions.** Freeze the resolved subset: **251 lines, 250 patients, 810 count files**. KP3 remains excluded; full-C overlap is zero in the 142-patient Passports space. Resolve ancestry/parent relationships before locking: any additional cross-patient relatedness invalidates the proposed counts rather than triggering an opportunistic replacement.

Use an A-only reference. Do not inherit Broad `AdherentMean` without establishing that reserved donors contributed no outcomes to it. Do not use C displacement values, C results, or C-derived rewards.

A reproducible metadata-only partition is available:

- Compute SHA-256 of UTF-8  
  `CL-RD-RAW-207-v1\0<model-list SHA256>\0<eligibility-file SHA256>`.
- Take its first eight bytes as seed bytes: **`2ea967015ccfbcf7`**, unsigned big-endian **3362331852358532343**.
- Order patients by `SHA256(seed_bytes || UTF8(patient_id))`, breaking ties by patient ID.
- Assign the first **90 patients to A**, the remaining **160 to B**.
- Within A: **A0=50 fitting donors; A1=20 feasibility/E0 donors; A2=10 cycle-one donors; A3=10 cycle-two donors**.
- Assign the ordered B patients round-robin to **16 panels of 10 patients**.

The current metadata produces:

| Partition | Patients | Lines | Files | ZIP-member payload bytes |
|---|---:|---:|---:|---:|
| A0 | 50 | 51 | 168 | 424,971,538 |
| A1 | 20 | 20 | 52 | 132,613,289 |
| A2 | 10 | 10 | 27 | 68,882,593 |
| A3 | 10 | 10 | 27 | 68,876,661 |
| B | 160 | 160 | 536 | 1,358,834,183 |

PEO1/PEO4 remain together in A0. Freeze the complete manifests before count access. Release A0/A1 first; retain A2/A3 for fresh development rollouts and B until the final policy lock.

**Schema witness before bulk acquisition.** After accounting reopening and SPEC review, extract at most four A0 members, ≤16 MiB compressed, covering distinct documented filename/library layouts. Require:

- Unique guide identifiers and an authoritative guide→gene mapping.
- Explicit endpoint-count and plasmid-count roles, including library/batch correspondence.
- Documented replicate, lane and assay-time interpretation.
- Nonnegative integer counts, matching guide identities, and a retained schema report.
- At least two usable guides for every fixed coordinate under the frozen plasmid-only filter.

The listing contains **no separately named plasmid members**. Plasmids may be embedded in count files, but this remains unwitnessed. Missing plasmids or guide annotations produce `BLOCKED-DATA`; processed effects are not substitutes. Sanger documents plasmid-relative fold changes, but its documentation does not establish this archive’s column schema. [Official processing documentation](https://depmap.sanger.ac.uk/documentation/datasets/wg-crispr-knockout/)

**Frozen processing.** Subject to that schema witness:

1. Sum documented sequencing lanes belonging to the same replicate.
2. Normalize each endpoint/plasmid sample independently by library size.
3. Retain uniquely mapped guides with plasmid CPM ≥1.
4. Compute  
   \[
   LFC_{qs}=\log_2\frac{CPM_{qs}+0.5}{\operatorname{mean}(CPM_{q,\mathrm{matched\ plasmids}})+0.5}.
   \]
5. Take the median guide LFC per gene, median replicate/file score per line, then average line-level displacement vectors equally within patient.

No cross-line fitted normalization, ComBat, component removal, or B-informed filtering. Describe any mixed assay durations explicitly; this is an archival cell-line endpoint, not a matched environmental intervention.

The supplemental annotation supplies **1,788 `common_essential=true` genes** and **1,121 `core_fitness_pancan=TRUE` genes**. Freeze these as prior positive-control annotations for diagnostics. **`false` does not establish nonessentiality.** Their derivation must be checked before calling them independent controls or using them for outcome-changing calibration. They need not alter the primary LFC transformation.

**Task and attainable quality.** Retain the fixed `confirmatory207` identities. Construct an A0-only reference:

\[
a_g=\operatorname{mean}_{i\in A0}x_{ig},\qquad
r_{0g}=\operatorname{rank}_{207}(a_g),
\]

\[
D_{ig}=|\operatorname{rank}_{207}(x_i)_g-r_{0g}|/206.
\]

Use average ties. Average related lines’ displacement vectors within patient. Predict the **207-coordinate displacement vector**, scoring patient-equal, coordinate-equal MSE. Clip predictions to [0,1]; use \(q=1-\mathrm{MSE}\).

This is a conventional-cell-line engineering task. It supplies no additional external organoid validation.

Freeze these competent predictive baselines:

- A0 patient-mean displacement vector.
- Tissue means shrunk toward the global mean, shrinkage counts `{1,5,10,20,50,∞}`.
- Ridge predictors using baseline strength, measured lability, fixed annotations and tissue interactions; λ `{0.01,0.1,1,10,100}`.
- An otherwise identical, independently tuned **no-lability ablation**.

Select hyperparameters with five patient-grouped A0 folds. Recompute references within training folds for feasibility calculations.

Let \(E_0\) be A1 donor-mean MSE and \(E_*\) the best prelisted competent baseline’s A1 MSE. Before policy optimization, freeze:

\[
e_\tau=\min(0.90E_0,\;1.05E_*),\qquad \tau=1-e_\tau.
\]

Require \(E_*\le0.90E_0\), finite nondegenerate scores, and an A-only uncertainty assessment supporting useful baseline attainment. Otherwise this tested task fails its usefulness screen. Do not move τ after policy results.

**Policy comparators and cycle.** Compare:

- Fixed exploration in a predeclared family/refinement order.
- Fixed-allocation/random selection, with frozen allocation and seeds.
- A strong static strategy that starts with the A-selected competent baseline and permits ordinary local cross-validation.

Do not require unnecessary model calls for closed-form predictors.

Reserve E0’s **24 evaluated nodes**, then at most **36 fresh nodes per cycle**, for two cycles. Pgen004 would complete cycle one; pgen005 would complete cycle two. Each needs the unchanged incumbent plus ≥3 executable challengers, such as cost-aware selection, tissue-conditioned allocation, and stopping/refinement control.

Freeze challenger order, replay-support rules and promotion criteria before replay. Use recorded outcomes and exact admissible contexts only. Inadequate support invokes the predeclared fresh-rollout fallback. Retain the incumbent on failure. Metadata probes do not count as policy cycles.

**Token-savings feasibility is currently unsupported.** The plausible mechanism is avoiding genuinely expensive, unproductive generation/refinement branches. This task’s strong predictors are cheap, so that mechanism may have negligible room to operate.

Let \(S\) be shared charged TOK, \(H\) learned-policy overhead, and \(L,F\) learned/fixed deployment TOK across the actual reserved campaign. Twenty-percent savings requires:

\[
S+H+L\le0.8(S+F),
\]
or
\[
F\ge1.25(H+L)+0.25S.
\]

Run the A-only shortcut test first. **If a useful fixed baseline attains τ with zero additional hosted generation, positive learned overhead makes the proposed TOK advantage infeasible.** A retained execution demonstrating attainment and its costs is the required witness—not an assertion that small models must suffice. Failure closes this tested task/endpoint combination, not every possible policy task.

Charge shared production once per counterfactual arm and learning overhead once over **one actual deployment campaign**. Do not amortize over hypothetical future deployments.

**Acquisition and processing budget.** Selective extraction requires approximately **2,054,178,264 bytes**, versus **2,848,002,413 bytes** for the full ZIP. A0/A1 require only **557,584,827 payload bytes**.

Prefer receipted range extraction, with local-header validation, CRC verification and retained member SHA-256 hashes. Reserve **3 GiB total new raw-route transfer**, including failures and retries. Permit full-download fallback only when the measured remaining reservation covers it. A multipart ETag is not an MD5 checksum.

Stream gzip/TSV processing; the ZIP “uncompressed” sizes describe nested gzip members, not expanded TSV sizes. Reserve ≤8 GiB disk, 2 GiB RSS per processing job, ≤2 heavy jobs, and ≤600 seconds per chunk. Require a measured A0 throughput witness before reserving the remaining processing time; the eight-hour pilot ceiling remains binding.

**Precision and allocation gates.** Use A0/A1 only to estimate attainment, paired cost variability and overhead headroom. Predeclare an A-only power calculation with:

- 16 independent patient panels.
- 20% savings null margin.
- A **35% total-savings planning alternative**, explicitly an assumption.
- ≥80% estimated power using conservative A-derived variability.
- Simultaneous protection against all three fixed comparators.

For eventual B evaluation, freeze 10,000 whole-panel paired bootstrap resamples, seed **2026102804**, keeping shared/learning costs fixed and charged once. Require the one-sided lower savings bound to reach 20% against every fixed comparator. Preserve nonattainment as censoring; do not certify savings from imputed exact costs.

There is also a concrete allocation conflict: **16 panels × 3 arms already require 48 calls if each rollout invokes the hosted generator once**, exceeding phase 5’s current 20-call allocation. Witness a legitimate ≤20-call protocol or explicitly revise prospective allocations within authorized totals before Lock 1. Do not batch unrelated B histories into shared prompts merely to reduce the call count.

**3. Ranked next three generations**

| Rank | Generation | Cheapest discriminator and exact stop/go |
|---|---|---|
| **1** | **sgen001: patient identity + C6 novelty/consequence adjudication** | First reconcile the **144 locked donor IDs versus 142 Passports patients**, using metadata only. Then inspect the closest S1–S3 methods, relevant supplements/code and citation neighborhood. **GO:** authoritative identity dispositions, defensible uncertainty interpretation, and a supported substantively novel consequence under independent review ≥90/no high-critical. **Otherwise:** C6 remains PARTIAL with the exact reason; preserve the frozen result. |
| **2** | **sgen002: scientific reproduction and review package** | Reproduce from frozen retained artifacts without LLM search. Require exact IDs/counts/decisions and numerical agreement within `atol=1e-10, rtol=1e-8`; regenerate atlas, tables and figures. **GO:** verified provenance, complete coverage, reproducible available components and review ≥90/no high-critical. **Otherwise:** identify missing components explicitly. Absent donor arrays or a binding no-redecoding restriction leaves interval reproduction pending. This cannot establish the absent policy comparison. |
| **3** | **pgen004: accounting → schema → A-only headroom → first real cycle** | **GO to acquisition:** the §11 accounting witness and reviewed prospective SPEC pass. **GO to optimization:** schema, independent processing, useful attainable τ, savings headroom, precision and complete allocation feasibility pass, followed by G2/Lock 1 review. **Otherwise:** retain a scoped failure/PENDING disposition and continue another legal generation; do not spend B or manufacture a ceremonial cycle. |

The patient discrepancy deserves priority. Retained metadata map `WTSI-COLIVM_031/061` to **SIDP01937** despite different locked donor IDs, and `WTSI-COLIVM_051/090` to **SIDP01939** despite different donor IDs. These mappings require authoritative reconciliation; they do not by themselves prove which source is wrong. Any subsequent correction must preserve the original execution and cannot be presented as another independent external validation.

The campaign remains incomplete. Neither a successful metadata screen nor this proposed battery establishes C8, C9 or C13.

ENDPOINT:NO; PGEN004:NO_GO; NEXT:sgen001 patient-identity/novelty adjudication, then sgen002 frozen scientific reproduction; reopen pgen004 only on the named accounting and feasibility witnesses.