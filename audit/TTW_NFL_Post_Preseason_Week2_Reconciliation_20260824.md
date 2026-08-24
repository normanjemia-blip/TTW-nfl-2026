# TTW NFL — Post-Preseason Week 2 Reconciliation (2026-08-24)

**READ-ONLY RESEARCH PRODUCT + ONE APPROVED METADATA APPLICATION.** No formula, rating, QB point value,
setting, schedule, market line or model output was changed. The live Google Sheet was not accessed.

## 1. Repository, branch, HEAD, starting worktree
- Repository: `TTW-nfl-2026` (`github.com/normanjemia-blip/TTW-nfl-2026`)
- Branch: `claude/nfl-preseason-readiness-audit-unvx7i`
- Starting HEAD: `63ae04f03e703055e03edc5c01ed1da668a3a4cb`
- Starting worktree: **clean** — 0 modified, 0 untracked

## 2. Authoritative workbook
- File: `TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx`
- SHA-256 before: `ffcd5004f5886cbcb1a3b2e5115f40c90cf5a3e1ebc4d971cf3dbb7bae0ca53d`
- SHA-256 after: `4f5496e15090ddad8b63f9fa9c4a7590d3347b836fcc8b91b2bcf65c0253ff39`
- Formula count: **57,399 → 57,399**, coordinates identical, 0 formula-text diffs
- Sheets 21; `SETTINGS!B7` = **2026-07-13** (freeze date unchanged); hidden pipeline tabs untouched

## 3. Population — evidence-driven, not targeted
No authoritative "14-team" list exists; per correction, the population is **all 19 monitor rows carrying a
Blocker, plus any team whose Week 2 evidence creates a material new candidate**.

| Basis | Count |
|---|---|
| Existing Blocker rows reconciled | **19** |
| New material Week 2 candidates (DET, LAC) | **2** |
| **Total reconciled** | **21** |

Classification totals: **UPDATE 8 · RECORD CORRECTION 1 · NUMERIC REVIEW 1 · MONITOR 10 · NO CHANGE 1**

## 4. Mandatory reassessments

### Washington — UPDATE (monitor-only)
HC Dan Quinn named **Brandon Coleman** the starting left tackle after Laremy Tunsil's torn triceps required
surgery; Coleman worked with the starters. Separately, **Jayden Daniels was active and took 3 snaps** in Week 2,
his first game action since December. Blocker "replacement left tackle unconfirmed" is **RESOLVED**.
No numerical change: there is no governed mapping from an offensive-line substitution to a rating.
Source: <https://www.commanders.com/news/commanders-confident-brandon-coleman-tackle-laremy-tunsil> (2026-08-10), HIGH.

### Chicago — UPDATE (monitor-only)
**Luther Burden III**'s injury is now diagnosed as a **groin injury**; he is expected to miss the rest of the
preseason but to be **available for Week 1**. Blocker **RESOLVED**. No numerical change.
Source: <https://www.espn.com/nfl/story/_/id/49574301/sources-bears-luther-burden-iii-expected-miss-preseason> (2026-08-10), HIGH.

### Cleveland — UPDATE (workbook metadata applied)
**OFFICIAL, 2026-08-24:** the Browns named **Deshaun Watson** the 2026 starting quarterback over Shedeur Sanders,
who becomes the backup. The workbook baseline QB was already Watson, so **Active == Baseline** and the delta
stays 0. This is the same metadata-only pattern approved for Minnesota. Blocker **RESOLVED**.
Source: <https://sports.yahoo.com/nfl/live/nfl-news-injury-updates-preseason-week-2-schedule-whos-playing-starters-143714619.html> (2026-08-24), HIGH (multi-source: Yahoo, SI, ESPN).

### Minnesota — NO CHANGE (integrity verified only)
`I25 = High`, `J25` = Vikings official 2026-08-11 announcement, `K25 = 2026-08-11`, `C25 = E25 = 3.0`.
No Week 2 evidence contradicts it. Entries preserved exactly; **not reapplied, not duplicated**.

## 5. Full reconciliation table (21 teams)

