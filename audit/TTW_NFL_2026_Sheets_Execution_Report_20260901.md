# TTW NFL 2026 — Phase 4 Google Sheets Execution Report (2026-09-01)

**Intended promotion version: v1.4.** Nothing was promoted. The authoritative live Sheet (`1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`) was **not opened for editing, not copied into, and not changed**. PR #1 remains a draft. The authoritative workbook SHA-256 is unchanged at `79923992e9cfe156af47207b1756010af9a375592997be8e194bc75e4e9d313f`, and the candidate SHA-256 is unchanged at `8be3b9511a6fadf6d723d8ce7f0001198f1b4423bf1162c77316fda918f442cb`.

---

## 1. Verifier repaired (Phase 4 item 1)

Both `or True` escape paths are gone (`grep -c "or True"` → **0**). Two checks now assert real conditions:

- **`settings_unchanged_core`** verifies seven values by exact label: Current season **2026**, Current week **1**, As-of date **2026-09-01**, Enable BET labels **Y**, ATS BET **1.5**, ATS INVESTIGATE **1.5**, ATS LEAN **1.0**. A missing label reports `<label missing>` rather than passing.
- **`weights_unchanged_A040_B035_C025`** now tests the triple `(H, M, R) == (0.4, 0.35, 0.25)` for every one of the 32 rows and names any offending team; it reports `32/32 rows exactly 0.4/0.35/0.25`.

**Mutation test — the repaired checks have teeth.** A throwaway copy with SETTINGS ATS BET set to 3.0 and PRESEASON M5 set to 0.30 produced 5 failures with exact diagnostics (`ATS BET at >=: got 3.0 want 1.5`; `ARI row 5: A=0.4 B=0.3 C=0.25`). The candidate was restored bit-for-bit afterwards (SHA re-verified).

Refreshed totals: **verifier 37 checks / 0 failed**, gates PASS, monitor validator PASS, linkcheck PASS, `tests/run_tests.py` **40/40**, `git diff --check` clean.

---

## 2. PR #1 scope narrative corrected (item 2)

Updated to the measured current values: **16 commits, 107 files changed, 10,329 insertions, 0 deletions**, against a `main` that holds exactly one file. Corrected in `TTW_NFL_2026_Candidate_Verification_20260901.md` §6 and in the PR body.

---

## 3. What was executed natively, and what could not be

| Item | Status |
|---|---|
| 3–4, 6 — import the **full 22-tab candidate** as a native Sheet and reconcile ENGINE/DASHBOARD | **NOT EXECUTABLE** in this environment — see §3.1 |
| 5 — the five DAL/NYG pins | **EXECUTED NATIVELY — all five confirmed** (§5) |
| 7 — the exact formula under four states | **EXECUTED NATIVELY — all four confirmed** (§4) |

### 3.1 Why the full workbook could not be imported

The Drive tooling available here exposes only file-level operations. `update_file` accepts **title and parent only** — there is no cell-level Sheets write API. `create_file` takes content **inline** as `textContent` or `base64Content`; the candidate is 1,349,730 bytes → 1,799,640 base64 characters, far beyond what an inline tool argument can carry, and no chunked or resumable upload is exposed. `copy_file` can duplicate the live Sheet but cannot apply the candidate's two change sets to the copy.

So a native duplicate of the whole workbook could not be created from here. Rather than skip the test, the two claims that actually needed native execution — the blank-preservation fix and the DAL/NYG pins — were executed natively on purpose-built disposable Sheets, below. The structural claims (22 tabs, MARKET LINES / QB VALUES / ADJUSTMENTS / PRESEASON MONITOR preservation, formula count, byte-identical drawings) remain proven at the **file level** by the Phase 3 verifier's 37 checks; they are not re-provable natively without the import. **The owner still needs to open the candidate in Sheets once** to confirm the whole-file behaviours in §7.

### 3.2 A tooling quirk worth recording

`read_file_content` renders formula cells as **blank**, which initially looked like "formulas did not import". A minimal probe (`=1+1`) disproved that: formulas import and evaluate correctly, but only `download_file_content` with `exportMimeType: text/csv` returns **computed values**. All evidence below therefore comes from the CSV export path.

