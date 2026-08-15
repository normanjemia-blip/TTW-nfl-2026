# Status Reconciliation — checkpoint 2026-08-15

**Branch:** `claude/nfl-preseason-readiness-audit-unvx7i` · **Starting commit:** `ea3572b` · tree clean at start.

## Commit / branch verification

| Item | Stated | Verified | Result |
|---|---|---|---|
| Branch `claude/nfl-preseason-readiness-audit-unvx7i` | correct start point | exists, checked out, clean | ✅ **confirmed** |
| Commit `fc0b247` | correct start point | `git cat-file -t fc0b247` → *"Not a valid object name"* | ❌ **does not exist in this repository** |

Actual HEAD is `ea3572b` ("QB preseason sweep 2026-08-10"). `fc0b247` is not an ancestor, not on `main`, and not on the remote. I did **not** reset or rebase to chase it; work continued from the verified HEAD. If `fc0b247` exists elsewhere, it belongs to a different repository or an unpushed clone.

## Checkpoint claims vs. repository reality

| # | Claim | Verified state | Status |
|---|---|---|---|
| 1 | All 272 regular-season games loaded | 272 × 2026 REG rows in `IMPORT SCHEDULE` | ✅ match |
| 2 | As-of date may still show July 13 | `SETTINGS!B7 = 2026-07-13` | ✅ match — **33 days stale** vs checkpoint |
| 3 | Week 1 has 16 missing spreads and 16 missing totals | 16 / 16 missing in AUTHORITATIVE; usable market spreads = 0 | ✅ match |
| 4 | BET must remain OFF | `SETTINGS!B67 = "N"` | ✅ match |
| 5 | Thresholds preserved | ATS 3.0/1.5/1.0, Totals 3.0/1.5/1.0 | ✅ match |
| 6 | PRESEASON uses regressed 2025 TTW only; public blank; win totals validate-only | SrcA populated 32/32; SrcB 0/32; mode `VALIDATE-ONLY` | ✅ match |
| 7 | QB VALUES are populated | **Partly.** AUTHORITATIVE has all 32 baseline values dated 2026-07-13 (original absolute values). The *researched* QB state (zero-initialised, LV +0.50, ATL/MIN resolved) lives only in candidates `v1.2`, `v1.2.1`, `v1.2.2` — **not** in AUTHORITATIVE and **not** in the Google Sheet | ⚠️ **discrepancy** |
| 8 | PRESEASON MONITOR contains 32 team-game rows | No such artifact existed in the repo before this session | ⚠️ **discrepancy — created now** |
| 9 | AFC North research draft on HOLD | No AFC North artifact exists in this repository | ⚠️ **discrepancy — nothing to hold** |
| 10 | Existing validator / link-check / gate suite | None existed: no `AGENTS.md`, `CLAUDE.md`, `tests/`, `Makefile`, CI, or validators | ⚠️ **discrepancy — baseline is "no infrastructure"; created now** |

### Discrepancy notes

**#7 — QB state lineage.** The authoritative workbook and the native Google Sheet still carry the pre-research QB values. Graduating any QB finding therefore means promoting a candidate, not editing AUTHORITATIVE in place. No promotion is authorized, so none was done.

**#9 — AFC North.** There is no draft to place on HOLD here. Its HOLD status is honoured vacuously. When the artifact appears, the volatile sections requiring refresh after roster cuts and the final market audit are: QB depth/starter lines, offensive-line combinations, injury availability, any market-derived win-total commentary, and any conclusion resting on preseason participation. Recorded here so the requirement is not lost.

**#10 — Baseline.** Step 1 asked for a baseline run of the existing suite. The honest baseline is that no suite existed; the first meaningful run is the one created in this session (results below), not a pre-existing green build.

## Preseason Week 1 coverage at checkpoint

Local time at execution: **2026-08-15 ~06:00 ET**.

| Date | Games | Status |
|---|---|---|
| Aug 13 | 6 | COMPLETE (12 team-games) |
| Aug 14 | 3 | COMPLETE (6 team-games) |
| Aug 15 | 7 | **NOT PLAYED** at checkpoint (14 team-games) |

18 of 32 team-game rows are post-game; 14 remain pre-kickoff and are locked to `Starter Use = TBD`.

## Suite results (this session)

| Suite | Result |
|---|---|
| `scripts/run_gates.py` | **PASS** — 21 sheets, 57,399 formulas, BET OFF, thresholds 3.0/1.5/1.0, VALIDATE-ONLY, 272 REG, PRESEASON SrcB blank |
| `scripts/validate_preseason_monitor.py` | **PASS** — 32 rows / 32 teams / 18 complete / 14 not played / 19 named blockers |
| `scripts/linkcheck_preseason.py` | **PASS** (format + host allowlist); network probe: 6/8 URLs reachable, 2 WARN |
| `tests/run_tests.py` | **PASS** — 13/13 |
| Idempotence | Monitor CSV **byte-identical** on second generation |

## Blockers

1. **Source access (2 URLs).** `covers.com` lineup pages return HTTP errors to direct HEAD requests (bot protection). Content was obtained via search indexing; the URLs are recorded but not independently re-fetchable from this environment. Affects DET / LAC / DEN rows — treated as `MEDIUM` confidence, not `HIGH`.
2. **Post-game participation unconfirmed for 6 Aug-13 teams** (IND, NE, HOU, ARI, TEN, SF) — no qualifying source located. Rows carry `Starter Use = TBD` with named blockers rather than an inferred value.
3. **PIT unresolved conflict** — head coach wanted Rodgers to take snaps; reporting indicates he likely sat. Both claims preserved; not silently resolved.
4. **Workbook access.** No write authorization; the Google Sheet was neither read nor modified. All findings are proposals only.
