# TTW NFL 2026 — Phase 5C Production Promotion: **HALTED BEFORE ANY WRITE**

# Status: **NOT PROMOTED — connector cannot perform cell-level writes**

**Production was read, never written.** The authoritative Sheet is byte-for-byte in its pre-approval state, PR #1 is still a draft, and no cell anywhere was modified. Per your standing instruction — *"If the available connector cannot perform cell-level writes, do not replace the entire production file or improvise another method. Stop and provide the exact manual copy ranges"* — I stopped at the write boundary and produced the manual application pack in §4.

---

## 1. Production preflight — identity confirmed

| Field | Value |
|---|---|
| **Title** | `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE` |
| **File ID** | `1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew` |
| **modifiedTime** | **2026-09-01T04:25:11.009Z** — byte-identical to the timestamp the promotion manifest was built against |
| createdTime | 2026-07-23T11:23:20.760Z |
| Owner | normanjemia@gmail.com · MIME `application/vnd.google-apps.spreadsheet` |
| Current version | Banner reads **v1.1**; latest CHANGELOG entry is **1.1-W1 (2026-09-01)**; row 7 empty |
| Preflight read at | 2026-09-01T14:32Z |

Identity matches the approved target exactly. **No drift**: `modifiedTime` has not advanced since the manifest baseline was captured.

## 2. Rollback checkpoint captured

A fresh full export was taken before anything else and committed as
`TTW_NFL_2026_PROD_ROLLBACK_CHECKPOINT_20260901T1432Z.xlsx` — 1,349,749 bytes, SHA-256 `e3349d8ee42fedae6cc411e9ca92f68bc6f7cd9c2ae2f378393bdc2d28199ce9`.

> This checkpoint's SHA differs from the Phase-3 base export (`39c7c567…`) purely because Google repackages the archive on every export. Content equality was therefore verified **semantically**, and is exact — see §3.

## 3. Drift check against the manifest baseline — **15 checks, 0 failed**

| Check | Result |
|---|---|
| Tab count and order | 22, matching |
| Formula count | **57,399** fresh vs 57,399 baseline |
| Formula drift | **0 of 57,399** differ |
| Constant drift | **0** differ |
| **All 133 target cells at expected pre-promotion values** | **133/133 match the manifest "Before" column** |
| Source B blank in all 32 rows | ready to receive |
| Source C blank in all 32 rows | confirmed |
| GP = 0 for all 32 | confirmed |
| `TEAM RATINGS D5:D36` still reads `0` | 32/32 — the defect is still present, as the manifest assumes |
| WinTotalsMode | VALIDATE-ONLY |
| Banner | still v1.1 |
| CHANGELOG row 7 | still empty |
| DAL pre-promotion | −2.26, rank 27 |
| NYG pre-promotion | −1.59, rank 24 |

Production is exactly where the manifest expects it. **Everything was ready to write.**

## 4. Why the write did not happen

The Google Drive connector exposes only file-level operations. Its complete tool surface is `get_file_metadata`, `search_files`, `list_recent_files`, `read_file_content`, `download_file_content`, `create_file`, `copy_file`, `update_file`, `share_file`, `get_file_permissions`, `trash_file`. **`update_file` accepts only `title` and `parentId`** — there is no Sheets API binding and therefore no way to set a cell, a range, or a formula.

The three workarounds were all considered and rejected as violating your instruction or your constraints:

- **Replacing the file wholesale** via `create_file`/upload — explicitly forbidden, and it would destroy the Sheet ID, sharing, and version history you required be preserved.
- **`copy_file` then swap** — same identity destruction, and it cannot apply the change sets anyway.
- **Any scripted/App Script route** — improvising another method, explicitly forbidden.

So the promotion stops here, with production untouched and a verified-ready manual pack below.

---

## 5. Exact manual copy ranges — 133 cells in 5 paste operations

Paste-ready files are committed under `promotion/manual_apply_v14/` and attached in chat. Each was verified to reproduce the approved candidate exactly.