---

## 4. Item 7 — the exact formula under four states, executed by Google Sheets

**Disposable probe Sheet ID:** `1inj6XOyeCZflxkguPaMEyfhlNAjul5wBXEkZvl9r-pY`
**Title:** `TTW_NFL_2026_DISPOSABLE_PROBE_BlendFix_20260901` · created **2026-09-01T13:27:08Z**, read back **2026-09-01T13:52Z**
Raw evidence committed at `audit/TTW_NFL_2026_Sheets_Probe_Results_20260901.csv`.

The probe carries the production formulas verbatim — the old D, the fixed D, and the **unmodified** H fallback `IF(AND(D="",C=""),"",IF(D="",C,ROUND(G*IF(C="",0,C)+(1-G)*D,2)))` — with prior = −1.07 and blend weight 0.8.

| State | OLD_D | NEW_D | H via OLD | H via NEW | ISNUMBER | TYPE |
|---|---|---|---|---|---|---|
| **GP=0**, governed returns `""` | **0** ← defect | *(blank)* | **−0.86** = 80% of prior | **−1.07 = 100% prior** ✓ | FALSE | 2 (text) |
| **GP>0**, governed = 1.234 | 1.23 | **1.23** | −0.61 | **−0.61** ✓ *(blend intact)* | TRUE | 1 (number) |
| **Truly empty** governed cell | **0** ← defect | *(blank)* | **−0.86** | **−1.07 = 100% prior** ✓ | FALSE | 1 |
| **Missing team** (`#N/A`) | *(blank)* | *(blank)* | −1.07 | **−1.07** ✓ | FALSE | 16 (error) |

**This is the confirmation Phase 3 explicitly could not give.** Google Sheets reproduces the defect on *both* coercion paths — a formula-blank **and** a truly empty cell both come back as numeric **0** through `ROUND(INDEX(...),2)`, dragging the Week-1 rating to 80% of the prior. The `ISNUMBER` guard returns FALSE in every non-numeric state and TRUE only for the genuine number, so the fixed formula yields blank exactly when it should and the untouched H fallback then delivers 100% preseason prior.

Two details worth keeping: `TYPE` = 2 for the formula-blank confirms Google is holding **text** (an empty string) in that cell, which is precisely why the numeric coercion is silent; and for the truly-empty cell `TYPE` reports 1 while `ISNUMBER` still reports FALSE — the fix relies on `ISNUMBER`, which is correct in both states.

No `#REF!`, `#VALUE!`, or `#DIV/0!` appeared anywhere in the probe. The single `#N/A` is the deliberate missing-team case and is caught by the formula's own `IFERROR`, exactly as designed (`TYPE` 16 confirms the underlying error was raised and handled).

---

## 5. Item 5 — the five pins, confirmed natively

Computed by Google Sheets in the same probe, from the real 32-team data using the production PRESEASON `J`/`S` formulas and the production ENGINE bridge:

| Pin | Required | Google Sheets result | ✓ |
|---|---|---|---|
| DAL prior / effective | −1.07, rank 22 | **−1.07, rank 22** | ✓ |
| NYG prior / effective | −1.90, rank 24 | **−1.90, rank 24** | ✓ |
| DAL@NYG FinalMargin | +0.77 | **0.77** (AwayEff −1.07, HomeEff −1.90, NDiff −0.83, HFA 1.6) | ✓ |
| Fair line | NYG −0.8 | **`NYG -0.8`** | ✓ |
| Edge vs market DAL −2.5 | +3.27 NYG | **3.27**, side **`NYG +2.5`** | ✓ |

---

## 6. Item 6 — reconciliation

**Reconciled natively:** all 32 teams' centered Source B, effective A+B prior, GP=0 effective rating and rank, plus the DAL@NYG ENGINE bridge. Google's results are **identical, value for value, to both the candidate workbook and `TTW_NFL_2026_Preseason_Prior_Shadow_20260901.csv` — zero mismatches across 32 teams**. Three independent implementations (the shadow generator, the candidate workbook, and Google Sheets itself) now agree exactly.

That also natively confirms four of the item-4 checks: Source B populated for all 32, GP=0 effective = prior for all 32 (F = H = J), the blend fix behaving as intended, and no errors in the recomputed layer.

