Choose **one bounded metadata feasibility probe of the official 26Q3 release**. Its discriminating question is: **Are there additional, independently identified organoid donors that can support development and reserved evaluation of the frozen displacement endpoint, without using C?**

This is the cheapest remaining plausible route. The [first-party staff update](https://forum.depmap.org/t/organoid-dependency-data/4671/7) identifies `CRISPRGeneEffect` and `Model.csv` as containing organoids. The packet does not establish their file routes, eligible donor counts, or independence. A metadata query must establish those facts.

Additional within-donor 2D measurements or raw replicate counts are not automatically necessary: the target is displacement from the **fixed 2D consensus**. Independently sampled organoid donors with suitable processed measurements could suffice. Requiring unavailable raw counts would prematurely exclude that possibility.

**Exact next SPEC:** proposed `reviews/prompts/g2_task_route_probe_v1.json`.

1. **Purpose and status.** Pre-Lock1, metadata-only feasibility experiment. Keep `q=null`, `admissible_for_policy=false`, G2 FAIL, and C outcomes quarantined. No generations, scientific scoring, or dependency-matrix download.

2. **Resource envelope.** One CPU job, at most 1 GiB reserved memory, 300 seconds total, six network requests total, 30-second request timeouts, and 32 MiB transferred. Zero metered spend. Record actual consumption against existing allocations; these are additional restrictions within the unchanged campaign ceilings.

3. **Primary route.** Start from the supplied official staff post and follow its authoritative release links. Obtain the release manifest and metadata-only model/donor information. Record resolved URLs, release identity, retrieval status, hashes, schema, file sizes, access terms, and metadata column mappings. Retrieve only explicitly metadata-only resources. If establishing eligibility requires opening numeric dependency outcomes, return `UNRESOLVED`.

4. **Required metadata witness.** Produce a table establishing:
   - Eligible organoid model IDs and documented biological donor IDs, with duplicate models nested under donors.
   - Overlap with all 148 C models/144 donors and the six Broad input models. Unresolved donor identity means unknown independence.
   - Availability of the genes, ranking universe, and other inputs required by the frozen endpoint.
   - Whether processing and reference construction can proceed without C outcomes or quantities fitted from them.
   - Enough eligible independent donors to construct the original development/reserved-panel structure and meet its precision requirements. Record counts and constraints; do not invent adequate sample sizes or count gene splits as biological replication.

5. **Outputs.** A proposed `reviews/g2_task_route_probe_v1.json` containing the evidence table, request/resource ledger, exclusions, and exactly one verdict:
   - `CANDIDATE_FOUND`: every structural requirement has documented support.
   - `INELIGIBLE`: an authoritative, sufficiently complete inventory establishes a specific failure.
   - `UNRESOLVED`: access, provenance, coverage, or independence remains unknown.

`CANDIDATE_FOUND` authorizes drafting a new prelock contract for review. It does not clear G2 or authorize outcome access.

The candidate **real-data quality endpoint** should be prediction error for the existing biological quantity. For eligible development donor \(d\) and fixed gene \(g\), let \(D_{dg}\) be displacement computed using the frozen endpoint rules. A workflow trained only on development data predicts donor-population mean displacement \(\hat\mu_g\). On a donor-disjoint reserved panel, use

\[
q=-\frac{1}{|B|}\sum_{d\in B}
       \frac{1}{207}\sum_g(\hat\mu_g-D_{dg})^2.
\]

Average nested models within donors first. Predictions must respect the endpoint’s bounds. This rewards accuracy on real biological measurements; it rewards neither association magnitude nor significance. Genes supply coordinates of each donor’s loss, not independent sampling units.

Freeze that loss, panel membership, baselines, quality margins, uncertainty procedure, and access schedule **before reading new outcomes**. Baselines must include the development donor mean for each gene, alongside the applicable fixed author and baseline-strength procedures. Omitting that simple, strong predictor would make apparent improvement unpersuasive.

This development task remains subordinate to the unchanged confirmatory association: `confirmatory207 / mean_abs_delta / base_strength`, with the existing external donor-bootstrap procedure. Predictive performance supplies no replacement biological success claim.

There is also a substantive feasibility test: a small prediction problem may offer no material practical savings over its strongest simple baseline. Before policy generations, the new specification must establish a credible path to the original meaningful-quality and matched-all-in-savings requirements. If it cannot, reject the task despite available data.

The **single fallback**, within the same request/time/transfer envelope, is the publication-declared official **“NextGen Model Manuscript2026” file-set manifest**. A metadata query must establish its route. Apply exactly the same eligibility test. If it contains only already counted donors, it contributes no independent panels.

The cached `29472362` manifest already establishes its relevant limitations. Extended Figure 9’s additional measurements on the same five biological models cannot supply donor-independent reserved panels. Neither warrants an outcome download for this blocker.

**Stop criterion:** stop this acquisition branch when the primary route and the one fallback either fail eligibility or remain unresolved within the envelope. Also stop if documented eligible counts cannot meet the original partition/precision requirements, or if the resulting task cannot plausibly deliver the required meaningful quality and material all-in savings. Record the precise unmet condition; do not infer global dataset nonexistence from a timeout.

My assessment is **negative expected value for outcome downloads or policy generations now; modest positive value for this one metadata probe**. If it yields no qualifying witness, invoke the prescribed unmet-gate terminal process. The full goal remains unmet: G2, two real policy cycles, supported new biology, independent external evaluation, material host-cost accounting/C9, and full-campaign reproduction/C11 remain outstanding. Synthetic calibration PASS and the 91/100 code review do not discharge them.