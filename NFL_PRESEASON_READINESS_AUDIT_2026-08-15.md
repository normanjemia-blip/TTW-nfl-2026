# NFL Preseason Readiness Audit — Checkpoint 2026-08-15

**Repository:** `normanjemia-blip/ttw-nfl-2026`
**Branch:** `claude/nfl-preseason-readiness-audit-unvx7i`
**Starting commit:** `ea3572b` · **Final commit:** `dc660252eecd9d61fb10ea2f05e2ee7b7d4a2353` (local, unpushed)
**Authoritative workbook:** `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE` — [Google Sheet](https://docs.google.com/spreadsheets/d/1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew/edit)
**Scope:** repo-local monitoring, validation and reporting only. No workbook, model input, or Google Sheet was modified.

---

## 1. Branch and commit verification

| Item | Stated | Verified | Result |
|---|---|---|---|
| Branch `claude/nfl-preseason-readiness-audit-unvx7i` | correct start point | exists, checked out, clean tree | ✅ **confirmed** |
| Commit `fc0b247` | correct start point | `git cat-file -t fc0b247` → *"Not a valid object name"* | ❌ **does not exist in this repository** |

`fc0b247` is not on `main`, not on the remote, and not an ancestor of HEAD. Actual HEAD at start was `ea3572b` ("QB preseason sweep 2026-08-10"). I did **not** reset or rebase to chase the missing commit; work continued from the verified HEAD. If `fc0b247` exists, it belongs to a different repository or an unpushed clone.

---

## 2. Verified current status

### Checkpoint claims confirmed

| Claim | Verified state | Status |
|---|---|---|
| All 272 regular-season games loaded | 272 × 2026 REG rows in `IMPORT SCHEDULE` | ✅ match |
| As-of date may still show July 13 | `SETTINGS!B7 = 2026-07-13` | ✅ match — **33 days stale** |
| Week 1: 16 missing spreads, 16 missing totals | 16 / 16 missing in AUTHORITATIVE; usable market spreads = 0 | ✅ match |
| BET must remain OFF | `SETTINGS!B67 = "N"` | ✅ match |
| Thresholds preserved | ATS 3.0 / 1.5 / 1.0 · Totals 3.0 / 1.5 / 1.0 | ✅ match |
| PRESEASON: regressed 2025 TTW only, public blank, win totals validate-only | SrcA 32/32 · SrcB 0/32 · mode `VALIDATE-ONLY` | ✅ match |

### Discrepancies found

1. **QB VALUES lineage (material).** The claim "QB VALUES are populated" is only partly true. AUTHORITATIVE holds all 32 baseline values dated `2026-07-13` — the original absolute values. The *researched* QB state (zero-initialised rows, LV +0.50, ATL/MIN resolved) exists **only in candidates** `v1.2`, `v1.2.1`, `v1.2.2`. It is **not** in AUTHORITATIVE and **not** in the Google Sheet. Graduating any QB finding therefore means promoting a candidate, not editing AUTHORITATIVE in place.
2. **PRESEASON MONITOR did not exist** as a repository artifact before this session. Created now.
3. **No AFC North draft exists in this repository.** Its HOLD is honoured vacuously. Volatile sections that will need refresh after roster cuts and the final market audit are recorded so the requirement is not lost: QB depth/starter lines, offensive-line combinations, injury availability, market-derived win-total commentary, and any conclusion resting on preseason participation.
4. **No pre-existing validator, link-check or gate suite** — and no `AGENTS.md`, `CLAUDE.md`, `tests/`, `Makefile`, or CI. The honest Step 1 baseline is *absence of infrastructure*, not a green build. The suites below are the first meaningful run.

### Preseason Week 1 coverage

Execution time **2026-08-15 ~06:00 ET**.

| Date | Games | Status |
|---|---|---|
| Aug 13 | 6 | COMPLETE (12 team-games) |
| Aug 14 | 3 | COMPLETE (6 team-games) |
| Aug 15 | 7 | **NOT PLAYED** at checkpoint (14 team-games) |

18 of 32 team-game rows are post-game; 14 remain pre-kickoff and are gate-locked to `Starter Use = TBD`.

---

## 3. Files changed

**15 added, 1 modified. All six workbook SHA-256 values unchanged.**

| Path | Role |
|---|---|
| `preseason/PRESEASON_MONITOR.csv` | 32 team-game intake rows (Aug 13–15) |
| `preseason/intake_template.csv` | Header-only template for later preseason weeks |
| `preseason/SCHEMA.md` | Column definitions and allowed values |
| `scripts/gen_preseason_monitor.py` | Deterministic monitor generator (byte-stable) |
| `scripts/validate_preseason_monitor.py` | Schema + authorization gate validator |
| `scripts/linkcheck_preseason.py` | Source-URL format/host check + reachability probe |
| `scripts/run_gates.py` | Workbook invariant gates (read-only) |
| `scripts/reconcile_checkpoint.py` | Checkpoint-vs-workbook reconciliation |
| `scripts/dq_div0_diagnosis.py` | `#DIV/0!` root-cause and consumer trace |
| `tests/run_tests.py` | Regression suite, 13 tests, stdlib only |
| `docs/preseason_monitoring.md` | Workflow documentation |
| `audit/Status_Reconciliation_2026-08-15.md` | Full reconciliation record |
| `audit/graduation_candidates_2026-08-15.md` | Graduation proposals |
| `audit/DQ_DIV0_Diagnosis.md` | Diagnosis + exact proposed patch (not applied) |
| `README.md` | *(modified)* preseason-monitoring section |

### Workbook integrity (all unchanged)

| File | SHA-256 |
|---|---|
| `…v1.1_AUTHORITATIVE.xlsx` | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` |
| `TTW_NFL_v1_1_1 Version 2.xlsx` | `243ce78fd0305f0f67afa35bc88e1b29beae4d464fa747e48a8c30952d032998` |
| `…v1.2_QB_WORKING.xlsx` | `2d9d36d0b17b4acb7fa7ae1122d94d5adab57413336b029112ad430415ad4c7d` |
| `…v1.2.1_QB_CANDIDATE.xlsx` | `e6efbbb3a2b75c76f57bf13906de84f50aefd25ea05d59ef6ddba56aa2aee136` |
| `…v1.2.2_QB_SWEEP_CANDIDATE.xlsx` | `9271a30f2dbda88dc7128742bb8eee18dd892f69c3ac56e64c475263ae1f48db` |
| `…v1.3_MARKET_CANDIDATE.xlsx` | `1e9cb2c564bbe26c5da810b6cefcfba2ce163ee62271c40c49fc4a4dfa50bf9d` |

Google Sheet: **not read, not written.**

---

## 4. Tests and validators

| Suite | Result | Detail |
|---|---|---|
| `scripts/run_gates.py` | **PASS** | 21 sheets · 57,399 formulas · BET OFF · ATS+Totals 3.0/1.5/1.0 · VALIDATE-ONLY · 272 REG · PRESEASON SrcB blank |
| `scripts/validate_preseason_monitor.py` | **PASS** | 32 rows / 32 teams / 18 complete / 14 not played / 19 named blockers |
| `scripts/linkcheck_preseason.py` | **PASS** | Format + host allowlist clean; network probe 6/8 reachable, 2 WARN (non-blocking) |
| `tests/run_tests.py` | **PASS 13/13** | Gates, validator, linkcheck, workbook SHA pin, no-new-spreadsheet, monitor invariants, DQ guard semantics |
| Idempotence | **PASS** | Monitor CSV byte-identical on second generation |

### Gates enforced by the validator
- `Decision` must stay `PENDING`; `Workbook Updated?` must stay `N` (no live-workbook authorization).
- `Game Status = NOT PLAYED` ⇒ `Starter Use = TBD`.
- Every row requires a valid `Source URL` (https + host allowlist) and ISO `Source Date`.
- Any `UNVERIFIED` finding must carry a **named blocker** — never a silent gap.
- A non-`NONE` `Proposed Destination` must name a **field** and must not contain a point value.
- AUTHORITATIVE SHA-256 pinned; no new spreadsheet file may be added to the repository.

---

## 5. Preseason games and teams reviewed

9 of 16 games complete (18 team-games). Decision-relevant findings only — no scores, margins, box-score production or small-sample efficiency was used as evidence.

| Team | Starter Use | Finding |
|---|---|---|
| DET | RESTED | QB1 Goff rested; few starters used |
| CIN | LIMITED | Burrow + most offensive starters played limited reps |
| GB | LIMITED | Love expected to play; HC "anybody healthy ready" *(pre-game expectation only)* |
| PIT | RESTED | **Conflict:** HC wanted Rodgers snaps; reporting indicates he likely sat |
| LAC | RESTED | QB1 Herbert rested |
| LV | LIMITED | No.1 pick Mendoza played as QB2 — consistent with staged development behind Cousins |
| IND, NE, HOU, ARI, TEN, SF | TBD | No qualifying participation source — named blockers |
| DEN | MIXED | Starters got early snaps but **QB1 Bo Nix held out entirely** (no diagnosis reported) |
| ATL | STARTERS PLAYED | Tua started the opener with full complement; Penix Jr. sidelined (ACL) |
| TB | RESTED | Mayfield held back; QB2 Browning nursing a back injury |
| NYJ | STARTERS PLAYED | HC "everyone's playing"; Geno Smith with Hall and Wilson |
| MIA | STARTERS PLAYED | First look at QB1 Malik Willis (3yr/$67.5M) |
| WAS | RESTED | Daniels did not suit up; Mariota started. **LT Tunsil torn triceps** |
| 14 Aug-15 teams | TBD | Not yet kicked off at checkpoint |

---

## 6. Graduation candidates

**Nothing applied.** All rows remain `Decision = PENDING`, `Workbook Updated? = N`. Every item requires human approval.

| # | Team | Destination | Proposed change (field, not value) | Evidence | Confidence | Approval |
|---|---|---|---|---|---|---|
| 1 | MIN | QB VALUES | Confidence `Medium → High`; refresh Source/Last-update | HC officially named Kyler Murray regular-season Week 1 starter 2026-08-12; McCarthy backup. Active = Baseline, delta stays 0. [vikings.com](https://www.vikings.com/news/kyler-murray-quarterback-starting-2026-nfl-season) · OFFICIAL | HIGH | **YES** |
| 2 | — | SETTINGS *(outside allowed destination list)* | `As-of date` `2026-07-13 → 2026-08-15` | 33 days stale; drives QB-row staleness and MARKET LINES `Stale?`. Verified in-workbook. | HIGH | **YES** |
| 3 | WAS | ADJUSTMENTS | Create documented entry for starting-LT availability (**no point value**) | Tunsil torn triceps, expected to miss significant time; Coleman shifting to LT. [nfl.com](https://www.nfl.com/news/2026-nfl-preseason-week-1-10-things-to-watch) · OFFICIAL | HIGH | **YES** |
| 4 | CHI | ADJUSTMENTS | Create documented entries for secondary availability (**no point value**) | Gordon PUP (calf); Bryant 4–6 mo post knee surgery; Flowers out for season; Bishop suspended 3 games. [nfl.com](https://www.nfl.com/news/2026-nfl-preseason-week-1-10-things-to-watch) · OFFICIAL | HIGH | **YES** |
| 5 | CAR | ADJUSTMENTS | Create documented entry for EDGE availability (**no point value**) | Nic Scourton torn ACL, first practice. [si.com](https://www.si.com/nfl/four-key-injuries-overshadowed-first-day-nfl-training-camps) · MULTI-SOURCE | MEDIUM | **YES** |
| 6 | LV | QB VALUES | Refresh Source/Last-update only (**approved +0.50 stands**) | Cousins remains QB1; Mendoza played as QB2. BEAT REPORT | MEDIUM | **YES** |
| 7 | ATL | QB VALUES | Refresh Source/Notes/Last-update; **no** Confidence change | Preseason start only, **not** a regular-season declaration; Penix sidelined (ACL). BEAT REPORT | MEDIUM | **YES** |
| 8 | MIA | QB VALUES | Refresh Source/Last-update (confirms baseline QB role) | Willis worked as QB1 in the opener. BEAT REPORT | MEDIUM | **YES** |
| 9 | CLE | QB VALUES | Refresh Source/Last-update only; **remains UNCERTAIN** | Watson started opener, Sanders starts Wk2, HC "not shutting the door". OFFICIAL | HIGH | **YES** |

**Explicitly not proposed:** no power-rating points, no injury-point values, no weight retuning, no PRESEASON destination items (public ratings stay blank, win totals stay VALIDATE-ONLY), no market-line changes. DEN (Nix hold-out, no diagnosis) and TB (Browning back injury, no timeline) stay MONITOR with no destination.

---

## 7. DATA QUALITY `#DIV/0!` diagnosis

**Verdict: missing empty-range guard — harmless to output, but a real monitoring defect.**

Six cells affected: `CALC!B39:B43` (`=ROUND(AVERAGE(range),6)`) plus the `DATA QUALITY!B8` mirror (`=ABS(CALC!$B$42)`).

**Root cause (measured):** each source range — `CALC!F2:F33`, `I2:I33`, `L2:L33`, `O2:O33`, `AC2:AC33` — currently holds **0 numeric values**; every cell is a formula returning text-blank because no 2026 in-season stats are loaded. `AVERAGE()` over zero numerics is undefined.

**Consumer trace:** exactly one consumer workbook-wide — `DATA QUALITY!B8`, a display row. The readiness gate keys off per-game `DQStatus="BLOCKED"`, not these cells (`0 BLOCKED / 0 WARNING / 0 unmatched`). No ENGINE output, recommendation label, validator or gate reads it.

**Why it still matters:** the mean-check exists to detect a genuine defect (opponent adjustment failing to centre). A permanent error state hides that signal and habituates the operator to ignore it.

**Exact proposed patch — NOT applied:**
```
CALC!B39  =IF(COUNT($F$2:$F$33)=0,"",ROUND(AVERAGE($F$2:$F$33),6))
CALC!B40  =IF(COUNT($I$2:$I$33)=0,"",ROUND(AVERAGE($I$2:$I$33),6))
CALC!B41  =IF(COUNT($L$2:$L$33)=0,"",ROUND(AVERAGE($L$2:$L$33),6))
CALC!B42  =IF(COUNT($O$2:$O$33)=0,"",ROUND(AVERAGE($O$2:$O$33),6))
CALC!B43  =IF(COUNT($AC$2:$AC$33)=0,"",ROUND(AVERAGE($AC$2:$AC$33),6))
DATA QUALITY!B8  =IF(CALC!$B$42="","— (awaiting weekly stats)",ABS(CALC!$B$42))
```
`COUNT()` counts numerics only, so populated-data results are bit-identical to today's formulas. Guard semantics are unit-tested in `tests/run_tests.py :: DQGuardPatch` (empty → blank; populated → same mean; mixed → ignores blanks; genuine non-zero still surfaced). Applying it touches authoritative formulas and is outside current authorization.

---

## 8. Unresolved conflicts

1. **PIT — Aaron Rodgers snaps.** Head coach wanted Rodgers to play; reporting indicates he likely sat with Rudolph/Allar/Howard under center. Both claims preserved; not silently resolved.
2. **ATL — preseason start vs regular-season declaration.** Tua started the preseason opener, but no source states Atlanta has declared its regular-season Week 1 starter while Penix rehabs. Not treated as settling the competition.
3. **CLE — competition explicitly unsettled.** Watson started the opener, Sanders starts Week 2, HC "not shutting the door." Correctly remains UNCERTAIN.
4. **Cross-season source artifact rejected.** A headline pairing Joe Burrow's Bengals opener with Philadelphia contradicts the actual Aug-13 DET-at-CIN matchup; treated as a stale-season artifact and not used.

---

## 9. Blockers

1. **Source access — 2 URLs.** `covers.com` lineup pages return HTTP errors to direct fetch (bot protection). Content was obtained via search indexing; URLs recorded but not independently re-fetchable from this environment. Affects DET / LAC / DEN rows — capped at MEDIUM confidence, not HIGH.
2. **Post-game participation unconfirmed for six Aug-13 teams** — IND, NE, HOU, ARI, TEN, SF. No qualifying source located. Rows carry `Starter Use = TBD` with named blockers rather than an inferred value.
3. **Workbook write access.** No authorization for live-workbook or Google Sheet changes; all findings are proposals only.
4. **QB lineage gap.** Researched QB state is candidate-only; promoting it requires a separate authorized promotion, not an in-place edit.

---

## 10. Branch and commit status

- **Branch:** `claude/nfl-preseason-readiness-audit-unvx7i`
- **Commit:** `dc660252eecd9d61fb10ea2f05e2ee7b7d4a2353` — one scoped commit, created only after all tests passed
- **State:** 1 commit ahead of `origin`, **not pushed**, **no PR opened**, per instruction
- A repository stop-hook requests a push; that request conflicts with the explicit instruction and was **not** actioned. The commit is durable locally and pushes cleanly on request.

---

## 11. Exact next action after the remaining preseason games

1. After the Aug-15 slate concludes, collect post-game starter-participation sources for the 14 pending team-games plus the six Aug-13 blockers.
2. Re-run `python3 scripts/gen_preseason_monitor.py` to flip those rows off `TBD`.
3. Re-run the four suites: `run_gates.py` → `validate_preseason_monitor.py` → `linkcheck_preseason.py` → `tests/run_tests.py`.
4. Regenerate the graduation report and bring the combined list for approval.

**Priority order for approval:** the **SETTINGS as-of date** first (every staleness gate depends on it), then **MIN confidence Medium → High**. Both are low-risk and unblock accurate staleness reporting ahead of roster cuts, official depth charts and the major injury review.

Ratings, wagers and recording-copy conclusions remain locked. BET stays OFF.
