# TTW NFL Power Ratings 2026 — Repository Manifest

This repository holds the "To The Window" NFL Power Ratings 2026 workbook, its
preseason-readiness audit trail, and the v1.1 promotion record.

## Authoritative version: **v1.1 (native Google Sheet)**

As of 2026-07-23, **v1.1 is authoritative**. It passed native Google Sheets
round-trip verification (**PASS — 21/21 checks**) and now lives as the native
Google Sheet:

- **Native Google Sheet ID:** `1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`
- **URL:** https://docs.google.com/spreadsheets/d/1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew
- **Promoted XLSX source SHA-256:** `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f`
- **Round-trip XLSX SHA-256:** `fbfda1be9657b422e502baa5761fb4907e8e21f4908f5c1751b7c4ab715ab0fb`

Round-trip evidence is in [`promotion/`](promotion/). All 57,399 formulas
(coordinates, text, cached values), constants, drawings/persons, defined names,
data validations, meaningful cell styles, the 272 unscored 2026 REG games, the
clean production state (0 usable market spreads / adjustments / QB deltas / team
overrides), the v1.1 banner, and the CHANGELOG alignment entry all verified
identical across the round trip. The 24 changed package parts are accepted,
behavior-neutral Google re-packaging differences (style dedup, formatting-only
cell/column trimming, named-range/validation reordering) — see the report.

## Workbooks

| File | Role | SHA-256 | Version banner |
|---|---|---|---|
| `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx` | **Authoritative v1.1 XLSX source** — the exact package promoted to the native Sheet (renamed from `…_VERSION_ALIGNMENT_CANDIDATE.xlsx` via `git mv`; content SHA-256 unchanged) | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` | `(v1.1)` |
| `TTW_NFL_v1_1_1 Version 2.xlsx` | **Preserved provenance / rollback** — the original uploaded, audited baseline; keep byte-for-byte, do not overwrite | `243ce78fd0305f0f67afa35bc88e1b29beae4d464fa747e48a8c30952d032998` | `(v1.0)` — *original mislabel; superseded by v1.1* |
| `TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx` | **Working copy (NOT authoritative)** — QB VALUES manual fields populated from live Aug-2026 research; QB deltas all 0 (model output unchanged). Built by surgical edit of the QB sheet only (SHA-256 `2d9d36d0b17b4acb7fa7ae1122d94d5adab57413336b029112ad430415ad4c7d`) | — | `(v1.1)` |
| `TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx` | **Candidate (NOT authoritative)** — approved LV QB deviation entered (Cousins +0.50); 29 OK / 3 UNCERTAIN (SHA-256 `e6efbbb3a2b75c76f57bf13906de84f50aefd25ea05d59ef6ddba56aa2aee136`) | — | `(v1.2.1)` |
| `TTW_NFL_Power_Ratings_2026_v1.3_MARKET_CANDIDATE.xlsx` | **Candidate (NOT authoritative)** — Week 1 market lines populated (2026-05-15 DraftKings OPENING lines; all 16 rows flag STALE) (SHA-256 `1e9cb2c564bbe26c5da810b6cefcfba2ce163ee62271c40c49fc4a4dfa50bf9d`) | — | `(v1.3)` |

- **QB Preseason Activation Phase 1 (2026-08-05):** all 32 QB situations researched from current sources. 28 settled (0/0, High), 3 uncertain (ATL/CLE/MIN, blank/Low), 1 deviation (LV: Cousins over priced-in Mendoza). Deliverables in `audit/qb_*`.
- **Phase 2 — Market Lines (2026-08-06):** Week 1 rows 5–20 populated with the **2026-05-15 DraftKings OPENING lines** (favorite + positive spread + total), recorded with true source/line date. **Not current** — all 16 rows flag `STALE` against the 2026-07-13 As-of date and must be refreshed with Novig lines before live use. QB values, adjustments and team ratings unchanged. See `audit/Market_Candidate_v1_3_Verification_Report.md`.
- **QB Candidate v1.2.1 (2026-08-05):** approved LV deviation entered — Baseline Fernando Mendoza = 0, Active Kirk Cousins = **+0.50**, Confidence High. Exactly one non-zero QB delta league-wide; **29 OK / 3 UNCERTAIN** (ATL, CLE, MIN left blank/Low by design). 57,399 formulas unchanged. Candidate is **not promoted**; authoritative v1.1 and the native Google Sheet untouched.
- **Canonical version: v1.1** (proven in `audit/Version_Evidence_Report.md`; no internal `v1.1.1` reference exists — the filename token `v1_1_1` is secondary evidence only).
- The authoritative v1.1 XLSX differs from the original baseline in **exactly 5 cells**: `START HERE!A1` (banner v1.0→v1.1) and the four cells of a new CHANGELOG row 4. All 57,399 formulas, sheet order/visibility, schedule, sample/backtest data, and production-state inputs are identical.
- The original uploaded workbook is retained **byte-for-byte** as provenance and rollback. No live market-line, injury, QB, or weekly-stat entry has been performed.

## Grounded facts (source workbook)

- 21 sheets (11 visible / 10 hidden); 57,399 formula cells.
- Schedule: 2026 = **272** regular-season games (unscored); 2025 = 285 games (scored, incl. playoffs — the historical sample).
- 2025 sample/backtest data and 2026 preseason priors both present.
- Clean production state: 0 usable market spreads, 0 adjustments, 0 non-zero QB deltas, 0 team overrides, 0 DATA QUALITY blocks.
- 6 `#DIV/0!` cells are expected preseason mean-checks (resolve once weekly stats load), not defects.

