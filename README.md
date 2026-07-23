# TTW NFL Power Ratings 2026 — Repository Manifest

This repository holds the "To The Window" NFL Power Ratings 2026 workbook and its
preseason-readiness audit trail.

## Workbooks

| File | Role | SHA-256 | Version banner |
|---|---|---|---|
| `TTW_NFL_v1_1_1 Version 2.xlsx` | **Authoritative source** (audited baseline — do not overwrite) | `243ce78fd0305f0f67afa35bc88e1b29beae4d464fa747e48a8c30952d032998` | `(v1.0)` — *known mislabel; workbook is canonically v1.1* |
| `TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx` | **Candidate (NOT authoritative)** — banner aligned to v1.1 + CHANGELOG note | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` | `(v1.1)` |

- **Canonical version: v1.1** (proven in `audit/Version_Evidence_Report.md`; no internal `v1.1.1` reference exists — the filename token `v1_1_1` is secondary evidence only).
- The candidate differs from the source in **exactly 5 cells**: `START HERE!A1` (banner v1.0→v1.1) and the four cells of a new CHANGELOG row 4. All 57,399 formulas, sheet order/visibility, schedule, sample/backtest data, and production-state inputs are identical.
- The source workbook is preserved byte-for-byte and remains the repository baseline. The candidate is **not** promoted; no live preseason-data entry has been performed.

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

## `scripts/` — reproducible, read-only audit + build tooling

`audit_workbook.py`, `schedule_audit.py`, `clean_state.py`, `ml_validate.py`,
`integrity.py`, `generate_grounding.py`, `version_evidence.py`,
`build_candidate.py`, `verify_candidate.py`, `changed_cells_and_parity.py`.

Requires `openpyxl` (`pip install openpyxl`). None of the audit scripts modify the
source; `build_candidate.py` reads the source and writes only the candidate file.

## Constraints honored

Source preserved byte-for-byte; no formulas, weights, thresholds, methodology,
backtest settings, schedule, sample data, MARKET LINES sample rows, QB values,
adjustments, team ratings, formatting, sheet order or visibility were changed.
Only the one proven version-label mislabel and a new CHANGELOG entry differ in the
candidate.
