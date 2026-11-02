**C1: MET. C6 novelty component: SUPPORTED**, under the bounded “not located” qualification. The measured paired-format-lability → external gene-rank-displacement relationship remains substantively distinct from S1–S3. This does not adjudicate the other C6 requirements.

Verified: **3 tests pass**; independent reconciliation reproduces **4/7/3 omissions**, including individual Dempster and Geurts/Clevers dispositions. All 23 retained text hashes match; totals are **237,568 transferred bytes across 48 responses** and **308,583 uncompressed Python bytes**. The request deviation is ledgered, and the locked SPEC hash is unchanged.

Remaining issues:

1. **Medium — Retrospective enforcement remains overstated.** [reviews/novelty_audit_v8.md:4](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/novelty_audit_v8.md:4) still describes the executed extraction as “fail-closed” and points to the replacement helper without identifying v1. V2’s filename checks cannot retrospectively validate the 48 recorded responses. [ledger/experiments.jsonl:51](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/ledger/experiments.jsonl:51) acknowledges the overrun, but the audit does not qualify its completion wording.  
   **Fix:** explicitly state that sgen003 executed v1; distinguish receipt/hash consistency checks from enforcement guarantees; identify v2 as subsequent hardening; reference the deviation and preserve the outstanding acquisition-verification limitation.

2. **Medium — Resource ceilings remain unenforced.** [src/zipfetch.py:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/zipfetch.py:23) bounds each read to the requested length plus one, but imposes no request-count or cumulative-byte ceiling. Archive-controlled directory/member sizes can therefore authorize oversized reads. My probe reached `read(33554434)` for a request exceeding 32 MiB. Receipts record successful requests after consumption; they do not enforce allowances.  
   **Fix:** reserve request and byte allowances before dispatch, reject invalid/oversized ranges, and account for failed attempts and consumed bytes. Add boundary tests.

3. **Medium — ZIP consistency checks remain incomplete.** [src/zipfetch.py:69](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/zipfetch.py:69) ignores each directory entry’s starting disk. [src/zipfetch.py:88](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/zipfetch.py:88) omits local CRC/size comparisons and compares filenames through lossy UTF-8 decoding. In-memory probes accepted a nonzero starting disk, inconsistent local CRC/sizes with descriptor flag unset, and distinct local/directory filename bytes that decode identically.  
   **Fix:** reject unsupported disk/ZIP64/encryption metadata; compare raw filename bytes; validate local CRC/sizes when bit 3 is unset; constrain member regions before the directory. Add regression cases. Existing bounds/total, truncation/excess, EOCD-count/comment, method-mismatch, and central-CRC rejection probes passed.

4. **Low — Bibliography details still need cleanup.** [reviews/novelty_audit_v8.md:23](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/novelty_audit_v8.md:23) retains SigProfiler and older biology papers in its omission summary although they are absent from the corrected list. [omitted_refs_v2.json:116](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen003/omitted_refs_v2.json:116) truncates the Roberts DOI to `10.1111/ecog.0288`; cached XML gives `10.1111/ecog.02881`.  
   **Fix:** regenerate the summary from v2 and retain accurate structured identifiers, including the Zenodo DOI.

Review remained read-only.

SGEN003_FIX_REVIEW_SCORE: 90; C1:MET; C6_NOVELTY:SUPPORTED