| Team | Basis | Class | Prior State | Week 2 Evidence | Proposed Action | Conf | Blocker |
|---|---|---|---|---|---|---|---|
| CLE | Blocker row | UPDATE | Values blank, Confidence Low, competition explicitly unsettled | OFFICIAL 2026-08-24: Browns named Deshaun Watson the 2026 starting QB over Shedeur Sanders; Sanders is the backup. Baseline QB in workbook is already Watson, so Active == Baseline. | Confidence Low->High; replace source with the official announcement; set last-update 2026-08-24. Leave C12/E12 at 1.0. | HIGH | RESOLVED — competition officially settled |
| WAS | Blocker row | UPDATE | Blocker: replacement left tackle unconfirmed | OFFICIAL: HC Dan Quinn named Brandon Coleman the starting LT after Laremy Tunsil's torn triceps required surgery; Coleman worked with the starters. Jayden Daniels was active and took 3 snaps in Week 2, his first game action since December. | Monitor-layer only: record the named replacement LT and Daniels' return to game action. No points or rating proposed. | HIGH | RESOLVED — replacement LT now named |
| CHI | Blocker row | UPDATE | Blocker: Burden III diagnosis and timeline not reported | Luther Burden III diagnosis reported as a groin injury sustained in practice; expected to miss the remainder of the preseason but to be available for Week 1. | Monitor-layer only: record the diagnosis and expected Week 1 availability. No points or rating proposed. | HIGH | RESOLVED — diagnosis and timeline now reported |
| NYG | Blocker row | RECORD CORRECTION | Injury field attributed a carted-off Jamal Adams to New York | RECORD CORRECTION: Jamal Adams is a Minnesota Vikings player, injured during the MIN@NYG game — not a Giants player. Independently, Adams is now confirmed out for the season with a knee injury. | Remove the misattribution from the NYG monitor row. No points or rating proposed. | HIGH | RESOLVED — misattribution corrected |
| MIN | Blocker row (integrity verify only) | NO CHANGE | Confidence High, Baseline=Active=Kyler Murray, C25/E25=3.0, last-update 2026-08-11, Decision UPDATE/Y | No Week 2 evidence contradicts the Vikings' 2026-08-11 official starter announcement. Separately, Vikings S Jamal Adams is out for the season (knee) — a roster fact, not a QB-record fact. | Preserve all current MIN entries exactly. Verified intact. | HIGH | No blocker; integrity confirmed |
| PHI | Blocker row | MONITOR | Blocker: reasons for five defensive absences unreported | OLB Jonathan Greenard on PUP with a pectoral injury; DC Vic Fangio stated he does not know when Greenard will return and there is concern he could miss the start of the regular season. | Monitor-layer only: record the Greenard pec injury and Week 1 availability concern. No points or rating proposed. | HIGH | PARTIAL — Greenard explained; other absences still unreported |
| LV | Blocker row | MONITOR | Blocker: Cousins' own Week 1 snap count unverified | RB Ashton Jeanty left practice with a right knee injury and was helped off; severity not disclosed. No change to the Cousins QB1 position. | Monitor-layer only: record the Jeanty injury pending a diagnosis. QB record unchanged; approved +0.50 deviation untouched. | MEDIUM | OPEN — Jeanty diagnosis and severity not disclosed |
| HOU | Blocker row | MONITOR | Blocker: Week 1 starter participation unverified | WR Jayden Higgins (second year) tore his ACL; Xavier Hutchinson moves into the Z receiver role. | Monitor-layer only: record the Higgins ACL and the resulting depth-chart move. No points or rating proposed. | MEDIUM | PARTIAL — new injury recorded; Week 1 participation still unverified |
| NO | Blocker row | NUMERIC REVIEW | Blocker: no official statement on whether NO changed its Week 1 starter | Zach Wilson started Week 2 against the Rams after outplaying Spencer Rattler; workbook baseline QB Tyler Shough again did not start. Three different QBs have now started or led ahead of the baseline. | No governed mapping exists for a preseason-usage-driven baseline change. Leave C27/E27 unchanged; escalate for explicit ruling. | MEDIUM | OPEN — still no official NO Week 1 starter declaration |
| ATL | Blocker row | MONITOR | Blocker: post-game snap total for Tua unverified | Neither Tua Tagovailoa nor Michael Penix Jr. played in Week 2; Cooper Rush started and was relieved by Jack Strand. No official regular-season starter declaration. | Monitor-layer only: record that neither QB played and the competition remains officially undeclared. | MEDIUM | OPEN — no official ATL Week 1 declaration |
| DEN | Blocker row | UPDATE | Blocker: reason for Bo Nix hold-out not stated (rest vs precaution) | Bo Nix returned to action in Week 2 and was described as sharp, confirming the Week 1 hold-out was not injury-driven. | Monitor-layer only: record that Nix returned and the Week 1 hold-out was precautionary/planned rest. | MEDIUM | RESOLVED — hold-out reason now evident |
| PIT | Blocker row | UPDATE | Blocker: unresolved conflict on whether Rodgers took any Week 1 snaps | Aaron Rodgers was inactive for the Week 1 preseason game against Green Bay, resolving the conflict: he took no snaps. | Monitor-layer only: record that Rodgers was inactive. No points or rating proposed. | MEDIUM | RESOLVED — Rodgers confirmed inactive |
| GB | Blocker row | UPDATE | Blocker: pre-game expectation only; post-game snap confirmation unverified | Jordan Love played briefly in the Week 1 preseason game against Pittsburgh, confirming participation. | Monitor-layer only: confirm Love's participation. No points or rating proposed. | MEDIUM | RESOLVED — participation confirmed |
| ARI | Blocker row | UPDATE | Blocker: Week 1 starter participation unverified | HC Mike LaFleur said starters would play one drive, two at most, with Jacoby Brissett starting and Gardner Minshew II relieving him. | Monitor-layer only: confirm Brissett as the starter and the limited-snap plan. | MEDIUM | RESOLVED — Brissett confirmed starter |
| SF | Blocker row | UPDATE | Blocker: Week 1 starter participation unverified | Brock Purdy made his 2026 preseason debut in Week 2, taking one to two series with the first-team offense; Mac Jones followed. | Monitor-layer only: confirm Purdy's participation and usage. | MEDIUM | RESOLVED — participation confirmed |
| TB | Blocker row | MONITOR | Blocker: Browning diagnosis/timeline not specified | HC Todd Bowles planned eight to fifteen snaps for the starters in Week 2 and Baker Mayfield played. No further detail published on Jake Browning's back injury. | Monitor-layer only: record Mayfield's Week 2 usage; Browning blocker remains. | MEDIUM | OPEN — Browning diagnosis/timeline still unspecified |
| TEN | Blocker row | MONITOR | Blocker: Week 1 starter participation unverified | Cam Ward played in Week 2, described as getting a chance to settle in. Rookie WR Carnell Tate continues to see significant preseason work. | Monitor-layer only: record Ward's Week 2 participation. | MEDIUM | PARTIAL — Week 2 participation noted; Week 1 still unverified |
| IND | Blocker row | MONITOR | Blocker: Week 1 starter participation unverified | Riley Leonard started Week 2 and played the first half. Daniel Jones remains the previously announced regular-season Week 1 starter; preseason usage does not alter that. | Monitor-layer only: record Week 2 QB rotation. No change to the Jones baseline. | MEDIUM | PARTIAL — Week 1 participation still unverified |
| NE | Blocker row | MONITOR | Blocker: Week 1 starter participation unverified | New England hosted Philadelphia in Week 2 following joint practices. No qualifying source located confirming Drake Maye's participation or snap count. | No action. Blocker carried forward. | LOW | OPEN — participation still unverified |
| DET | New Week 2 candidate | MONITOR | No prior blocker; Week 1 row recorded rested starters | All-Pro LT Penei Sewell did not suit up in Week 2 and C Cade Mays sustained a wrist injury during camp. | Monitor-layer only: record the offensive-line availability items pending diagnoses. | MEDIUM | OPEN — no diagnosis or timeline published for either player |
| LAC | New Week 2 candidate | MONITOR | No prior blocker; Week 1 row recorded Herbert rested | C Tyler Biadasz was lost to injury, affecting the interior offensive line. | Monitor-layer only: record the Biadasz injury pending a diagnosis. | MEDIUM | OPEN — diagnosis and timeline not published |