**Not reconciled natively:** the remaining 15 ENGINE/DASHBOARD rows. Their inputs (market lines, HFA, QB adjustments, rest, manual adjustments) are unchanged by the candidate and were verified preserved cell-for-cell at the file level, and all 16 games are recomputed in `audit/TTW_NFL_2026_Candidate_Week1_Slate_20260901.csv` — but only DAL@NYG has been executed by Google. Confirming the other 15 requires the full-workbook import in §7.

---

## 7. Owner steps that still require a real duplicate

Open the candidate once in Sheets (File → Import → *Create new spreadsheet*, or upload the .xlsx to Drive and open it) and confirm:

1. **22 tabs** present, including the live-only PRESEASON MONITOR.
2. TEAM RATINGS **D5:D36 render genuinely blank** (not 0) and **F = H = J** for all 32 rows — §4 makes this the expected outcome.
3. GP = 0 for all 32; Source B populated with Sources Used = 2; **Source C blank**; WinTotalsMode **VALIDATE-ONLY**; Enable BET labels **Y**; ATS BET and INVESTIGATE both **1.5**.
4. No `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!` or circular-reference warnings after full recalculation. *(Note: `CALC!B39:B43` and `DATA QUALITY!B8` carry pre-existing `#DIV/0!` from empty-range AVERAGE at zero games — documented in `audit/DQ_DIV0_Diagnosis.md`, present in production today, and unrelated to this candidate.)*
5. MARKET LINES, QB VALUES, ADJUSTMENTS and PRESEASON MONITOR unchanged.
6. The remaining 15 ENGINE/DASHBOARD rows match the slate CSV.

---

## 8. Rollback plan

Nothing needs rolling back today — no production artifact was touched. Should the candidate later be promoted:

| Scenario | Action |
|---|---|
| **Before promotion (now)** | Nothing to undo. Delete the two disposable probe Sheets whenever convenient (§9); they are not referenced by anything. |
| **Candidate imported to Drive for review, then rejected** | Trash the imported copy. The authoritative Sheet was never involved. |
| **Promoted to the live Sheet, then needs reverting** | Restore via Google Sheets **File → Version history** to the version timestamped before promotion. The pre-promotion state is independently reproducible from `TTW_NFL_2026_LIVE_EXPORT_20260901_BASE.xlsx` (SHA `39c7c567…`), committed in this repo — re-import it if version history is unavailable. |
| **Only part of the change needs reverting** | The two change sets are independent. To undo **Source B**, clear PRESEASON I/K/L rows 5–36 — the priors return to Source-A-only. To undo the **blend fix**, restore D5:D36 to `IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),"")`. Both are listed cell-by-cell in `audit/TTW_NFL_2026_Candidate_Changed_Cells_20260901.csv`. |
| **Repo-side** | The candidate rebuilds byte-identically from the committed base export via `scripts/build_srcb_blendfix_candidate.py`; the authoritative workbook is SHA-pinned in `tests/run_tests.py`, so any accidental modification fails the suite. |

---

## 9. Disposable artifacts created

Both are throwaway test Sheets in the owner's My Drive. Neither is referenced by any model, script, or report input; both may be trashed at any time.

| Purpose | Title | ID | Created |
|---|---|---|---|
| Formula-state + pins probe | `TTW_NFL_2026_DISPOSABLE_PROBE_BlendFix_20260901` | `1inj6XOyeCZflxkguPaMEyfhlNAjul5wBXEkZvl9r-pY` | 2026-09-01T13:27:08Z |
| Tooling sanity probe | `TTW_NFL_2026_DISPOSABLE_PROBE_MINIMAL_20260901` | `1O6niXzSKW-Yis5kVljqnU1xegHXsGDjUiZuHDRN3Z-I` | 2026-09-01T13:43:16Z |

They were left in place so the evidence in §4–§6 can be inspected directly rather than taken on trust.

---

## 10. Status

**Stopped for final owner approval.** Intended promotion version **v1.4**. The candidate's internal banner still reads v1.1 and no CHANGELOG entry was added — deliberately, since Phase 4 authorized no candidate edits; both are owner actions at promotion time.
