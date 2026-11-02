SCORE: 76/100

VERDICT: The data export is accurate, and the visual concept and audit-history narrative are strong. This needs material corrections before shipping: the opening copy broadens the audited population and turns observational consistency into causal conclusions, citations present an unposted draft as a preprint, and the explorer mislabels thousands of statistically significant results. Navigation, accessibility, and particle interaction also need targeted fixes. None requires a framework rewrite.

ISSUES:

**CRITICAL**

None verified.

**HIGH**

- **The headline changes the denominator.** [site/index.html:311](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:311), also OG description at line 12. “About 85% of the ‘organoid-specific’ weak spots” suggests the published catalogues overall. Verified: **387/456 = 84.87% of this audit’s qualifying differential dependencies**; Broad published gains are **135/285 = 47.37%** medium-consistent, and Sanger headline genes are **5/16** present. Readers can leave with a substantially broader conclusion. **Smallest fix:** explicitly attach “of the 456 differential dependencies identified in our reanalysis” to the headline and OG claim.

- **The story asserts causal separation that the audit does not establish.** [site/index.html:325](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:325), lines 330–342 and 412–414. Verified wording includes “Same cells,” “the control experiment,” “the medium alone reproduces the effect,” and “fully explained by the medium.” The manuscript describes **different model populations, nine adherent comparators, and mixed formulations**. Also, the 387 classifications do not mean 387 points lie on equality: their A/D ratios range **0.500245–1.92275**. These claims contradict the scoped methods disclaimer. **Smallest fix:** use “medium-consistent under our criteria,” identify the observational comparison, and describe the diagonal as A=D rather than causal proof.

- **Publication status and PDF readiness are misrepresented.** [site/index.html:585](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:585), lines 594, 605 and 612; `site/assets/manuscript_v2.pdf`, page 1. Citations say “Technical note preprint,” while Downloads references a bundle “accompanying the preprint.” The PDF contains **“[AUTHORS - to be completed by submitting author]”**, “[Affiliations]” and “[name, email].” There is no visible warning that posting remains pending. **Smallest fix:** label it an **unpublished draft**, explicitly disclose author placeholders, and make both copyable citations reflect that status.

- **“No significant difference” is false for 7,569 genes.** [site/index.html:637](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:637), line 660. Flag zero means failure of the combined **q<0.01 and |D|≥0.25** hit rule. I counted **7,569 flag-zero genes with q<0.01**. For example, MAPK11 has **D=−0.207602, q=4.223×10⁻³⁶**; the rendered verdict says “no significant … difference … q=0.00.” This directly misinforms gene searches. **Smallest fix:** say “Does not meet the audit’s differential-hit threshold,” distinguish the effect-size cutoff from significance, and format small q-values appropriately.

**MEDIUM**

- **Gene details open outside the viewport.** [site/index.html:880](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:880), also lines 741 and 799. Initial `#gene=ITGB1` loading selects ITGB1 with **zero scroll calls**. Table and scatter clicks also call `select(..., false)`, although the detail panel sits above the table. Deep links therefore land on the story, and lower-row/scatter clicks can appear ineffective. **Smallest fix:** scroll to details for incoming gene links and explicit selections; move focus appropriately for keyboard activation.

- **The promised code/provenance download is absent.** [site/index.html:551](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:551), lines 699–700 and 604–613. “Full code in Downloads” leads to five items containing no code or review bundle. The alternative references an unposted preprint’s repository bundle without linking it. Gene details likewise mention the source table without linking directly to it. **Smallest fix:** publish/link the existing release bundle or repository and add a direct primary-table link inside each gene detail.

- **Browsing and sorting are mouse-only.** [site/index.html:734](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:734), lines 741 and 810. Gene rows and sortable headers have click handlers but no native controls, focusability, or keyboard activation; headers lack `aria-sort`. The hidden progress rail also remains tabbable because line 83 only changes opacity and pointer events. **Smallest fix:** make gene names links, put buttons in sortable headers with `aria-sort`, and hide/inert the rail when inactive.

- **Several small-text combinations fail normal-text contrast.** [site/index.html:114](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:114), lines 185–186. Recomputed ratios: white on the hot CTA **3.33:1**, unresolved badge **3.86:1**, and no-difference badge **3.27:1**. These use 14px or 10.5px text. Verdicts and the primary search CTA become harder to read. **Smallest fix:** darken these backgrounds or use sufficiently dark text.

- **Visual fallbacks are incomplete.** [site/index.html:1196](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:1196). A WebGL initialization failure only logs a warning; the story keeps promising live points and hover interaction without an alternate visual. Reduced motion disables idle sway/pulse but retains scrubbed formation morphing, chapter translations and mouse repulsion. **Smallest fix:** reuse an existing static figure for unavailable WebGL and provide a stationary presentation for reduced motion, with matching instructions.

