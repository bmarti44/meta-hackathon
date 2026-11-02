# pgen002 Amendment 1 — metadata source version correction (before probe v2)
Probe v1 used model_list_latest.csv.gz from cog.sanger.ac.uk, which is a stale 2021 build
(last-modified 2021-04-27; max sampling_year 2018; maps only 33/148 C HCM-SANG models).
The current dated product on the same official route is model_list_20260921.csv
(957,555 bytes, HEAD 200). Probe v2 uses the dated file; join normalization additionally
splits synonyms on ';' and '|' (observed separators). Pass bar, budgets, and all other
SPEC terms unchanged. Probe v1 results retained as FAILING witness (criterion 3 unwitnessed:
C-overlap removal incomplete under stale list); v2 reruns all receipted requests.
