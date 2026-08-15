# PRESEASON_MONITOR schema

One row per team-game (32 rows for a 16-game preseason week).

| Column | Notes |
|---|---|
| PS Wk | Preseason week number |
| Game Date | ISO `YYYY-MM-DD`, one of the week's dates |
| Game Status | `COMPLETE` \| `NOT PLAYED` |
| Team / Opponent | Standard TTW team codes (matches workbook `Teams`) |
| Site | `Home` \| `Away` |
| Starter Use | `TBD` \| `STARTERS PLAYED` \| `LIMITED` \| `RESTED` \| `MIXED` |
| Player / Unit | Subject of the finding |
| Confirmed Finding | Concise interpretation; `UNVERIFIED` if unconfirmed |
| Injury / Availability | Most current verified diagnosis/availability, else `UNVERIFIED` |
| Source URL | Must be https and on the source-priority host allowlist |
| Source Date | ISO `YYYY-MM-DD` publication date |
| Evidence Type | `OFFICIAL` \| `MULTI-SOURCE` \| `BEAT REPORT` \| `GAME OBSERVATION` \| `MARKET` \| `OTHER` |
| Confidence | `HIGH` \| `MEDIUM` \| `LOW` |
| Proposed Destination | `NONE` \| `QB VALUES` \| `ADJUSTMENTS` \| `PRESEASON` |
| Proposed Change | The **field** that might change — never a numeric value |
| Decision | `PENDING` (locked) \| `MONITOR` \| `UPDATE` \| `IGNORE` |
| Workbook Updated? | `N` until the owner authorizes live-workbook changes |
| Blocker | Named blocker whenever evidence is missing |
