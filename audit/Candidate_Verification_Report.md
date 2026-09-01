# Candidate Verification Report — v1.1 Version Alignment

**Source (audited baseline):** `TTW_NFL_v1_1_1 Version 2.xlsx`
**Candidate:** `TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx`
**Date:** 2026-07-23
**Build method:** surgical zip/XML edit — only `xl/sharedStrings.xml` (banner) and `xl/worksheets/sheet21.xml` (CHANGELOG row 4) rewritten; every other part copied byte-for-byte. openpyxl was **not** used to save (it would drop the 21 drawing parts and `persons/person.xml`).

## SHA-256

| File | SHA-256 | Size |
|---|---|---|
| Source (unchanged) | `243ce78fd0305f0f67afa35bc88e1b29beae4d464fa747e48a8c30952d032998` | 1,435,824 B |
| Candidate | `674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f` | 1,435,435 B |

The source SHA-256 is **identical** to the approved baseline audit — the source was preserved byte-for-byte.

## Verification results

| Check | Expected | Result | ✔ |
|---|---|---|---|
| Sheet count | 21 | 21 | ✔ |
| Sheet order | identical | identical | ✔ |
| Sheet visibility (11 visible / 10 hidden) | unchanged | unchanged | ✔ |
| Formula count | 57,399 | 57,399 | ✔ |
| Formula coordinates | identical set | identical | ✔ |
| Formula text | 0 differences | **0** | ✔ |
| 2026 regular-season games | 272 | 272 | ✔ |
| Zip members | 71, none added/removed | 71, none added/removed | ✔ |
| Drawings (×21) + `persons/person.xml` | byte-identical | byte-identical | ✔ |
| Zip members byte-identical | 69 of 71 | 69 of 71 (only the 2 edited differ) | ✔ |
| Production-state: usable market spreads | 0 | 0 | ✔ |
| Production-state: adjustments / QB deltas / team overrides | 0 / 0 / 0 | 0 / 0 / 0 | ✔ |
| Total cell differences | 5 (1 banner + 4 new CHANGELOG) | **5** | ✔ |

## The 5 changed cells (complete)

| Sheet!Cell | Old | New |
|---|---|---|
| `START HERE!A1` | `… NFL POWER RATINGS 2026 (v1.0)` | `… NFL POWER RATINGS 2026 (v1.1)` |
| `CHANGELOG!A4` | *(empty)* | `1.1` |
| `CHANGELOG!B4` | *(empty)* | `2026-07-23` |
| `CHANGELOG!C4` | *(empty)* | Version-label alignment (documentation only)… *(full text in `changed_cells.csv`)* |
| `CHANGELOG!D4` | *(empty)* | None. Documentation-only banner correction; metrics unchanged (Spread MAE 10.376; Totals MAE 10.787). |

No formula, schedule, 2025 sample/backtest, MARKET LINES sample, QB, adjustment, team-rating, setting, weight, threshold, methodology, formatting, sheet-order or visibility cell changed. Only the one proven mislabel and the new (previously empty) CHANGELOG row differ.

## Deliverables

- `TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx` — the candidate (non-authoritative).
- `audit/changed_cells.csv`, `audit/changed_cells.json` — the 5 changed cells.
- `audit/version_evidence.json` + `Version_Evidence_Report.md` — canonical-version proof.
- `audit/candidate_verification.json` — machine-readable verification (this report's data).
- `scripts/build_candidate.py`, `scripts/verify_candidate.py`, `scripts/changed_cells_and_parity.py` — reproducible build + checks.

## Status note

This candidate is **not** promoted to authoritative status. The audited source workbook remains the repository baseline. No live preseason-data entry was performed.

## Reproduction

```bash
python3 scripts/version_evidence.py            # canonical-version evidence
python3 scripts/build_candidate.py             # build candidate from source
python3 scripts/verify_candidate.py            # full source-vs-candidate verification
python3 scripts/changed_cells_and_parity.py    # changed-cell CSV/JSON + byte parity
```
