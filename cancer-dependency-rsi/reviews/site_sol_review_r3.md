SCORE: 89/100

VERDICT: Minor fixes before shipping. N1–N4 are genuinely fixed, and no data regression was found. Three verified remainders keep this below 90: causal-isolation wording, missed hover contrast, and a small CPU/shader repulsion mismatch during pointer fade. Each needs a local fix.

**PER-ITEM DISPOSITION CHECK**

Line references below are in [site/index.html](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html).

| Item | Disposition and verified evidence |
|---|---|
| Denominator | **FIXED.** Lines 442–444 correctly distinguish **135/285 gains (47%)** from **266/537 gains and losses (50%)**. |
| Causal wording | **PARTIAL — medium.** Revised headlines and F labels are improved. “Shape-only contrast” and “shape without food change” remain; see below. |
| Publication status | **FIXED.** Citation, BibTeX and Downloads identify an unpublished draft; Downloads disclose author placeholders and pending posting. |
| Flag-zero wording | **FIXED.** MAPK11’s executable verdict distinguishes statistical significance from the effect-size cutoff and displays **q<0.001**. |
| Offscreen details / **N1** | **FIXED.** Bare-root initialization uses `select("SQLE", "never", false)`: fixture recorded **zero scroll calls and zero hash writes**. Incoming ITGB1 links scroll to details. All selection call sites retain the intended argument meanings. |
| Code/source downloads | **FIXED.** Release ZIP is valid and contains analysis code/reviews. Gene details link the primary CSV. |
| Keyboard controls / **N2** | **FIXED.** All seven sortable columns, both directions, matched their comparator, arrows and `aria-sort`. Signed-column captions also matched. |
| Focus restoration / **N3** | **FIXED.** Lines 764–770 restore focus to the replacement header button. Activation followed by repeated rendering retained focus in the fixture. |
| Contrast | **PARTIAL — low.** Primary hover is fixed: white on `#b02e12` gives **6.47:1**. Other hover instances remain below threshold. |
| Visual fallbacks | **FIXED.** Forced renderer failure installs fig1, applies `no-gl` and rewrites `.gl-note` toward the explorer. Reduced-motion targets snap to integer formations; intro is complete and autonomous displacement is disabled. |
| Picking/highlight mirror | **PARTIAL — low.** Intro scaling, z-offset and drift are mirrored. Repulsion differs while mouse strength is between zero and one; see below. |
| Repeated redirect parameters | **FIXED.** Repeated, encoded and empty query values survived fixtures; www requests passed through. |
| Clipboard failure | **FIXED.** Both legacy-copy failure and rejected Clipboard API calls showed selectable text without false success. |
| Medium-gains ticker | **FIXED.** All **12 entries** match the independently filtered/ranked medium-consistent gains; HSD17B7 and AIRIM are excluded. |
| Signed ratio sorting | **FIXED.** STK38L is first ascending and last descending. |
| Paper rendering / **N4** | **FIXED.** Fixture rendered **100/100 ticks** while paper top was 200px, **0/100** at top 0, then resumed on return. Paper entry cleared the cursor. Highlight work remains one point per tick. |

**NEW ISSUES — verified remaining instances**

**CRITICAL / HIGH:** None.

**MEDIUM**

- **Causal isolation still appears in two explanations.** [Line 439](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:439) calls F the “shape-only contrast”; [line 487](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:487) says “shape without food change.” The site’s own limitations identify mixed formulations and model-selection differences. These phrases imply cleaner isolation than the comparison establishes. **Smallest fix:** use “dome-versus-adherent contrast within the organoid-medium family” and remove “without food change.”

**LOW**

- **Hover contrast has leftover failing instances.** [Line 154](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:154) makes ordinary paper links `#ff4b2e`: **2.83:1** against the paper background. [Line 168](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:168) gives popular-gene buttons white text on that orange: **3.33:1** at 12.5px. **Smallest fix:** use the existing `#b02e12` for those hover foreground/background colors respectively.

- **Repulsion applies mouse strength on opposite sides of smoothstep.** [CPU lines 959–960](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:959) calculate `smoothstep(mouseOn × falloff)`; [shader lines 1074–1075](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/site/index.html:1074) calculate `mouseOn × smoothstep(falloff)`. At `mouseOn=0.5`, distance `0.15`, the arithmetic fixture differed by **0.02154 world units**. An actual first-pointer-tick fixture produced **1.77px** projected separation. These are numerical fixtures, not browser observations. **Smallest fix:** multiply by `mouseOn` after the CPU smoothstep.

**CHECKS RUN**

- Read the prior reviews/dispositions and all current site HTML/JS, redirect, generator and tests; searched for leftover wording and hover instances.
- Ran `.venv/bin/python -B -m pytest -q -s -p no:cacheprovider tests/test_site_data.py`: **5 passed**.
- Rebuilt exports entirely in memory: **genes.json and stats.json matched byte-for-byte**. Confirmed **17,525 genes, 456 hits, 387 medium-consistent, 68 unresolved, one format candidate**, catalogue counts, ticker ranking and summary-statistic artifacts.
- Executed Node VM explorer, selection, sorting, focus, clipboard, fetch-failure and redirect fixtures.
- Executed stage fixtures using bundled Three.js math and a renderer stub, including **1,120 CPU/shader comparisons**, reduced motion, fallback and paper suspension/resumption.
- Checked formation finiteness and D/A coordinates, ZIP integrity, downloadable asset equality, local targets, duplicate IDs and contrast.

Limits: no real-browser/mobile rendering, GPU profiling or live deployment verification. No historical R2 file snapshot was available for a direct byte diff.