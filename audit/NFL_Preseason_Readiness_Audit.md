# NFL Preseason Readiness — Baseline Audit

**Workbook:** `TTW_NFL_v1_1_1 Version 2.xlsx`
**Audit date:** 2026-07-23
**Branch:** `claude/nfl-preseason-readiness-audit-unvx7i`
**Phase:** Baseline Audit → Clean Production State → Workflow Preparation
**Method:** Read-only inspection with `openpyxl` (formulas and cached computed values). The source workbook was **not** modified. All figures below are reproducible via the scripts in `scripts/` and the machine-readable snapshot in `audit/grounding.json`.

---

## 1. Grounded workbook facts

| Fact | Value |
|---|---|
| `.xlsx` workbooks in repo | **Exactly 1** (`TTW_NFL_v1_1_1 Version 2.xlsx`) |
| SHA-256 | `243ce78fd0305f0f67afa35bc88e1b29beae4d464fa747e48a8c30952d032998` |
| File size | `1,435,824` bytes |
| Sheet count | **21** |
| Visible sheets | 11 |
| Hidden sheets | 10 |
| Total formula cells | **57,399** |
| Internal version banner (`START HERE!A1`) | `TO THE WINDOW — NFL POWER RATINGS 2026 (v1.0)` |
| CHANGELOG versions present | `1.0` (2026-01-05), `1.1` (2026-07-13) |
| Error cells (cached) | **6** — all `#DIV/0!`, all expected preseason mean-checks (see §5) |
| SETTINGS: Current season / week / as-of | `2026` / `1` / `2026-07-13` |
| SETTINGS: Win-totals mode | `VALIDATE-ONLY` |

### Sheet order & state

Order (left→right): START HERE, DASHBOARD, ENGINE, MARKET LINES, ADJUSTMENTS, QB VALUES, TEAM RATINGS, DATA QUALITY, SETTINGS, IMPORT SCHEDULE, IMPORT STATS, MAP, CLEAN, CALC, LISTS, PRESEASON, HISTORY 2025, BACKTEST, AUDIT, DICTIONARY, CHANGELOG.

- **Visible (11):** START HERE, DASHBOARD, ENGINE, MARKET LINES, ADJUSTMENTS, QB VALUES, TEAM RATINGS, DATA QUALITY, SETTINGS, IMPORT SCHEDULE, IMPORT STATS
- **Hidden (10):** MAP, CLEAN, CALC, LISTS, PRESEASON, HISTORY 2025, BACKTEST, AUDIT, DICTIONARY, CHANGELOG

All 10 hidden sheets use Excel state `hidden` (none `veryHidden`). This matches the START HERE tab map ("Hidden: MAP/CLEAN/CALC … the pipeline — unhide to audit, never edit").

### Formula cells by sheet

| Sheet | Formulas | | Sheet | Formulas |
|---|---:|---|---|---:|
| ENGINE | 12,900 | | IMPORT STATS | 620 |
| CLEAN | 33,120 | | TEAM RATINGS | 480 |
| DATA QUALITY | 4,505 | | ADJUSTMENTS | 300 |
| MARKET LINES | 2,400 | | DASHBOARD | 274 |
| CALC | 1,289 | | PRESEASON | 192 |
| IMPORT SCHEDULE | 1,114 | | QB VALUES | 160 |
| MAP | 39 | | START HERE | 6 |
| SETTINGS, LISTS, HISTORY 2025, BACKTEST, AUDIT, DICTIONARY, CHANGELOG | 0 | | **Total** | **57,399** |

---

## 2. Schedule audit

Source: `IMPORT SCHEDULE` (raw `games.csv` paste zone), data rows 6→562.

| Season | Games | Scored | Unscored |
|---|---:|---:|---:|
| 2025 | 285 | 285 | 0 |
| 2026 | 272 | 0 | 272 |
| **Total** | **557** | 285 | 272 |

By game type:

- **2025:** 272 REG + 6 WC + 4 DIV + 2 CON + 1 SB = **285** (full 2025 season incl. playoffs, fully scored — the historical sample).
- **2026:** **272 REG**, zero postseason, all unscored.

