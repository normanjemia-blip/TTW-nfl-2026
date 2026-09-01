# DATA QUALITY rating-mean `#DIV/0!` — Diagnosis and Proposed Patch

**Checkpoint:** 2026-08-15 · **Workbook inspected:** `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx` (read-only)
**Live sheet modified:** NO. **Workbook modified:** NO. This is a proposed patch plus a repo-local test only.

## Verdict: harmless-to-output, but a real monitoring defect (missing empty-range guard)

It is **not** a calculation failure and it does **not** corrupt any rating. It **is** a genuine defect in the sense that the DATA QUALITY panel displays a permanent error state that will mask a real future failure.

## Affected cells (6)

| Cell | Formula | Cached |
|---|---|---|
| `CALC!B39` | `=ROUND(AVERAGE($F$2:$F$33),6)` | `#DIV/0!` |
| `CALC!B40` | `=ROUND(AVERAGE($I$2:$I$33),6)` | `#DIV/0!` |
| `CALC!B41` | `=ROUND(AVERAGE($L$2:$L$33),6)` | `#DIV/0!` |
| `CALC!B42` | `=ROUND(AVERAGE($O$2:$O$33),6)` | `#DIV/0!` |
| `CALC!B43` | `=ROUND(AVERAGE($AC$2:$AC$33),6)` | `#DIV/0!` |
| `DATA QUALITY!B8` | `=ABS(CALC!$B$42)` | `#DIV/0!` (mirror) |

## Root cause (measured, not inferred)

Each source range `CALC!F2:F33`, `I2:I33`, `L2:L33`, `O2:O33`, `AC2:AC33` currently contains **0 numeric values** — every cell is a formula returning text-blank `""` because no 2026 in-season stats are loaded (Week 1, `IMPORT STATS` empty). `AVERAGE()` over a range with zero numerics is undefined → `#DIV/0!`. The formulas are correct; they simply lack an empty-range guard.

## Consumer trace (why it is not currently dangerous)

Only **one** consumer exists workbook-wide:

- `DATA QUALITY!B8` = `=ABS(CALC!$B$42)` — a **display** row labelled "Rating mean check |avg P3c| (should be ~0)".

Nothing else reads `CALC!B39:B43`. Critically, the readiness gate keys off per-game `DQStatus="BLOCKED"`, **not** these cells — confirmed by `DATA QUALITY` summary reporting `0 BLOCKED / 0 WARNING / 0 unmatched`. So no ENGINE output, recommendation label, validator, or gate consumes the error.

## Why it still matters

The mean-check exists to detect a **real** defect: if the 4-pass opponent adjustment ever stops centering, `|avg P3c|` drifts from ~0. With the cell permanently showing `#DIV/0!`, that signal is invisible, and an operator habituated to the error will not notice when it becomes a genuine non-zero. The guard restores the signal without changing any arithmetic.

## Exact proposed patch (NOT applied)

Behaviour-preserving when data exists; blank instead of error when it does not.

```
CALC!B39  =IF(COUNT($F$2:$F$33)=0,"",ROUND(AVERAGE($F$2:$F$33),6))
CALC!B40  =IF(COUNT($I$2:$I$33)=0,"",ROUND(AVERAGE($I$2:$I$33),6))
CALC!B41  =IF(COUNT($L$2:$L$33)=0,"",ROUND(AVERAGE($L$2:$L$33),6))
CALC!B42  =IF(COUNT($O$2:$O$33)=0,"",ROUND(AVERAGE($O$2:$O$33),6))
CALC!B43  =IF(COUNT($AC$2:$AC$33)=0,"",ROUND(AVERAGE($AC$2:$AC$33),6))

DATA QUALITY!B8  =IF(CALC!$B$42="","— (awaiting weekly stats)",ABS(CALC!$B$42))
```

`COUNT()` counts numerics only, so text-blanks are ignored exactly as `AVERAGE()` ignores them — the populated-data result is bit-identical to today's formula.

## Test coverage

`tests/run_tests.py :: DQGuardPatch` proves the guard semantics:
- empty range → blank, not `#DIV/0!`
- populated range → identical mean to `AVERAGE`
- mixed text-blank/numeric → ignores blanks
- a genuine non-zero mean is still surfaced (guard does not suppress the signal)

## Authorization required

Applying this touches formulas in the authoritative lineage, which is outside current authorization. Recommended sequencing: apply to a candidate, verify 57,399 formulas and 0 unintended diffs, then promote with the normal round-trip check.