## 6. Sources, dates and verification times

| Team | Source URL | Source Date | Verified At | Conf |
|---|---|---|---|---|
| CLE | https://sports.yahoo.com/nfl/live/nfl-news-injury-updates-preseason-week-2-schedule-whos-playing-starters-143714619.html | 2026-08-24 | 2026-08-24T14:04Z | HIGH |
| WAS | https://www.commanders.com/news/commanders-confident-brandon-coleman-tackle-laremy-tunsil | 2026-08-10 | 2026-08-24T14:04Z | HIGH |
| CHI | https://www.espn.com/nfl/story/_/id/49574301/sources-bears-luther-burden-iii-expected-miss-preseason | 2026-08-10 | 2026-08-24T14:04Z | HIGH |
| NYG | https://www.nbcsports.com/nfl/profootballtalk/rumor-mill/news/jamal-adams-is-out-for-the-year-with-a-knee-injury | 2026-08-16 | 2026-08-24T14:04Z | HIGH |
| MIN | https://www.nbcsports.com/nfl/profootballtalk/rumor-mill/news/jamal-adams-is-out-for-the-year-with-a-knee-injury | 2026-08-16 | 2026-08-24T14:04Z | HIGH |
| PHI | https://www.espn.com/nfl/story/_/id/49582563/eagles-olb-greenard-another-couple-weeks-pec-injury | 2026-08-21 | 2026-08-24T14:04Z | HIGH |
| LV | https://www.si.com/nfl/raiders/onsi/las-vegas-best-case-worst-after-ashton-jeanty-injury | 2026-08-24 | 2026-08-24T14:04Z | MEDIUM |
| HOU | https://www.nfl.com/news/2026-nfl-preseason-week-2-what-we-learned-saturday-games | 2026-08-23 | 2026-08-24T14:04Z | MEDIUM |
| NO | https://www.nfl.com/news/2026-nfl-preseason-week-2-what-we-learned-saturday-games | 2026-08-23 | 2026-08-24T14:04Z | MEDIUM |
| ATL | https://www.nfl.com/news/2026-nfl-preseason-week-2-what-we-learned-saturday-games | 2026-08-23 | 2026-08-24T14:04Z | MEDIUM |
| DEN | https://www.cbssports.com/nfl/news/nfl-preseason-week-2-schedule-live-scores-updates-highlights-drew-allar-will-howard/live/ | 2026-08-22 | 2026-08-24T14:04Z | MEDIUM |
| PIT | https://www.sportsbettingdime.com/news/nfl/preseason-week-2-whos-playing-starting-full-guide/ | 2026-08-13 | 2026-08-24T14:04Z | MEDIUM |
| GB | https://www.sportsbettingdime.com/news/nfl/preseason-week-2-whos-playing-starting-full-guide/ | 2026-08-13 | 2026-08-24T14:04Z | MEDIUM |
| ARI | https://www.sportsbettingdime.com/news/nfl/preseason-week-2-whos-playing-starting-full-guide/ | 2026-08-21 | 2026-08-24T14:04Z | MEDIUM |
| SF | https://www.sportsbettingdime.com/news/nfl/preseason-week-2-whos-playing-starting-full-guide/ | 2026-08-20 | 2026-08-24T14:04Z | MEDIUM |
| TB | https://www.sportsbettingdime.com/news/nfl/preseason-week-2-whos-playing-starting-full-guide/ | 2026-08-22 | 2026-08-24T14:04Z | MEDIUM |
| TEN | https://sports.yahoo.com/nfl/live/nfl-news-injury-updates-preseason-week-2-schedule-whos-playing-starters-143714619.html | 2026-08-24 | 2026-08-24T14:04Z | MEDIUM |
| IND | https://www.nfl.com/news/2026-nfl-preseason-week-2-what-we-learned-saturday-games | 2026-08-23 | 2026-08-24T14:04Z | MEDIUM |
| NE | https://www.sportsbettingdime.com/news/nfl/preseason-week-2-whos-playing-starting-full-guide/ | 2026-08-22 | 2026-08-24T14:04Z | LOW |
| DET | https://www.nfl.com/news/2026-nfl-preseason-week-2-what-we-learned-saturday-games | 2026-08-23 | 2026-08-24T14:04Z | MEDIUM |
| LAC | https://www.espn.com/nfl/story/_/id/49664649/2026-nfl-preseason-week-2-takeaways-analysis-roster-questions | 2026-08-23 | 2026-08-24T14:04Z | MEDIUM |

