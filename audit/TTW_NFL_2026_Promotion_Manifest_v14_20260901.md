# TTW NFL 2026 — v1.4 Promotion Manifest (2026-09-01)

**STOPPED FOR OWNER REVIEW. Nothing in this document has been applied.** The authoritative live Google Sheet (`1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`) is unchanged, PR #1 remains a draft, and the disposable probe Sheets are untouched.

## Checksums

| Artifact | SHA-256 |
|---|---|
| **Release candidate** `TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx` | `a71e8ba3356fe456d678eb2db75ec67ddfdbe287e743cc9901600cf57c97e22e` |
| Base (read-only live export, 2026-09-01T04:25Z) `TTW_NFL_2026_LIVE_EXPORT_20260901_BASE.xlsx` | `39c7c567364234068245e68d0af943ca71e4a128b652f57cec258d40ac1e3f35` |
| Authoritative workbook (untouched) `…v1.1_AUTHORITATIVE.xlsx` | `79923992e9cfe156af47207b1756010af9a375592997be8e194bc75e4e9d313f` |

The candidate rebuilds **byte-identically** from the base via `scripts/build_srcb_blendfix_candidate.py` (verified this phase), so the checksum is reproducible rather than asserted.

> The Phase 3/4 candidate carried SHA `8be3b951…`. Phase 5A added only the version banner and one CHANGELOG row, which is why the checksum moved. Every SHA reference elsewhere in the repo has been updated to `a71e8ba3…`.

---

## 1. What a human actually enters — 133 cells

Full per-cell listing with before/after values: **`audit/TTW_NFL_2026_Promotion_Manifest_v14_20260901.csv`** (359 rows).

| # | Sheet | Range | Action | Before | After |
|---|---|---|---|---|---|
| 1 | PRESEASON | `I5:I36` | Paste 32 values | blank | Equal-weight VSiN p29 / ESPN FPI composite (e.g. ARI 6.059, DAL 12.9395, NYG 10.236) |
| 2 | PRESEASON | `K5:K36` | Paste 32 text cells | blank | Source citation (identical string in all 32 rows) |
| 3 | PRESEASON | `L5:L36` | Paste 32 text cells | blank | `2026-09-01` |
| 4 | TEAM RATINGS | `D5:D36` | Replace 32 formulas | `=IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),"")` | `=IFERROR(IF(ISNUMBER(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0))),ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),""),"")` |
| 5 | START HERE | `A1` | Edit text | `TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)` | `TO THE WINDOW — NFL POWER RATINGS 2026 (v1.4)` |
| 6 | CHANGELOG | `A7:D7` | Add one row | blank | `1.4` / `2026-09-01` / change text / backtest-impact text |

Row 4 is fill-down safe: the formula uses relative row references, so entering it in `D5` and filling to `D36` reproduces all 32 exactly.

## 2. What changes on its own — 226 cells, do **not** type these

| Sheet | Range | Effect |
|---|---|---|
| PRESEASON | `J5:J36` | SrcB centered — blank → centered composite |
| PRESEASON | `S5:S36` | Effective prior — Source-A-only → A+B renormalized (DAL −2.82 → **−1.07**, NYG −1.99 → **−1.90**) |
| PRESEASON | `T5:T36` | Sources used — `1` → `2` |
| TEAM RATINGS | `D5:D36` | `0` (coerced) → **blank** |
| TEAM RATINGS | `F/H/J5:J36` | Prior, blended base and EFFECTIVE RATING all become the prior (GP=0 → 100% prior) |
| TEAM RATINGS | `K5:K36` | Rank — 27 of 32 move (DAL 27 → **22**, NYG stays **24**) |
| ENGINE / DASHBOARD | all 16 Week-1 rows | Recomputed; see `audit/TTW_NFL_2026_Candidate_Week1_Slate_20260901.csv` |

## 3. Explicitly unchanged

Source C blank in all 32 rows · `WinTotalsMode` = VALIDATE-ONLY · source weights A 0.40 / B 0.35 / C 0.25 · Week-1 blend weight 0.80 · ATS BET 1.5 / INVESTIGATE 1.5 / LEAN 1.0 · Enable BET labels `Y` · season 2026 / week 1 / as-of 2026-09-01 · all QB values · all market lines · all adjustments · all team overrides (none) · SrcA raw and regressed · the PRESEASON MONITOR tab · every other formula in the workbook (57,399 total, coordinates identical).

