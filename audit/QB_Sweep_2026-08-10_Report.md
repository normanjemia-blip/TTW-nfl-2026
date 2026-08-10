# NFL QB Preseason Sweep — August 10, 2026

**Checkpoint used:** `TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx` (QB lineage; the v1.3 market candidate was **not** used)
**Candidate produced:** `TTW_NFL_Power_Ratings_2026_v1.2.2_QB_SWEEP_CANDIDATE.xlsx`
**Branch:** `claude/nfl-preseason-readiness-audit-unvx7i`

## Scope limitation — read this

Web search hit the account's monthly spend limit partway through the sweep. Coverage actually achieved:

- **Deep, fresh per-team review (Aug 9–10 sources): ATL, CLE, MIN, LV** — the four flagged situations.
- **League-wide scans:** camp-injury tracker sweep, suspension sweep, and an all-32 camp-news sweep. These surfaced **no new starting-QB injury, suspension, demotion or availability change** among the other 28 teams.
- **Not achieved:** individual per-team re-verification of each of the 28 previously-settled teams.

Accordingly, **the 28 settled rows were left untouched**, retaining their 2026-08-05 verification date. They should be re-swept when search budget allows. No row was modified without fresh evidence.

One source artifact was **rejected, not acted on**: an aggregator line reading "Miami Dolphins: Tua Tagovailoa wins the Week 1 job." Tua signed with Atlanta in March 2026 and MIA's baseline is Malik Willis; this is a cross-season artifact.

## 1. Results by flagged team

### ATL — RESOLVED to baseline (Tua Tagovailoa) · Medium · delta 0
Ian Rapoport / NFL Network (2026-08-09): Tua is the projected Week 1 starter. Michael Penix Jr. is **not medically cleared** following his **third ACL surgery** and is not fully practicing — *"This is not a competition until he is fully practicing."* Tua is healthy and taking first-team reps (his early-camp issue resolved; Cooper Rush was signed as veteran depth). **Caveat:** no official announcement, and Rapoport notes job security is conditional ("he'll be the guy until he's not"), with in-season rotation possible. Hence **Medium**, not High. Active == Baseline → initialized **0 / 0**, delta 0.

### CLE — REMAINS UNCERTAIN · Low · values blank
Todd Monken has **not** named a starter. Watson and Sanders alternate first-team days and each starts one of the first two preseason games. Reporting is explicit that the decision is **not expected until after the 2026-08-22 game vs Buffalo**. Evidence does **not** support resolution; values left blank at Low, note and date refreshed only.

### MIN — RESOLVED to baseline (Kyler Murray) · Medium · delta 0
Murray has out-snapped McCarthy **63–33 with the first-team offense over the last four practices**, with the gap "growing daily"; he takes roughly two-thirds of first-team 11-on-11 snaps and is described as "pulling away" / "taking full control." **Source conflict resolved:** an initial reading that McCarthy had overtaken Murray (32–26) traced to **2026-08-01 total team snaps including scout-team work** — a single-day reversal, not the trend. No official announcement yet, hence **Medium**. Active == Baseline → initialized **0 / 0**, delta 0.

### LV — +0.50 RE-VERIFIED, unchanged
Starter status not reopened; re-verified only. HC Klint Kubiak named Cousins QB1 to open camp (Raiders.com official, NFL.com, ESPN). Cousins enters 2026 **healthy**; Mendoza is being developed gradually as QB2 ("competing with, not against"). A practice scuffle with Maxx Crosby involved no injury. **No credible contradicting evidence.** The approved **+0.50** deviation remains appropriate and is **unchanged**.

## 2. Changes since v1.2.1

| Team | Field | v1.2.1 | v1.2.2 |
|---|---|---|---|
| ATL | Baseline / Active value | blank / blank | **0 / 0** |
| ATL | Confidence | Low | **Medium** |
| MIN | Baseline / Active value | blank / blank | **0 / 0** |
| MIN | Confidence | Low | **Medium** |
| CLE | Source note / Last update | Aug-05 text / 2026-08-05 | refreshed / **2026-08-10** (values & Low unchanged) |
| LV | Source note / Last update | Aug-05 text / 2026-08-05 | re-verification text / **2026-08-10** (0 / 0.50 and High unchanged) |

All four are **zero-delta**. No new nonzero value was invented.

## 3. Injuries / suspensions / availability

- **No QB suspensions** league-wide. (The only August suspension found — Cowboys DE Charles Snowden, 3 games — is not a quarterback.)
- **Michael Penix Jr. (ATL)** — third ACL surgery, not medically cleared; the reason ATL is not a live competition.
- **Tua Tagovailoa (ATL)** — early-camp issue resolved; practicing, concussion history noted as ongoing risk.
- **Patrick Mahomes (KC)** — previously cleared for camp after Dec ACL/LCL surgery; no new setback surfaced.
- **Bo Nix (DEN), Daniel Jones (IND)** — no new setback surfaced since the Aug-5 sweep.
- Roster note (no starter impact): Baltimore released QB Diego Pavia.

## 4. Counts and deviations

- **QB OK: 31 · QB UNCERTAIN: 1** (was 29 / 3)
- **Remaining UNCERTAIN: CLE only**
- **Every nonzero deviation present: exactly one — LV, Kirk Cousins vs baseline Fernando Mendoza, +0.50** (approved 2026-08-05, re-verified 2026-08-10)
- **New deviation recommendations awaiting approval: none.** No newly discovered baseline-vs-active mismatch was found, so no valuation was required and none was invented.

## 5. Verification — all pass

| Check | Expected | Result | ✔ |
|---|---|---|---|
| Sheets | 21 | 21 | ✔ |
| Formulas | exactly 57,399 | **57,399** | ✔ |
| Formula coordinates & text | identical | identical, **0** diffs | ✔ |
| MARKET LINES changes | none | **none** | ✔ |
| ADJUSTMENTS changes | none | **none** | ✔ |
| TEAM RATINGS changes | none | **none** | ✔ |
| SETTINGS / schedule / HISTORY 2025 / BACKTEST / PRESEASON | none | **none** | ✔ |
| QB edits confined to authorized rows (6, 12, 23, 25) | yes | **0** outside | ✔ |
| Sheets changed | QB VALUES, START HERE, CHANGELOG only | those three only | ✔ |
| Drawings + persons | byte-identical | byte-identical | ✔ |
| Nonzero deltas | exactly one, LV +0.50 | **exactly one, LV +0.50** | ✔ |
| Counts | 31 OK / 1 UNCERTAIN | **31 / 1** | ✔ |

**19 cell diffs total** = 14 QB manual inputs (rows 6, 12, 23, 25) + version banner + 4 CHANGELOG cells.

## 6. SHA-256

| File | SHA-256 |
|---|---|
| v1.2.1 base | `e6efbbb3a2b75c76f57bf13906de84f50aefd25ea05d59ef6ddba56aa2aee136` |
| **v1.2.2 sweep candidate** | `9271a30f2dbda88dc7128742bb8eee18dd892f69c3ac56e64c475263ae1f48db` |
| v1.1 authoritative (untouched) | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` |

Candidate only — **not promoted**. Authoritative v1.1 workbook and the native Google Sheet were not modified.