## 7. Exact workbook cells — current and proposed

**Only one workbook change was applied**, and it is metadata-only.

| Cell | Before | After | Type | Justification |
|---|---|---|---|---|
| `QB VALUES!I12` (CLE Confidence) | `Low` | `High` | Metadata (text) | Competition officially settled by the club on 2026-08-24 |
| `QB VALUES!J12` (CLE Source) | `Browns camp: Watson/Sanders open; Watson current frontrunner — TTW scale` | `Cleveland Browns official announcement, 2026-08-24: Deshaun Watson named starting quarterback for the 2026 season over Shedeur Sanders, who becomes the backup.` | Metadata (text) | Replaces pre-announcement camp text with the official citation |
| `QB VALUES!K12` (CLE Last update) | `2026-07-13` | `2026-08-24` | Metadata (date) | Aligns last-update to the announcement date |

**Explicitly NOT changed:** `C12 = 1.0`, `E12 = 1.0` (CLE QB points), `F12`/`G12`/`H12`/`L12`/`N12` formulas,
`C25`/`E25` (MIN), `SETTINGS!B7`, all team ratings, priors, weights, HFA, league constants, schedules,
market lines and downstream outputs.

**Expected recalculation:** `N12` (QBFlag) moves 1 → 0 because `$I12="Low"` no longer holds. `F12` stays
`1.0 − 1.0 = 0`. No model output moves.

