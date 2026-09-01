# Phase 2 — Week 1 Market Line Population: Verification Report

**Built from:** `TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx`
**Candidate:** `TTW_NFL_Power_Ratings_2026_v1.3_MARKET_CANDIDATE.xlsx`
**Date:** 2026-08-06

## ⚠ Read this first — what was actually entered

**The lines populated are OPENING lines dated 2026-05-15, not current lines.**

No genuinely current (August 2026) Week 1 market lines were retrievable this session — every public source traces back to the May schedule-release opening numbers, and search results explicitly advised checking sportsbooks directly for current odds. Rather than present stale numbers as current, they are recorded with their **true source and true line date**, so the workbook's own staleness rule fires:

- `SETTINGS` As-of date = 2026-07-13, `StaleDays` = 3 → line date 2026-05-15 is **59 days old**
- Expected result on open/recalc: **all 16 Week 1 rows report `STALE`** in the `Stale?` column, and the operational state is `STALE LINE`.

**These must be refreshed with current Novig lines before any live use.** The workbook names Novig as the primary entry source; DraftKings/FanDuel were the only publicly verifiable sources available.

## Source and cross-source divergence

**Primary source used:** DraftKings **opening** lines (schedule release), as of **2026-05-15** — FOX Sports "2026 NFL Odds Week 1: Lines, Spreads For All 16 Games" (explicitly "as of May 15 … DraftKings"), corroborated by ESPN's schedule-release odds piece, DK Network (2026-05-14) and RotoWire.

A second, **undated** FanDuel lookahead set was also retrieved. It disagrees with DraftKings on **13 of 16 games**, including one **side flip**:

| Game | FanDuel (undated) | DraftKings 2026-05-15 (used) |
|---|---|---|
| **MIA @ LV** | **MIA -3.5** / 40.5 | **LV -3** / 41.5 — *favorite is a different team* |
| ARI @ LAC | LAC -10.5 / 46.5 | LAC -11.5 / 45.5 |
| WAS @ PHI | PHI -4.5 / 47.5 | PHI -5.5 / 46.5 |
| NO @ DET | DET -6.5 / 49.5 | DET -7 / 48.5 |
| SF @ LA | LA -3.5 | LA -2.5 |
| CLE @ JAX | JAX -7.5 | JAX -7 |
| ATL @ PIT | PIT -2.5 / 41.5 | PIT -3 / 42.5 |
| NYJ @ TEN | TEN -2.5 / 38.5 | TEN -3 / 39.5 |
| BAL@IND, BUF@HOU, CHI@CAR, TB@CIN, DEN@KC | total differs by 1.0 | — |

Only **NE@SEA, GB@MIN, DAL@NYG** agree exactly across both books. DraftKings was chosen because it is the only set with a verifiable, explicit date. The MIA @ LV side flip is material — LV is also the team carrying the approved QB deviation — and should be re-checked first when current lines are entered.

## Verification results — all pass

| Check | Expected | Result | ✔ |
|---|---|---|---|
| Sheets | 21 | 21 | ✔ |
| Sheet order & visibility | unchanged | unchanged | ✔ |
| Formula count | 57,399 | **57,399** | ✔ |
| Formula coordinates | unchanged | identical | ✔ |
| Formula text | unchanged | **0** diffs | ✔ |
| **QB VALUES changes** | none | **none** | ✔ |
| **ADJUSTMENTS changes** | none | **none** | ✔ |
| **TEAM RATINGS changes** | none | **none** | ✔ |
| SETTINGS / schedule / HISTORY 2025 / BACKTEST changes | none | **none** | ✔ |
| Sheets changed | MARKET LINES, START HERE, CHANGELOG only | those three only | ✔ |
| Market edits confined to Week 1 inputs | rows 5–20, cols G,H,I,N,O,P | **0** outside that range | ✔ |
| Week-18 sample rows (261–276) | untouched | untouched | ✔ |
| Input check (favorite in game, spread positive) | 16/16 OK | **16/16 OK** | ✔ |
| Drawings + persons | byte-identical | byte-identical | ✔ |
| Zip parts changed | market sheet, changelog sheet, sharedStrings | those three only | ✔ |

**Total cell diffs: 101** = 96 market inputs (16 games × G,H,I,N,O,P) + 1 version banner + 4 CHANGELOG cells.

## Week 1 lines entered (sign convention: Favorite + positive spread)

| Row | Game | Favorite | Spread | Total | → Market home spread |
|---|---|---|---|---|---|
| 5 | NE @ SEA | SEA | 3.5 | 44.5 | −3.5 |
| 6 | SF @ LA | LA | 2.5 | 48.5 | −2.5 |
| 7 | CHI @ CAR | CHI | 2.5 | 44.5 | +2.5 |
| 8 | TB @ CIN | CIN | 3.5 | 50.5 | −3.5 |
| 9 | NO @ DET | DET | 7.0 | 48.5 | −7.0 |
| 10 | BUF @ HOU | BUF | 1.5 | 45.5 | +1.5 |
| 11 | BAL @ IND | BAL | 3.5 | 49.5 | +3.5 |
| 12 | CLE @ JAX | JAX | 7.0 | 40.5 | −7.0 |
| 13 | ATL @ PIT | PIT | 3.0 | 42.5 | −3.0 |
| 14 | NYJ @ TEN | TEN | 3.0 | 39.5 | −3.0 |
| 15 | ARI @ LAC | LAC | 11.5 | 45.5 | −11.5 |
| 16 | MIA @ LV | LV | 3.0 | 41.5 | −3.0 |
| 17 | GB @ MIN | GB | 1.5 | 44.5 | +1.5 |
| 18 | WAS @ PHI | PHI | 5.5 | 46.5 | −5.5 |
| 19 | DAL @ NYG | DAL | 2.5 | 48.5 | +2.5 |
| 20 | DEN @ KC | KC | 2.5 | 42.5 | −2.5 |

Each row also carries Source and Line date (`2026-05-15`) plus a Notes flag: *"OPENING line, NOT current — refresh with Novig before any live use."*

Usable market spreads move from **0 → 16**. Because every row is `STALE`, edges computed against them are reference-only until refreshed. (`EnableBetLabels` remains `N`, so 3.0+ edges display as `STRONG INVESTIGATE`, not `BET`.)

## Deliberate omissions
- **Open spread (J) / Open total (K) left blank.** No formula consumes them and the column carries no documented sign convention; since the entered numbers *are* the opening lines, duplicating them under an ambiguous convention would add risk without value.
- **Week-18 sample rows untouched** — out of scope for this phase.

## SHA-256
| File | SHA-256 |
|---|---|
| v1.2.1 base | `e6efbbb3a2b75c76f57bf13906de84f50aefd25ea05d59ef6ddba56aa2aee136` |
| **v1.3 candidate** | `1e9cb2c564bbe26c5da810b6cefcfba2ce163ee62271c40c49fc4a4dfa50bf9d` |
| v1.1 authoritative (untouched) | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` |

## Status
Candidate only — **not promoted**. Authoritative workbook and native Google Sheet untouched. QB values, adjustments and team ratings unchanged, as required.
