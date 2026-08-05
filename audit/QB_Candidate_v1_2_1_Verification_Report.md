# QB Candidate v1.2.1 — Verification Report

**Built from:** `TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx`
**Candidate:** `TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx`
**Date:** 2026-08-05 · **Approved deviation:** LV Kirk Cousins **+0.50**

## SHA-256
| File | SHA-256 |
|---|---|
| v1.2 working (base) | `2d9d36d0b17b4acb7fa7ae1122d94d5adab57413336b029112ad430415ad4c7d` |
| **v1.2.1 candidate** | `e6efbbb3a2b75c76f57bf13906de84f50aefd25ea05d59ef6ddba56aa2aee136` |
| v1.1 authoritative (untouched) | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` |

## Verification results
| Check | Expected | Result | ✔ |
|---|---|---|---|
| Sheets | 21 | 21 | ✔ |
| Sheet order & visibility | unchanged | unchanged | ✔ |
| Formula count | exactly 57,399 | **57,399** | ✔ |
| Formula coordinates | unchanged | identical | ✔ |
| Formula text | unchanged | **0** diffs | ✔ |
| Non-zero QB deltas | exactly one: LV +0.50 | exactly one: **LV +0.50** | ✔ |
| QB statuses | 29 OK / 3 UNCERTAIN | **29 OK / 3 UNCERTAIN** | ✔ |
| UNCERTAIN teams | ATL, CLE, MIN | ATL, CLE, MIN | ✔ |
| Schedule / market-line / adjustment / rating / settings / historical / backtest changes | none | **none** (0 diffs in any prohibited sheet) | ✔ |
| Sheets changed | QB VALUES, START HERE, CHANGELOG only | those three only | ✔ |
| Drawings + persons | byte-identical | byte-identical | ✔ |
| Zip parts changed | QB sheet, CHANGELOG sheet, sharedStrings | those three only | ✔ |

## Changed cells (9 total)
| Sheet!Cell | Old | New |
|---|---|---|
| `QB VALUES!C23` | *(blank)* | `0` — LV Baseline value (Fernando Mendoza) |
| `QB VALUES!E23` | *(blank)* | `0.5` — LV Active value (Kirk Cousins) |
| `QB VALUES!I23` | `Low` | `High` |
| `QB VALUES!J23` | deviation-pending note | current source + approved-rationale note |
| `START HERE!A1` | `… (v1.1)` | `… (v1.2.1)` |
| `CHANGELOG!A5` | *(blank)* | `1.2.1` |
| `CHANGELOG!B5` | *(blank)* | `2026-08-05` |
| `CHANGELOG!C5` | *(blank)* | QB activation entry |
| `CHANGELOG!D5` | *(blank)* | model-impact note |

`QB VALUES!D23` (Kirk Cousins), `K23` (2026-08-05) and `M23` (2026) were already correct in v1.2 and are unchanged. Full list: `audit/qb_candidate_changed_cells.csv` / `.json`.

## Defect found and fixed during this build
The first build attempt was **rejected by verification** and rebuilt. The cell-replacement regex tried the paired-tag pattern before the self-closing pattern; for a blank cell such as `<c r="C23" s="14"/>`, `[^>]*` consumed the `/`, so `.*?</c>` ran on to the following cell's closing tag. This silently deleted `D23` (Kirk Cousins) and `F23` (a delta formula), producing 57,398 formulas and 28 OK / 4 UNCERTAIN. The matcher now tries the self-closing form first (`scripts/build_qb_candidate.py`), and the rebuilt candidate passes every check.

The v1.2 working copy was **not** affected — its source cells were all value-bearing (non-self-closing), and it verified clean at 57,399 formulas with 0 formula diffs.

## QB status summary (computed from the workbook's own `QBFlag` logic)
Cached formula results in the file remain as last calculated; Excel/Sheets will recalculate on open. Statuses below are computed directly from the `QBFlag` definition (`D` blank, `Confidence="Low"`, `Reviewed<>CurrentSeason`, or stale `Last update`).

- **29 OK** — 28 teams initialized at zero (Active QB == Baseline QB) **plus LV** (Cousins, High, +0.50 delta).
- **3 UNCERTAIN** — ATL, CLE, MIN: Baseline/Active values blank, Confidence **Low**, delta 0. Left deliberately unresolved; not researched again during this task.

## Status
Candidate only — **not promoted**. The v1.1 authoritative workbook and the native Google Sheet were not modified.