### Justification for every numerical entry, including proposed zeros
No numerical entry is proposed anywhere in this reconciliation. **CLE `C12`/`E12` remain 1.0** — unchanged,
not re-derived — because Active QB equals Baseline QB, so the governed baseline-delta architecture yields a
delta of exactly 0 with no value edit required. **No zero was newly written**; existing zeros arise from the
`F = E − C` formula, which was not touched.

## 8. NUMERIC REVIEW item (escalated, not applied)

**New Orleans.** Zach Wilson started Week 2 after outplaying Spencer Rattler; workbook baseline QB **Tyler
Shough has still not started** in either preseason game. Three different quarterbacks have now been used ahead
of the baseline. This is materially suggestive of a baseline mismatch, **but no governed mapping exists** that
converts preseason usage into a QB value change, and New Orleans has issued **no official Week 1 starter
declaration**. Per the rule, it is classified **NUMERIC REVIEW** and `QB VALUES!C27/E27` are **left unchanged**.
Explicit approval and a documented methodology rule are required before any numerical move.

## 9. Record corrections

**New York Giants — corrected.** The Week 1 monitor attributed a carted-off **Jamal Adams** to New York.
Adams is a **Minnesota Vikings** player who was injured during the MIN@NYG game. The misattribution has been
removed from the NYG monitor row. Adams is independently confirmed **out for the season** with a knee injury.
Source: <https://www.nbcsports.com/nfl/profootballtalk/rumor-mill/news/jamal-adams-is-out-for-the-year-with-a-knee-injury> (2026-08-16), HIGH.
This is a monitor-layer text correction; no numerical or model effect.

## 10. Evidence discipline

No preseason score, final margin, or box-score line was used to justify any change. The single workbook
change rests on an official club announcement. Two stale cross-season artifacts were identified and
**rejected**: a headline placing Jacoby Brissett in a Patriots quarterback competition (Brissett is Arizona's
starter in 2026), and a Buccaneers–Dolphins result that does not match the 2026 Week 2 schedule.

## 11. Repo state vs live-Sheet state

| Layer | State |
|---|---|
| Repo (this branch) | CLE metadata applied to the local authoritative workbook; Week 1 monitor corrected; Week 2 intake created |
| **Live Google Sheet** | **NOT ACCESSED, NOT MODIFIED.** It remains at its prior state and now differs from the repo workbook by the three CLE cells plus the previously applied three MIN cells. Reconciling the live Sheet requires separate explicit authorization. |

## 12. Artifact hashes
- Authoritative workbook: `4f5496e15090ddad8b63f9fa9c4a7590d3347b836fcc8b91b2bcf65c0253ff39`
- `preseason/PRESEASON_MONITOR.csv`: `44ff52513fd57dbf46a3121078b996d586a39d5c53d5d485889febe682d3cc2f`
- `preseason/PRESEASON_WEEK2_INTAKE_20260824.csv`: `ed55d38a873e66f2d2b84d0b9c30cbc84105f9c0c661047739610a3bf681a15e`
