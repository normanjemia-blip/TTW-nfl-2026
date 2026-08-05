# QB Working Copy — Verification Report

**Source (read-only, authoritative):** `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx`
**Working copy:** `TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx`
**Date:** 2026-08-05 · **Build method:** surgical edit of `xl/worksheets/sheet6.xml` (QB VALUES) only; all other zip members copied verbatim.

## SHA-256
| File | SHA-256 |
|---|---|
| Source (unchanged) | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` |
| Working copy | `2d9d36d0b17b4acb7fa7ae1122d94d5adab57413336b029112ad430415ad4c7d` |

## Verification results
| Check | Expected | Result | ✔ |
|---|---|---|---|
| Sheet count | 21 | 21 | ✔ |
| Sheet order & visibility | unchanged | unchanged (11 visible / 10 hidden) | ✔ |
| Formula count | 57,399 | 57,399 | ✔ |
| Formula coordinates & text | identical | identical, **0** formula diffs | ✔ |
| Non-QB cell edits | none | **0** (all 132 diffs in QB VALUES) | ✔ |
| Schedule changes | none | none (no IMPORT SCHEDULE edits) | ✔ |
| Market-line edits | none | none (no MARKET LINES edits) | ✔ |
| Adjustments edits | none | none (no ADJUSTMENTS edits) | ✔ |
| Zip members changed | only QB sheet | only `xl/worksheets/sheet6.xml` | ✔ |
| Drawings + persons | byte-identical | byte-identical | ✔ |
| QB delta (model impact) | 0 for all 32 | **0** for all rows (no non-zero value entered) | ✔ |
| Google Sheet edits | none | none | ✔ |

## What changed (132 cells, all in QB VALUES)
| Column | Cells | Change |
|---|---|---|
| Baseline value (C) | 32 | 28 settled → `0`; 4 uncertain/deviation → blank |
| Active value (E) | 32 | 28 settled → `0`; 4 uncertain/deviation → blank |
| Active QB (D) | 1 | LV: Fernando Mendoza → Kirk Cousins (name only; value blank) |
| Confidence (I) | 3 | ARI Low→High, IND Medium→High, LV Medium→Low (26 already-High and the Low teams unchanged) |
| Source/Notes (J) | 32 | refreshed to Aug-2026 sources + status notes |
| Last update (K) | 32 | 2026-07-13 → 2026-08-05 |
| Reviewed season (M) | 0 | already 2026 (= CurrentSeason); unchanged |

Full list: `audit/qb_changed_cells.csv` / `.json`.

## Classification summary
- **Teams initialized at zero (settled, Active == Baseline → 0/0, High): 28** — ARI, BAL, BUF, CAR, CHI, CIN, DAL, DEN, DET, GB, HOU, IND, JAX, KC, LA, LAC, MIA, NE, NO, NYG, NYJ, PHI, PIT, SEA, SF, TB, TEN, WAS.
- **Teams left uncertain (blank, Low): 3** — ATL, CLE, MIN (see `qb_open_competitions.md`).
- **Proposed non-zero deviation cases (blank, Low, pending approval): 1** — LV (Cousins over priced-in Mendoza; see `qb_proposed_deviations.md`).

All deltas remain 0, so model outputs are unchanged; the working copy is not promoted and the authoritative workbook is untouched. Reproduce with `scripts/build_qb_working.py` then `scripts/verify_qb_working.py`.