> **Critical:** `PRESEASON` column **J** sits between I and K/L and holds a **formula**. Never paste across I→L in one action; that would overwrite J. Use the two separate blocks below.

### Order of operations

**0. Before touching anything:** in the Sheet, **File → Version history → Name current version** → `pre-v1.4 promotion 2026-09-01`. This is your one-click rollback.

| # | Target range | Source file | What it is | Cells |
|---|---|---|---|---|
| 1 | `PRESEASON!I5:I36` | `block1_PRESEASON_I5_I36.tsv` | 32 Source B composite values (single column) | 32 |
| 2 | `PRESEASON!K5:L36` | `block2_PRESEASON_K5_L36.tsv` | 32 source citations + 32 as-of dates (two columns) | 64 |
| 3 | `TEAM RATINGS!D5` then fill down to `D36` | `block3_TEAMRATINGS_D5_formula.txt` | the ISNUMBER formula — relative refs make fill-down exact | 32 |
| 4 | `START HERE!A1` | `block4_STARTHERE_A1_banner.txt` | version banner v1.1 → v1.4 | 1 |
| 5 | `CHANGELOG!A7:D7` | `block5_CHANGELOG_A7_D7.tsv` | the v1.4 entry (4 cells, one row) | 4 |
| | | | **Total** | **133** |

### Paste settings that matter

- Paste with **Ctrl+Shift+V (paste values only)** for blocks 1, 2 and 5, so no formatting is carried in.
- Block 2's as-of column must land as the **text** `2026-09-01`, matching the existing SrcA as-of convention in column G. If Sheets auto-converts it to a date, format the range as **Plain text** first, or prefix nothing and re-check — the verification script in §6 will catch it either way.
- Block 3: type or paste the formula into `D5` only, then select `D5:D36` and **Ctrl+D** to fill down. Do **not** paste the same absolute text into all 32 rows — the row references must increment.
- **Do not type into any of the 226 recalculated cells** (`PRESEASON J/S/T`, `TEAM RATINGS D/F/H/J/K` outputs, ENGINE, DASHBOARD). They recompute on their own; typing into them destroys formulas.

### Expected immediately after block 3

`TEAM RATINGS D5:D36` goes **blank** (not `0`) and every EFFECTIVE RATING jumps to its full preseason prior — DAL to **−1.07 / rank 22**, NYG to **−1.90 / rank 24**.

## 6. Verification after you apply it

Export the Sheet (File → Download → Microsoft Excel) and run:

```
python3 scripts/verify_native_import_5b.py <downloaded_export.xlsx>
```

That is the same 36-check suite that passed on the full-import test copy: it re-verifies all 133 written cells by readback, all 226 recalculations, the GP=0 fallback for all 32 teams, 16/16 ENGINE and DASHBOARD rows, the five DAL/NYG pins, formula count and coordinates, and that exactly the six pre-existing `#DIV/0!` errors remain with zero new errors. Send me the export and I will run it and produce the production execution report.

## 7. Rollback if anything looks wrong

1. **File → Version history → restore** `pre-v1.4 promotion 2026-09-01`. Single action, reverts everything including recalculated cells.
2. If version history is unavailable, the committed checkpoint `TTW_NFL_2026_PROD_ROLLBACK_CHECKPOINT_20260901T1432Z.xlsx` (SHA `e3349d8e…`) reproduces the exact pre-promotion state.
3. Partial rollback: clear `PRESEASON I5:I36`, `K5:L36` to undo Source B; restore `TEAM RATINGS D5:D36` to `=IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),"")` to undo the fix. The two change sets are independent.

## 8. What is unchanged

Sheet ID, sharing, tab structure and version history are untouched because nothing was written. Source C blank, VALIDATE-ONLY, weights 0.40/0.35/0.25, all thresholds, QB values, market lines, overrides, adjustments and every unrelated cell remain exactly as the preflight found them.

**PR #1 remains a draft. Stopped for final owner review.**
