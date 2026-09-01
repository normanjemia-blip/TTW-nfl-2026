# TTW NFL 2026 — v1.4 Production Execution Report (2026-09-01)

# RESULT: **PASS** — 63 checks across two suites, 0 failed

**v1.4 is live in production.** The 133-cell promotion was applied by Codex; this report is the independent post-promotion verification. **This verification was strictly read-only — I wrote nothing to production.** PR #1 remains a draft.

| | |
|---|---|
| **Sheet** | `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE` · ID `1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew` |
| **modifiedTime after promotion** | **2026-09-01T16:50:10.503Z** — matches the reported promotion timestamp exactly |
| Identity preserved | Same Sheet ID, title, `createdTime` (2026-07-23T11:23:20.760Z) and parent folder |
| **Native pre-write rollback copy** | `TTW_NFL_Power_Ratings_2026_PRE_v1.4_ROLLBACK_20260901T165005Z` · ID `1EoPQ4ishczoI6x-pQAkYTzmewm3CmSVrFpw1lVzbWY8` · created **2026-09-01T16:50:06.033Z**, i.e. **4.5 seconds before** the write landed — confirmed to exist and to pre-date the promotion |
| Verified at | 2026-09-01T17:05Z · **3 Drive calls** (metadata ×2, one export) |
| Post-promotion export | 1,351,146 bytes, SHA-256 `fde0164c554283118ac6b14a6e765c5abc474add79ad845067cc94c48cb92da8`, committed as `TTW_NFL_2026_PROD_POSTPROMOTION_20260901T1650Z.xlsx` |

> Export SHAs differ run-to-run because Google repackages the archive on every export; all verification below is therefore semantic, driven off the promotion manifest itself.

---

## 1. Readback of the 133 written cells — **133/133 PASS**

Every directly-entered cell was read back from production and compared against the manifest's `After` column:

| Range | Cells | Result |
|---|---|---|
| `PRESEASON!I5:I36` — Source B composite values | 32 | **32/32 exact** |
| `PRESEASON!K5:K36` — source citations | 32 | **32/32 exact** |
| `PRESEASON!L5:L36` — as-of `2026-09-01` | 32 | **32/32 exact** |
| `TEAM RATINGS!D5:D36` — ISNUMBER formula | 32 | **32/32 text-exact, row references correctly incremented** |
| `START HERE!A1` — banner | 1 | **v1.4** |
| `CHANGELOG!A7:D7` — v1.4 entry | 4 | **exact** |

Per-cell evidence: `audit/TTW_NFL_2026_Production_Readback_20260901.csv`.

## 2. The 226 recalculated cells — **PASS**

- **224 individually-addressed cells** (`PRESEASON J/S/T` and `TEAM RATINGS F/H/J/K`, 32 rows each) were read back and **all 224 match** their expected post-promotion values.
- The manifest's remaining 2 rows are range entries — `TEAM RATINGS D5:D36` and `ENGINE / DASHBOARD all Week-1 rows` — covered by the dedicated checks in §3 and §5 rather than by single-cell readback.

**No recalculated cell was overwritten with a literal**: all 57,399 formulas are present with identical coordinates and identical text to the approved candidate.

## 3. GP = 0 fallback — **32/32 PASS**

| Check | Result |
|---|---|
| GP = 0 for all 32 teams | **PASS** |
| `TEAM RATINGS D5:D36` genuinely **blank**, not numeric 0 | **32/32 blank** |
| `F = H = J = PRESEASON!S` (100% of the preseason prior retained) | **32/32** |

This is the defect the release existed to fix, now confirmed corrected in production: before promotion those cells read `0` and every rating sat at 80% of its prior.

## 4. Formula integrity — **PASS**

Formula count **57,399** · coordinates **identical** to the approved candidate (symmetric difference 0) · formula text **57,399/57,399 identical**. Nothing was added, removed, or displaced.

## 5. Week-1 slate reconciliation — **16/16 PASS**

All 16 ENGINE rows match `audit/TTW_NFL_2026_Candidate_Week1_Slate_20260901.csv` on FinalMargin, fair line, spread edge and supported side. DASHBOARD renders 16 games. Row-by-row output is in the readback CSV.

### The five pins, in production

