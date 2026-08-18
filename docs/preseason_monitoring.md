# Preseason Monitoring Workflow (repo-local)

Purpose: process preseason games into **proposals only**. Nothing here writes to a workbook or the
native Google Sheet. Ratings, wagers and recording-copy conclusions stay locked until preseason,
roster cuts, official depth charts and major injury reviews are complete.

## Artifacts
| Path | Role |
|---|---|
| `preseason/PRESEASON_MONITOR.csv` | 32 team-game intake rows for PS Wk1 (Aug 13-15) |
| `preseason/intake_template.csv` | Header-only template for later preseason weeks |
| `preseason/SCHEMA.md` | Column definitions + allowed values |
| `scripts/gen_preseason_monitor.py` | Regenerates the monitor CSV deterministically |
| `scripts/validate_preseason_monitor.py` | Schema + gate validator |
| `scripts/linkcheck_preseason.py` | Source-URL format/host check (+ best-effort reachability) |
| `scripts/run_gates.py` | Workbook invariant gates (read-only) |
| `tests/run_tests.py` | Regression suite (stdlib only) |

## Run order
```bash
python3 scripts/run_gates.py                  # workbook invariants (BET OFF, thresholds, 272 REG, ...)
python3 scripts/validate_preseason_monitor.py # monitor schema + authorization gates
python3 scripts/linkcheck_preseason.py        # source URLs
python3 tests/run_tests.py                    # full regression suite
```

## Enforced gates
- Decision/Workbook-Updated lifecycle: `PENDING`, `MONITOR` and `IGNORE` require `N`; `UPDATE` may be `N` before
  application or `Y` after a successful, owner-authorized workbook application. `PENDING`/`Y` is never permitted.
- A game with `Game Status = NOT PLAYED` must carry `Starter Use = TBD`.
- Every row needs a valid `Source URL` (host allowlist) and ISO `Source Date`.
- Any `UNVERIFIED` finding must carry a **named blocker** — never a silent gap.
- A non-`NONE` `Proposed Destination` must describe a **field**, and must not contain a point value.
- The authoritative workbook SHA-256 must not change; no new spreadsheet may be added.

## Evidence rules
Admissible: confirmed starter participation/rest, QB or position-role changes, credible injuries with
expected availability, depth-chart/roster changes, documented public-rating or market information.
**Inadmissible as team-strength evidence:** preseason scores, final margins, raw box-score production,
small-sample efficiency. Those never feed power ratings.

## Graduation
Findings are promoted only via `audit/graduation_candidates_<date>.md`, which lists team, destination,
proposed field change, evidence, confidence and approval requirement. Approval is the owner's; this
workflow never self-approves.