- **Picking/highlights use different positions from the shader.** [site/index.html:1025](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:1025), lines 1030–1033 and 1083–1097. The shader adds idle displacement and up to **0.38 world units** of repulsion; CPU picking omits both, along with introductory scaling. A source-arithmetic fixture at 1440×900 produced **43px** separation for SQLE, exceeding the **30px** pick radius. This is a numerical fixture, not a browser observation. **Smallest fix:** disable decorative displacement in the data formation and synchronize picking/highlight positions wherever displacement remains.

**LOW**

- **Apex redirects discard repeated query parameters.** [site/apex_redirect.js:8](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/apex_redirect.js:8). A valid event representing `?x=one&x=two` redirects to **`?x=one`**. The function reads only `.value`, ignoring AWS’s documented `multiValue` representation. Ordinary apex redirects and www passthrough worked. **Smallest fix:** serialize every `multiValue` entry when present. [AWS event schema](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/functions-event-structure.html)

- **Clipboard fallback reports success after failure.** [site/index.html:653](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:653). With `execCommand("copy")` returning `false`, the button still changes to **“Copied ✓”**. **Smallest fix:** check the boolean result and expose selectable text or a failure message.

- **The “top medium gains” list contains unresolved genes.** [src/build_site_data.py:90](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/build_site_data.py:90). `top_medium_gains` selects all negative-D hits. Verified members **HSD17B7 and AIRIM are unresolved**, yet this list supplies the main ticker. **Smallest fix:** filter by `medium_attributable` before ranking.

- **Reproduction-ratio sorting ignores sign.** [site/index.html:731](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:731). The universal absolute-value comparator puts **STK38L, A/D=−34338.1**, first when sorting all genes by “Reproduced flat.” Opposite-direction reproduction is treated as strongest reproduction. **Smallest fix:** use signed ordering for `rA`; retain magnitude ordering for effect columns.

- **Rendering work continues behind the paper sections.** [site/index.html:1167](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:1167), line 1187. After a highlight is set, every tick recomputes all **17,525 CPU positions**, including in paper mode, and rendering continues. The work is verified; battery/frame-time impact is inferred and was not profiled. **Smallest fix:** compute only the highlighted point and suspend stage rendering when fully covered.

CHECKS RUN:

- Read all 1,301 lines of `site/index.html`, the generator, redirect function, manuscript, FINDINGS and relevant STATUS history.
- Used Python/pandas recomputations to compare **all 17,525 records**, exported fields, flags, raw D values and bootstrap frequencies: **zero mismatches** at published precision.
- Independently rebuilt both flag variants and HC3 sensitivity. Confirmed **456 hits, 387 medium-consistent, 249 gains, 207 losses, 68 unresolved, one format candidate**; HC3 fractions **203/249=81.53%**, **156/207=75.36%**.
- Verified spot records:

  | Gene | D | A | F | Primary flag |
  |---|---:|---:|---:|---|
  | SQLE | −0.830 | −0.894 | +0.044 | Medium-consistent |
  | ITGB1 | −0.324 | −0.112 | −0.160 | Unresolved |
  | LSM7 | −0.306 | −0.047 | −0.246 | Format candidate |

- Rebuilt catalogue tags from Broad CSV and Sanger spreadsheet: **285 gains, 252 losses, 17 strict gains, 16 headline genes, 93 exclusive genes**; zero tag mismatches. Confirmed Broad **47%/87%** and Sanger **8/16, five medium, three unresolved**.
- Matched bootstrap **0.89814 [0.81641, 0.98818]** to stats/manuscript; recomputed held-out slope **0.963379** and correlation **0.974132**. Confirmed bootstrap ≥50% frequency fraction **72.15%**.
- Used Node VM checks to parse all inline JavaScript and classic vendor scripts; exercised explorer initialization, sorting, fetch failure, clipboard failure and redirect events with stubs.
- Executed formation construction: all buffers finite, **69 survivors**, diagonal coordinates match published D/A within Float32 precision, and **no current values activate the clamps**.
- Checked local HTML asset/fragment targets and duplicate IDs: no missing targets or duplicates. Canonical/OG and generated site links use www; no user-facing apex URLs found.
- Visually inspected all three figures; extracted the seven-page PDF and verified author placeholders. Measured `genes.json` at **3.43 MB**, approximately **0.79 MB gzip**.
- No real-browser/mobile rendering, GPU profiling, or live DNS/TLS/CloudFront deployment check was performed.