| Pin | Required | Production |
|---|---|---|
| DAL | −1.07, rank 22 | **−1.07, rank 22** ✓ |
| NYG | −1.90, rank 24 | **−1.90, rank 24** ✓ |
| DAL@NYG FinalMargin | +0.77 | **+0.77** ✓ |
| Fair line | NYG −0.8 | **NYG −0.8** ✓ |
| Edge | +3.27 on NYG +2.5 | **+3.27, NYG +2.5** ✓ |

## 6. Error budget — **exactly 6 inherited, 0 new — PASS**

Every cell on all 22 tabs was scanned for `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#ERROR!`.

- **6 errors total, 0 new.** They are exactly the documented pre-existing set: `CALC!B39:B43` and `DATA QUALITY!B8` (empty-range `AVERAGE` at zero games played — see `audit/DQ_DIV0_Diagnosis.md`).
- **Count unchanged across the promotion**: 6 before → 6 after, measured against the pre-promotion checkpoint.
- No circular-reference markers.

## 7. Everything else preserved — **PASS**

Cell-for-cell identical to the pre-promotion checkpoint: **MARKET LINES, QB VALUES, ADJUSTMENTS, PRESEASON MONITOR, IMPORT SCHEDULE**. Source C blank in all 32 rows · WinTotalsMode **VALIDATE-ONLY** · weights **0.40 / 0.35 / 0.25** in all 32 rows · ATS BET **1.5**, INVESTIGATE **1.5**, LEAN **1.0** · Enable BET labels **Y** · Week-1 blend weight 0.80 · 22 tabs, unchanged structure.

## 8. What actually changed in production

27 of 32 ranks moved. Mean absolute rating change **0.84 pts**, max **2.09**.

| Largest gains | | Largest declines | |
|---|---|---|---|
| BAL +1.54 (r10→5) | BUF +1.42 (r8→3) | ARI −2.09 (r26→29) | MIA −1.85 (r29→30) |
| LA +1.27 (r2→1) | **DAL +1.19 (r27→22)** | CLE −1.20 (r28→27) | ATL −1.00 (r19→21) |
| KC +1.06 (r18→15) | | LV −0.98 (r31→31) | |

**Week-1 edges of 3.0+ fell from five to two** (ARI +10.5 at −3.58; NYG +2.5 at +3.27) — the intended effect of adding Source B and removing the unintended 20% Week-1 compression.

## 9. Rollback, if ever needed

1. **Native pre-write copy** `1EoPQ4ishczoI6x-pQAkYTzmewm3CmSVrFpw1lVzbWY8`, created 4.5 s before the write — the fastest restore path.
2. **File → Version history** on the production Sheet, restoring the version named before promotion.
3. Committed exports: `TTW_NFL_2026_PROD_ROLLBACK_CHECKPOINT_20260901T1432Z.xlsx` (pre, SHA `e3349d8e…`) and `TTW_NFL_2026_PROD_POSTPROMOTION_20260901T1650Z.xlsx` (post, SHA `fde0164c…`).
4. Partial rollback remains available per `TTW_NFL_2026_Promotion_Manifest_v14_20260901.md` §5 — the two change sets are independent.

## 10. Verdict

**PASS.** The promotion applied exactly the approved 133 cells and nothing else. All 224 individually-addressed recalculations landed correctly, the GP=0 fallback holds for all 32 teams, formula count and coordinates are untouched, the slate reconciles 16/16, all five pins hold, and the error budget is unchanged at exactly six inherited errors with zero new ones.

**Production is now v1.4.** PR #1 remains a draft; nothing was written to production during this verification.

### Follow-ups for the owner

1. The **repo's `run_gates.py` still audits the v1.1 workbook** (`SETTINGS!B7 = 2026-07-13`, `PRESEASON SrcB blank`) and therefore still reports the pre-promotion shape. That is correct today — the repo workbook was deliberately never modified — but now that production is v1.4, decide whether the repo's authoritative copy should be refreshed from production and the gate baselines re-pinned.
2. Source C stays **VALIDATE-ONLY** pending the 2.1 pts/win calibration test (audit report §8).
3. PR #1 merge decision (`TTW_NFL_2026_Candidate_Verification_20260901.md` §6).
