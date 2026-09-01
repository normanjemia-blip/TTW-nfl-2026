# Version-Evidence Report — Canonical Version Determination

**Workbook audited:** `TTW_NFL_v1_1_1 Version 2.xlsx`
**Date:** 2026-07-23
**Question:** What is the workbook's *canonical intended* version — and is the `START HERE` banner (`v1.0`) correct?

## Canonical version: **v1.1**

Determined from internal evidence, in priority order. The filename token `v1_1_1` was treated as **secondary** and was **not** used to conclude "v1.1.1"; no internal reference to `v1.1.1` exists anywhere in the workbook.

| Priority | Source | Evidence | Points to |
|---|---|---|---|
| 1 | **Latest CHANGELOG entry** | Row 3 (last populated): Version `1.1`, Date `2026-07-13`, "External-audit safety pass." No `1.1.1` row exists. | **v1.1** |
| 2 | **SETTINGS freeze note** | `SETTINGS!A70`: "PARAMETER FREEZE: … frozen as of **v1.1 (2026-07-13)**." `SETTINGS!A66`: "**V1.1** SAFETY CONTROLS". | **v1.1** |
| 3 | **DICTIONARY version refs** | `A18` "**v1.1** Operational states", `A19` "**v1.1** Label policy", `A20` "**v1.1** Totals confidence", `A21` "**v1.1** Non-offensive TDs". | **v1.1** |
| 4 | **Internal documentation (AUDIT / BACKTEST / QB / HISTORY)** | `AUDIT!A44` "**V1.1** SAFETY-PASS TEST REPORT"; `BACKTEST!A78` "PARAMETER FREEZE (**v1.1**)", `A81` "**v1.1** totals correction"; `QB VALUES!A2` "**v1.1**: every row also needs…"; `HISTORY 2025!A2` "**v1.1**: totals columns regenerated…". | **v1.1** |
| 5 | Filename (secondary only) | `TTW_NFL_v1_1_1 Version 2.xlsx` — ambiguous token `v1_1_1`. **Not** used as proof. | (inconclusive) |

**Token tally across all non-formula text:** `v1.1` × 11 (all describing the current build) vs `v1.0` × 6 (all historical/archival — see below). No `v1.1.1` token anywhere.

## Every `v1.0` occurrence — proven classification

Each `v1.0` reference was read in full to decide whether it *incorrectly identifies the current workbook* (a mislabel to correct) or is a *legitimate historical reference* (must be left untouched).

| Cell | Full text (excerpt) | Verdict |
|---|---|---|
| **`START HERE!A1`** | "TO THE WINDOW — NFL POWER RATINGS 2026 **(v1.0)**" | **MISLABEL** — identifies the current workbook as v1.0. **Corrected → (v1.1).** |
| `HISTORY 2025!A2` | "**v1.1**: totals columns regenerated … Spread columns are the **v1.0** run (pipeline unchanged)." | Legitimate provenance (spread columns date from the v1.0 run). Cell already self-identifies as v1.1. **Untouched.** |
| `BACKTEST!A82` | "Corrected walk-forward totals MAE: 10.787 … (**v1.0**: 10.795 / 4.06)." | Legitimate historical comparison value. **Untouched.** |
| `BACKTEST!A83` | "Historical edge buckets above are **v1.0** archive values and are intentionally left untouched." | Legitimate archive, explicitly preserved by design. **Untouched.** |
| `AUDIT!A27` | "TEST REPORT — **v1.0** (all executed on recalculated copies of this exact file)" | Legitimate historical test-report section header. **Untouched.** |
| `AUDIT!A45` | "Regression: governed ratings bit-identical to **v1.0**; wk-18 spreads identical …" | Legitimate v1.1-vs-v1.0 regression statement. **Untouched.** |

**Conclusion:** exactly **one** cell (`START HERE!A1`) mislabels the workbook. Changing any of the other five `v1.0` references would make a factually correct historical statement wrong.

## Candidate produced

Because the internal evidence consistently identifies **v1.1** (not v1.1.1), the candidate is named:

```
TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx
```

Raw data: `audit/version_evidence.json`.
