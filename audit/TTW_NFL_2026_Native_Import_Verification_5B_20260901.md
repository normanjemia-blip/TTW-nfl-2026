# TTW NFL 2026 — Phase 5B Native Import Verification (2026-09-01)

# RESULT: **PASS** — 36 checks, 0 failed

**Read-only. Nothing was modified.** Production (`1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`) was not read, opened, or written. PR #1 remains a draft. Nothing was promoted. Only the test copy named below was used.

| | |
|---|---|
| **Test copy** | `1_LSTx-khcqPNo5b3K65ruv9d4s9dJy3U6L7OYFpAwNk` — "TTW NFL v1.4 FULL IMPORT TEST — DO NOT USE" |
| Created / last modified | 2026-09-01T14:17:34Z / 14:17:56Z · owner normanjemia@gmail.com |
| Verified at | 2026-09-01T14:23Z |
| Source candidate | `TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx`, SHA-256 `a71e8ba3356fe456d678eb2db75ec67ddfdbe287e743cc9901600cf57c97e22e` |
| **Drive calls used** | **2** — one xlsx export, one metadata read. Production was not called at all. |

Evidence: `scripts/verify_native_import_5b.py` (re-runnable) and `audit/TTW_NFL_2026_Native_Import_Reconciliation_20260901.csv`.

> The export's own SHA (`59d2971f…`) necessarily differs from the candidate's — Google repackages the archive on import/export. That is the same accepted round-trip difference documented in `promotion/nfl_v11_roundtrip_verification.md`. Verification is therefore semantic (formulas, values, structure), not byte-level.

---

## 1. Structure and survival of the change sets — PASS

| Check | Result |
|---|---|
| 22 tabs preserved, correct names and order | **PASS** |
| Formula count | **57,399** — unchanged |
| `PRESEASON I5:I36` Source B values | **32/32 intact** |
| `PRESEASON K5:K36` source citations | **32/32 intact** |
| `PRESEASON L5:L36` as-of `2026-09-01` | **32/32 intact** |
| `TEAM RATINGS D5:D36` ISNUMBER formula survived the round trip | **32/32 present, text-exact** |
| `START HERE A1` banner | **v1.4** |
| `CHANGELOG` row 7 v1.4 entry | **intact** |

## 2. The behaviour the whole candidate exists for — PASS

This is the decisive result: Google Sheets recalculated the entire workbook natively, and

| Check | Result |
|---|---|
| **`D5:D36` genuinely blank, not numeric 0** | **32/32 blank** — the fix holds in the real product |
| GP = 0 for all 32 | **PASS** |
| **F = H = J for all 32** | **32/32** |
| Effective rating equals the candidate's preseason prior | **32/32** |
| Ranks match the candidate | **32/32** |
| SrcB centered / effective prior match the candidate | **32/32 each** |
| Sources Used = 2 | **32/32** |

Had the fix failed, `D` would read `0` and every effective rating would sit at 80% of its prior. It reads blank, and the ratings are the full priors.

## 3. Guardrails — PASS

Source C blank in all 32 rows · weights **0.40 / 0.35 / 0.25** in all 32 rows · `WinTotalsMode` **VALIDATE-ONLY** · Enable BET labels **Y** · ATS BET **1.5**, INVESTIGATE **1.5**, LEAN **1.0** · season 2026 · week 1 · as-of 2026-09-01 · HFA 1.6 · prior regression 0.33 · Week-1 blend weight 0.80.

**MARKET LINES, QB VALUES, ADJUSTMENTS and PRESEASON MONITOR are cell-for-cell identical to the pre-change base export** — the candidate changed nothing there, and the native round trip changed nothing either.

## 4. Formula / conversion errors — PASS

Every cell on all 22 tabs was scanned for `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#ERROR!`.

- **Zero new errors.** No conversion damage from the native import.
- The only errors present are the **6 pre-existing `#DIV/0!` cells** — `CALC!B39:B43` and `DATA QUALITY!B8` — from an empty-range `AVERAGE` at zero games played. These exist in production today, are documented in `audit/DQ_DIV0_Diagnosis.md`, and are **not** caused by v1.4. Count is unchanged at 6/6.
- No circular-reference markers appeared.

## 5. Sixteen-game reconciliation — PASS

All 16 Week-1 ENGINE rows match `audit/TTW_NFL_2026_Candidate_Week1_Slate_20260901.csv` on **FinalMargin, fair line, spread edge and supported side** — 16/16. The DASHBOARD renders 16 games and its model spreads agree with ENGINE on all 16. Full row-by-row output: `audit/TTW_NFL_2026_Native_Import_Reconciliation_20260901.csv`.

This closes the item Phase 4 had to leave open: the other 15 games (beyond DAL@NYG) are now confirmed by Google itself, not by an independent reimplementation.

### The five pins, in the native Sheet

| Pin | Required | Native result |
|---|---|---|
| DAL | −1.07, rank 22 | **−1.07, rank 22** ✓ |
| NYG | −1.90, rank 24 | **−1.90, rank 24** ✓ |
| DAL@NYG FinalMargin | +0.77 | **+0.77** ✓ |
| Fair line | NYG −0.8 | **NYG −0.8** ✓ |
| Edge | +3.27 on NYG +2.5 | **+3.27, NYG +2.5** ✓ |

## 6. Time zone — comparison NOT possible with these tools; impact proven nil

**I could not read either Sheet's time zone, and I am not claiming they match.** The spreadsheet time zone lives in the Sheets API (`spreadsheetProperties.timeZone`); the Drive tools available here expose only file metadata, which carries no such field — the metadata read on the test copy returned `createdTime`, `modifiedTime`, `owner`, `title`, `mimeType`, `fileSize`, `parentId`, `viewUrl`, `viewedByMeTime` and nothing more. The xlsx export does not carry it either (scanned every XML part: zero occurrences of `timeZone`, `America/`, or a `date1904` flag). Reading production's time zone would have required a production call, which was out of scope and would have been equally fruitless.

What I *can* establish, and did:

1. **No clock-dependent function exists anywhere in the workbook** — all 57,399 formulas were scanned for `NOW(`, `TODAY(`, `RAND(`, `RANDBETWEEN(`: **zero hits**. Every date in the model is a static value the user typed (SETTINGS as-of date, MARKET LINES line dates, QB last-update dates), so no computed output can vary with the time zone.
2. **No date drifted in the round trip.** All **353** date-bearing cells in the test copy are identical to the pre-change base export — zero shifts — and **none carries a time-of-day component**, which is the only way a time-zone difference could move a serial. MARKET LINES line dates still read serial 46266; SETTINGS as-of still reads 2026-09-01.
3. The staleness logic compares two static dates (line date vs as-of date), never a clock read.

**Conclusion:** a time-zone difference between the test copy and production, if one exists, cannot change any rating, spread, edge, rank or staleness flag in this workbook. If you want the literal setting confirmed, it is a five-second check in each Sheet: **File → Settings → Time zone** — expected `(GMT-07:00) America/Los_Angeles` in both. That check is the one item in this phase I could not perform for you.

---

## 7. Verdict

**PASS.** The native Google Sheets import of the v1.4 candidate is faithful: structure intact, both change sets survived, the blank-preservation fix works in the real product, every guardrail holds, no conversion errors were introduced, all 16 games reconcile, and all five pins land. The single unverified item is the literal time-zone string, which is unreadable through the available tooling and provably cannot affect any output.

**Stopped for owner review.** No production artifact was touched, PR #1 is still a draft, and nothing has been promoted.