**Confirmation:** the 2026 schedule count is **272 regular-season games** = 32 teams × 17 games ÷ 2, i.e. exactly one complete NFL regular season, with no scores (as expected for an upcoming season). ✔

---

## 3. 2025 sample / backtest data & 2026 preseason data

**Both are present, as designed.**

- **2025 sample/backtest data — PRESENT:**
  - `IMPORT SCHEDULE` holds all 285 scored 2025 games.
  - `HISTORY 2025` (hidden): real per-game walk-forward sample (model margin, result, spread error, ref line, edge).
  - `BACKTEST` (hidden): calibration report — Spread MAE **10.376** vs Vegas **9.993**; Total MAE **10.795** vs Vegas **10.082**; edge-bucket hit rates. Matches CHANGELOG headline figures.
- **2026 preseason data — PRESENT:**
  - `PRESEASON` (hidden): 32-team 2026 priors pre-loaded (Source = "TTW model, 2025 wk1-18 final", as-of 2026-01-05), feeding the week-indexed preseason→current blend.
  - `SETTINGS`: Current season 2026, Week 1, preseason blend schedule (0.8 wk1 → 0.1 wk8+), priors regression 0.33.

---

## 4. Formula audit

- **57,399 formula cells** across 14 sheets; heaviest are CLEAN (33,120) and ENGINE (12,900).
- **Only 6 cached error cells**, all `#DIV/0!`, all in mean-check diagnostics (see §5). No `#REF!`, `#NAME?`, `#VALUE!`, `#N/A`, or spill errors anywhere.
- Array formulas drive the ENGINE / MARKET LINES / TEAM RATINGS grids; named ranges (CurrentWeek, EngWeek, QBDeltaCap, StaleDays, MinGamesTrust, etc.) resolve cleanly.
- Input-validation and staleness formulas are live and working (demonstrated by the sample block in §6).

---

## 5. The 6 `#DIV/0!` cells — expected preseason state, **not a defect**

| Cell | Formula | Meaning |
|---|---|---|
| `CALC!B39` | `=ROUND(AVERAGE($F$2:$F$33),6)` | Mean check P0c |
| `CALC!B40` | `=ROUND(AVERAGE($I$2:$I$33),6)` | Mean check P1c |
| `CALC!B41` | `=ROUND(AVERAGE($L$2:$L$33),6)` | Mean check P2c |
| `CALC!B42` | `=ROUND(AVERAGE($O$2:$O$33),6)` | Mean check P3c |
| `CALC!B43` | `=ROUND(AVERAGE($AC$2:$AC$33),6)` | Mean check P3cPv |
| `DATA QUALITY!B8` | `=ABS(CALC!$B$42)` | "Rating mean check \|avg P3c\| (should be ~0)" mirror |

These average the opponent-adjusted rating columns across the 32 team rows. In the current clean preseason state **no 2026 in-season stats are loaded** (`IMPORT STATS` empty, Week 1), so those ranges are empty and `AVERAGE()` of an empty range is undefined → `#DIV/0!`. They resolve to real numbers the instant weekly stats are pasted.

- They are internal diagnostics; they **block nothing** — the START HERE step-8 readiness gate keys off per-game `DQStatus="BLOCKED"`, not these cells (`DATA QUALITY` reports 0 BLOCKED / 0 WARNING / 0 unmatched).
- "Fixing" the cosmetic error would require wrapping the formulas in `IFERROR`, i.e. **changing formulas** — explicitly prohibited by the audit constraints. Left as-is.

---

## 6. Production-state counts (Clean Production State)

The workbook ships in a **clean production state** — no live current-season market, injury, depth-chart, or betting inputs:

| Input surface | Count | Status |
|---|---:|---|
| MARKET LINES — cells producing a **usable market spread** (`col Q` non-blank) | **0** | ✔ clean |
| MARKET LINES — raw manual input cells present | 48 (16 rows) | Inert sample — see below |
| ADJUSTMENTS — manual adjustment cells | **0** | ✔ clean |
| QB VALUES — rows with non-zero delta (Active ≠ Baseline) | **0** (of 32) | ✔ baseline only |
| TEAM RATINGS — manual override cells (`col I`) | **0** | ✔ clean |
| SETTINGS — Team HFA exceptions entered | **0** | ✔ clean |
| DATA QUALITY — Games BLOCKED (current week) | **0** | ✔ clean |
| DATA QUALITY — Games WARNING (current week) | **0** | ✔ clean |
| DATA QUALITY — Unmatched team names (whole file) | **0** | ✔ clean |

### The 48 MARKET LINES sample cells (rows 261–276) — investigated, benign

These 16 rows carry static `Favorite / Spread / Total` values labelled `Source = "NFLVERSE-HIST (sample)"`, `Notes = "SAMPLE — historical reference line"`, line date `2026-01-01`. They are **not** live current betting information. The audit confirmed they are inert:

1. **Self-flagged invalid.** Every row's `Input check` (`col R`) computes **`⚠ FAVORITE NOT IN GAME`** — the static favorite (ATL, BUF, CHI, …) does not match either team of the schedule-driven game the row aligns to (e.g. `Favorite='ATL'` on `2026_18_SF_ARI`).
2. **Produce no market number.** Because the favorite matches neither Home nor Away, `Market home spread` (`col Q`) returns **blank** for all 16 rows → **0 usable market spreads workbook-wide**. The ENGINE therefore receives no line from them and computes no edge against them.
3. **Marked STALE.** As-of 2026-07-13 vs line date 2026-01-01 → all flagged `STALE`.
4. **Dormant by week.** They align to **2026 Week 18** games; the current week is 1, so they are outside every current/near-term filter. If a user ever reaches Week 18, pasting real lines overwrites them.

They function as a live demonstration of the input-validation + staleness machinery (part of the workbook's "receipts" design) and **cannot contaminate any real 2026 edge calculation**. No action taken.

---

## 7. Defects found & repair-candidate decision

**No genuine functional defect was found. No repair candidate workbook was required or created.**

Two items were examined as candidates and both cleared:

| Item | Assessment | Action |
|---|---|---|
| 6 `#DIV/0!` mean-check cells | Expected preseason state (empty stat ranges); blocks nothing; a "fix" would require changing formulas (prohibited) | Documented, not modified |
| 48 sample MARKET LINES cells on 2026 Wk18 | Labelled sample; self-flagged `⚠ FAVORITE NOT IN GAME`; yields 0 usable market spreads; STALE; dormant | Documented, not modified |

**Observation (non-blocking, documentation only):** the user-facing banner `START HERE!A1` still reads **`(v1.0)`**, while the workbook is internally **v1.1** (CHANGELOG row for 1.1 dated 2026-07-13; SETTINGS parameter-freeze note "frozen as of v1.1 (2026-07-13)"; DICTIONARY "v1.1 …" entries; filename `v1_1_1`). This is a cosmetic version-label lag with **zero functional impact**. Because the constraints bar modifying the source without a proven genuine defect, this is reported for the owner's decision rather than auto-edited.

---

## 8. Workflow preparation

- Audit is fully reproducible: `scripts/*.py` (read-only) + `audit/grounding.json` (machine-readable snapshot). Re-running any script against the workbook regenerates these figures.
- Source workbook left byte-for-byte unchanged (SHA-256 above is the shipping baseline; re-hash before/after any future session to detect drift).
- Weekly routine is intact (START HERE steps 1–8; live status gates on SETTINGS week/date, schedule load count, QB completeness, market-line completeness, and DATA QUALITY blocks).
- Clean-state confirmed: no market/injury/adjustment/override inputs to strip before the 2026 season begins.

---

## Reproduction

```bash
pip install openpyxl
python3 scripts/generate_grounding.py      # -> audit/grounding.json (all grounded facts)
python3 scripts/audit_workbook.py          # sheet/formula/state grounding
python3 scripts/schedule_audit.py          # schedule counts
python3 scripts/clean_state.py             # production-state input counts
python3 scripts/ml_validate.py             # sample market-line validation proof
python3 scripts/integrity.py               # error-cell + DQ summary scan
```