## 4. Verification backing this manifest

| Check | Result |
|---|---|
| `scripts/verify_srcb_blendfix_candidate.py` | **41 checks, 0 failed** |
| Parts changed in the file | exactly 4: PRESEASON, TEAM RATINGS, CHANGELOG, sharedStrings |
| sharedStrings diff | banner only — no other string altered |
| CHANGELOG rows 1–6 | byte-preserved; row 8 still empty (exactly one new entry) |
| Formula count / coordinates | 57,399, identical; only `D5:D36` text changed |
| Deterministic rebuild | byte-identical from the committed base |
| Gates / monitor validator / linkcheck | PASS / PASS / PASS |
| `tests/run_tests.py` | **48/48** |
| `git diff --check` | clean |

### The five pins — reconfirmed in the finalized candidate

| Pin | Required | Result |
|---|---|---|
| DAL prior / rank | −1.07 / 22 | **−1.07 / 22** ✓ |
| NYG prior / rank | −1.90 / 24 | **−1.90 / 24** ✓ |
| DAL@NYG FinalMargin | +0.77 | **+0.77** ✓ |
| Fair line | NYG −0.8 | **NYG −0.8** ✓ |
| Edge | +3.27 on NYG +2.5 | **+3.27, NYG +2.5** ✓ |

These also match the values Google Sheets itself computed in the Phase 4 probe.

---

## 5. Rollback

**Before promotion:** nothing to undo.

**After promotion — preferred route.** Google Sheets **File → Version history → Name current version** *before* making any edit (suggested name `pre-v1.4 promotion 2026-09-01`). To roll back, restore that named version. This reverts all six change sets at once and is the only route that also restores the recalculated cells exactly.

**If version history is unavailable.** The pre-promotion state is fully reproducible from `TTW_NFL_2026_LIVE_EXPORT_20260901_BASE.xlsx` (SHA `39c7c567…`), committed in this repo — re-import it as a new Sheet and copy back, or replace the Sheet from it.

**Partial rollback.** The change sets are independent:

| To undo | Do this | Result |
|---|---|---|
| Source B only | Clear `PRESEASON I5:I36`, `K5:K36`, `L5:L36` | Priors revert to Source-A-only; J/S/T recalculate to blank/SrcA/1 |
| The blend fix only | Restore `TEAM RATINGS D5:D36` to `=IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),"")` | Week-1 returns to 0.8 × prior |
| Version label only | Set `START HERE A1` back to `(v1.1)` and clear `CHANGELOG A7:D7` | Cosmetic/documentation only |

**Do not** roll back by editing individual recalculated cells — they are formula outputs and typing over them destroys the formula.

**Repo-side.** The authoritative workbook is SHA-pinned in `tests/run_tests.py`; any accidental modification fails the suite. The candidate is SHA-pinned and rebuild-verified.

---

## 6. Manual upload for a disposable duplicate

The finalized candidate has been sent to the owner as a file attachment and is committed at the repo root. To create a **disposable** native duplicate — never the authoritative Sheet:

1. Drive → **New → File upload** → select `TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx`.
2. Right-click the uploaded file → **Open with → Google Sheets** (this creates a separate native Sheet; the .xlsx stays as-is).
3. Rename it with a `DISPOSABLE` marker so it cannot be confused with production.
4. Let it finish recalculating, then run the §7 checklist from `TTW_NFL_2026_Sheets_Execution_Report_20260901.md`.

Verify the download first: `shasum -a 256` must return `a71e8ba3356fe456d678eb2db75ec67ddfdbe287e743cc9901600cf57c97e22e`.

## 7. Open owner decisions

1. Approve promotion, or promote only one of the two change sets (§5 shows they separate cleanly).
2. Confirm the VSiN half of the composite may be used this way under the guide's subscriber terms — only the numeric page-29 table is used and the PDF is not committed.
3. Source C stays VALIDATE-ONLY pending the 2.1 pts/win calibration test recommended in the audit report §8.
4. Decide whether PR #1 is merged to establish `main` as trunk (`TTW_NFL_2026_Candidate_Verification_20260901.md` §6).