## `audit/` — documentation & machine-readable data

| File | Contents |
|---|---|
| `NFL_Preseason_Readiness_Audit.md` | Phase 1 baseline audit (grounding, schedule, formula, production-state, defect findings). |
| `grounding.json` | Reproducible grounded-facts snapshot of the source. |
| `Version_Evidence_Report.md` | Canonical-version determination + per-cell `v1.0` classification. |
| `version_evidence.json` | Raw version-token evidence. |
| `Candidate_Verification_Report.md` | Full source-vs-candidate verification for the v1.1 candidate. |
| `candidate_verification.json` | Machine-readable verification results. |
| `changed_cells.csv` / `changed_cells.json` | The exact 5 changed cells (old → new). |

## `promotion/` — v1.1 authoritative round-trip evidence

| File | Contents |
|---|---|
| `nfl_v11_roundtrip_verification.md` | Native Google Sheets round-trip verification report (**PASS**, 21/21 checks). |
| `nfl_v11_roundtrip_verification.json` | Machine-readable round-trip results (SHAs, checks, schedule, production state, accepted package differences). |
| `verify_roundtrip.py` | The verification script that produced the report/JSON (compares the promoted XLSX against the round-tripped export). |

## `scripts/` — reproducible, read-only audit + build tooling

`audit_workbook.py`, `schedule_audit.py`, `clean_state.py`, `ml_validate.py`,
`integrity.py`, `generate_grounding.py`, `version_evidence.py`,
`build_candidate.py`, `verify_candidate.py`, `changed_cells_and_parity.py`.

Requires `openpyxl` (`pip install openpyxl`). None of the audit scripts modify the
source; `build_candidate.py` reads the source and writes only the candidate file.

## Constraints honored

Original baseline preserved byte-for-byte; no formulas, weights, thresholds,
methodology, backtest settings, schedule, sample data, MARKET LINES sample rows,
QB values, adjustments, team ratings, formatting, sheet order or visibility were
changed. Only the one proven version-label mislabel and a new CHANGELOG entry
differ in the authoritative v1.1 XLSX. The v1.1 promotion (this manifest +
`promotion/`) is documentation-only: no workbook or Google Sheet was modified
during closeout, and no live preseason-data entry was performed.
