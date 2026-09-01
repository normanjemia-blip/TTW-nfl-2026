# TTW NFL 2026 — Phase 3 Candidate Verification Report (2026-09-01)

**Candidate:** `TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx`
SHA-256 `8be3b9511a6fadf6d723d8ce7f0001198f1b4423bf1162c77316fda918f442cb`

**Base:** `TTW_NFL_2026_LIVE_EXPORT_20260901_BASE.xlsx` — a fresh read-only export of the live Google Sheet (`1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`, modified 2026-09-01T04:25:11Z), SHA-256 `39c7c567364234068245e68d0af943ca71e4a128b652f57cec258d40ac1e3f35`. The stale repo workbook was **not** used as the base.

**Status: CANDIDATE ONLY — STOPPED FOR OWNER REVIEW.** The live Google Sheet was not edited. The authoritative workbook is untouched (SHA `79923992…` re-verified). PR #1 remains a draft; no merge is proposed. Production is unchanged.

---

## 1. Audit narrative corrections (Phase 3 item 1)

Three corrections applied to `TTW_NFL_2026_Preseason_Prior_Audit_20260901.md`:

1. **DAL A+B+C rank corrected to 21** (was written as "~19"). Verified against the shadow CSV: DAL A+B+C prior −0.58, rank 21.
2. **DEN/HOU Week-1 rank tie recorded.** Under A+B+C, DEN prior 2.23 and HOU prior 2.22 both blend to Week-1 effective **1.78** (1.784 and 1.776 each round to 1.78 at 2 dp), so they **share rank 9** — a tie created by rounding, not by equal strength. BAL/BUF likewise share 2.71 under A+B+C. Rank comparisons at exact ties must be read as equal, not ordered.
3. **DK-July vs September comparisons relabelled as cross-book context, not movement.** The July 23 board is DraftKings; the September 1 consensus is BetMGM + Fanatics. Different books, different prices and positions — the deltas are indicative context only, and the report now says so explicitly.

---

## 2. What changed in the candidate — exactly

**352 cells written across 2 of 22 tabs; 32 formulas changed; 96 new input constants. Nothing else.**

| Sheet | Cells | Kind |
|---|---|---|
| PRESEASON | I5:I36 | **input** — Source B composite paste (32) |
| PRESEASON | K5:K36 | **input** — Source B source citation (32) |
| PRESEASON | L5:L36 | **input** — Source B as-of `2026-09-01` (32) |
| PRESEASON | J5:J36, S5:S36, T5:T36 | cached values refreshed; **formulas unchanged** (96) |
| TEAM RATINGS | D5:D36 | **formula changed** — blank-preservation fix (32) |
| TEAM RATINGS | F, H, J, K ×32 | cached values refreshed; **formulas unchanged** (128) |

Full cell-by-cell listing: `audit/TTW_NFL_2026_Candidate_Changed_Cells_20260901.csv`.

### 2.1 Source B population (item 3)

Every one of the 32 rows receives the audited **equal-weight VSiN/ESPN FPI composite** — `(Makinen p29 + ESPN FPI) / 2` — pasted at full precision into the workbook's own SrcB paste column. The workbook's existing `J` formula centres it on the entry mean and the existing `S` formula renormalizes the present weights (0.40/0.75 and 0.35/0.75). **No weight was touched:** SrcA 0.40, SrcB 0.35, SrcC 0.25 all verified unchanged in all 32 rows.

Verified: PRESEASON centered Source B and the effective A+B priors reproduce the audited shadow CSV **exactly for all 32 teams** (`preseason_srcB_centered_matches_shadow_32`, `preseason_effective_AB_prior_matches_shadow_32`).

### 2.2 The blend fix (item 4)

```
old:  IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),"")
new:  IFERROR(IF(ISNUMBER(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0))),
              ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),""),"")
```

`ISNUMBER` is a type test, so it is FALSE for a formula-blank `""`, FALSE for a truly empty cell, and FALSE (never propagating) for the `#N/A` a missing team produces. The **existing H-column fallback is preserved untouched** — `IF($D5="",$F5,…)` — so a blank D now correctly yields 100% preseason prior at GP=0, and the blend still applies normally once games exist.

**Behavioural proof** (`tests/test_blend_fix_semantics.py`, executed against a real Excel formula engine, 6/6 passing):

| Case | old D | new D | new H |
|---|---|---|---|
| GP=0, CalcGoverned returns `""` | `""` | `""` | **−1.07 = 100% prior** ✓ |
| GP>0, CalcGoverned = 1.234 | 1.23 | 1.23 | **−0.61 = 0.8×prior + 0.2×1.23** ✓ (blend intact) |
| CalcGoverned truly empty | **0.0 ← defect** | `""` | **−1.07 = 100% prior** ✓ |
| team missing from lookup (`#N/A`) | `""` | `""` | −1.07 ✓ |
| no governed rating **and** no prior | `""` | `""` | `""` ✓ (no fake zero) |

**Honest scope limit on this proof.** The defect is engine-dependent. The engine used here reproduces it on the *truly empty* cell; the live platform (Google Sheets) reproduces it on the *formula-blank* cell — that is directly evidenced by Google's own cached value of `0` for D5:D36 in the base export while `CALC!AD` is blank. The fix closes **both** coercion paths, and is proven for all four cases under Excel semantics. **It has not been executed inside Google Sheets** (writing to the live Sheet is out of scope), so the owner should confirm in Sheets on a duplicate before promotion — expected result: TEAM RATINGS D shows blank and EFFECTIVE RATING equals the preseason prior for all 32 teams at GP=0.

### 2.3 What was deliberately **not** changed

- **Source C** stays entirely unpopulated (`srcC_still_empty` — all 32 rows blank) and **WinTotalsMode remains VALIDATE-ONLY** (item 5).
- No manual team override, no QB change, no weight change, no threshold change. Verified cell-for-cell across MARKET LINES, QB VALUES, ADJUSTMENTS, SETTINGS, and the live-only PRESEASON MONITOR tab.
- Week-1 blend weight remains **0.80** in SETTINGS and in TEAM RATINGS!G — the fix changes *whether* the in-season term exists, not the schedule.
- **Version banner and CHANGELOG were left untouched** (the candidate still reads v1.1). Editing them was not among the authorized changes, and "prove only intended cells changed" is stronger with them left alone. Version labelling is an owner decision at promotion.
- `sharedStrings.xml`, `styles.xml`, `workbook.xml`, all 22 drawings and `persons/person.xml` are **byte-identical** to the base.

---

## 3. Proof that only intended cells changed

`scripts/verify_srcb_blendfix_candidate.py` — **37 checks, 0 failed**:

- `zip_members_identical_set_and_order` (74 members, same order)
- `only_two_worksheet_parts_changed` → exactly `sheet17.xml` (PRESEASON) and `sheet8.xml` (TEAM RATINGS)
- `drawings_persons_byte_identical` (23 parts), `unchanged_sharedStrings.xml`, `unchanged_styles.xml`, `unchanged_workbook.xml`
- `formula_count_57399` — unchanged; `formula_coordinates_identical` — no formula added or removed
- `only_D5_D36_formulas_changed` — 32 changed, and no others anywhere in the workbook
- `D_column_fix_text_exact` — all 32 match the intended text character-for-character
- `only_srcB_input_constants_added` — the 96 new constants are exactly PRESEASON I/K/L rows 5–36; no other constant anywhere changed
- `preserved_market_lines`, `preserved_qb_values`, `preserved_adjustments`, `preserved_settings`, `preserved_preseason_monitor`
- `srcA_raw_unchanged`, `weights_unchanged_A040_B035_C025`, `srcC_still_empty`, `win_totals_mode_validate_only`, `blend_wt_wk1_still_080`, `all_GP_zero`

**Cached-value policy.** Cached values were refreshed for the edited cells and their same-sheet dependents (PRESEASON I/J/K/L/S/T, TEAM RATINGS D/F/H/J/K). Downstream sheets — ENGINE, DASHBOARD, DATA QUALITY — still carry the base's cached numbers and are left to recalculate on open: the workbook carries `<calcPr/>` with no `calcId`, so Excel full-recalculates on load and Google Sheets recalculates on import. The expected recalculated values are published in §4 and in the slate CSV, computed independently from the workbook's own ENGINE formula semantics. This is the same convention used by every earlier candidate in this repo.

---

## 4. Regenerated Week-1 slate (all 16 games)

Full table: `audit/TTW_NFL_2026_Candidate_Week1_Slate_20260901.csv`. Every market line is the candidate's own preserved Novig entry; ratings are the candidate's effective ratings; HFA/QBadj/Rest/Manual are the workbook's own unchanged values.

| Game | Fair line | Market | Edge | Side | Δ vs base |
|---|---|---|---|---|---|
| NE @ SEA | SEA −4.0 | −3.5 | +0.51 | SEA −3.5 | +0.40 |
| SF @ LA (N) | LA −2.7 | −3.5 | −0.82 | SF +3.5 | +0.37 |
| CHI @ CAR | CHI −1.7 | +2.5 | +0.80 | CAR +2.5 | −1.14 |
| TB @ CIN | CIN −1.6 | −3.5 | −1.95 | TB +3.5 | +1.00 |
| NO @ DET | DET −4.9 | −6.5 | −1.62 | NO +6.5 | +1.48 |
| BUF @ HOU | HOU −0.7 | +1.5 | +2.23 | HOU +1.5 | −1.83 |
| BAL @ IND | BAL −0.6 | +3.5 | +2.86 | IND +3.5 | −2.14 |
| CLE @ JAX | JAX −7.8 | −7.5 | +0.30 | JAX −7.5 | +0.38 |
| ATL @ PIT | PIT −2.7 | −3.5 | −0.78 | ATL +3.5 | +0.40 |
| NYJ @ TEN | TEN −3.2 | −2.5 | +0.74 | TEN −2.5 | +0.11 |
| ARI @ LAC | LAC −6.9 | −10.5 | **−3.58** | ARI +10.5 | +2.69 |
| MIA @ LV | LV −2.1 | −3.5 | −1.41 | MIA +3.5 | +0.87 |
| GB @ MIN | PK | −1.5 | −1.46 | GB +1.5 | −1.55 |
| WAS @ PHI | PHI −5.7 | −5.0 | +0.69 | PHI −5.0 | +0.57 |
| **DAL @ NYG** | **NYG −0.8** | **+2.5** | **+3.27** | **NYG +2.5** | −1.50 |
| DEN @ KC | KC −0.3 | −2.5 | −2.20 | DEN +2.5 | +0.67 |

Only two edges remain ≥3.0 (ARI +10.5 and NYG +2.5, down from five in the base). Two sides flip versus the base — CLE@JAX and GB@MIN — both from near-zero base edges (−0.08 and +0.09), i.e. noise-level flips, not reversals of a signal.

### Required pins — all verified in the candidate file

| Pin | Required | Candidate | ✓ |
|---|---|---|---|
| DAL prior | −1.07 | −1.07 | ✓ |
| NYG prior | −1.90 | −1.90 | ✓ |
| DAL rank | 22 | 22 | ✓ |
| NYG rank | 24 | 24 | ✓ |
| GP=0 effective = prior | yes (all 32) | yes (all 32) | ✓ |
| DAL@NYG FinalMargin | +0.77 NYG | +0.77 | ✓ |
| Fair line | NYG −0.8 | `NYG -0.8` | ✓ |
| Edge vs DAL −2.5 | +3.27 NYG | +3.27, side NYG +2.5 | ✓ |

### League-wide effect

27 of 32 ranks move; mean absolute rating change 0.84 pts, max 2.09 (ARI). Largest gains BAL +1.54, BUF +1.42, LA +1.27, **DAL +1.19**; largest declines ARI −2.09, MIA −1.85, CLE −1.20, ATL −1.00. Two effects are superimposed by design: Source B re-weighting, and the removal of the uniform 20% Week-1 compression.

---

## 5. Test results

| Suite | Result |
|---|---|
| `scripts/run_gates.py` | **PASS** (21 sheets, 57,399 formulas, BET OFF, thresholds 3.0/1.5/1.0, VALIDATE-ONLY, 272 REG) |
| `scripts/validate_preseason_monitor.py` | **PASS** (32 rows, 16 blockers) |
| `scripts/linkcheck_preseason.py` | **PASS** (32 rows, 16 URLs, all allowlisted) |
| `scripts/verify_srcb_blendfix_candidate.py` | **PASS — 37 checks, 0 failed** |
| `tests/run_tests.py` | **40/40 OK** (28 pre-existing + 6 candidate + 6 blend-fix semantics) |
| `git diff --check` | clean |

The gate suite still reports "PRESEASON SrcB blank" because it audits the **authoritative** workbook, which is untouched — that is the correct and expected result while the candidate remains unpromoted.

The candidate rebuilds **byte-identically** from the committed base export (`test_candidate_rebuilds_byte_identically`), so any reviewer can reproduce it exactly.

---

## 6. PR #1 scope resolution

PR #1 stays **draft**; no merge is proposed. Its "99 files changed" is fully explained and is not scope creep:

- `origin/main` contains **exactly one file** — the original uploaded `TTW_NFL_v1_1_1 Version 2.xlsx`. It has never received any project work.
- The branch carries **15 commits** spanning the entire project (baseline audit → v1.1 promotion → QB activation → market lines → monitoring workflow → reconciliations → the 2026-09-01 audit → this candidate).
- The diff is **9,206 insertions and 0 deletions**: nothing on `main` is modified or removed. The count reflects a repository being populated for the first time, not a large change to existing work.

Three options for the owner, in the order I would recommend them:

1. **Leave it draft and keep working on the branch** (status quo). Nothing depends on merging; every artifact is already reachable on the branch.
2. **Merge once to establish `main` as the trunk.** Safe on the evidence — 0 deletions, and the authoritative workbook SHA is unchanged from the promoted v1.1. Do this only after the Sheets-side confirmation in §7.
3. Split into thematic PRs — possible but low value: the history is linear and sequential, so a split would mostly re-order the same commits.

**Recommendation: option 1 until the owner has reviewed this candidate**, then option 2 if `main` should become the trunk.

---

## 7. Owner review checklist (nothing here has been done)

1. Open the candidate and confirm in **Google Sheets** that TEAM RATINGS D5:D36 renders blank and EFFECTIVE RATING equals the preseason prior for all 32 teams (§2.2 — the one claim not executable in this environment).
2. Confirm the Source B composite is the intended blend, and that the VSiN half may be used this way given the guide's subscriber terms (the numeric table only is used; the PDF is not committed).
3. Decide the version label and CHANGELOG entry (deliberately left untouched).
4. Decide whether the Week-1 blend fix ships together with Source B or separately — they are independent changes and the slate CSV separates their contributions.
5. Source C remains VALIDATE-ONLY pending the 2.1 pts/win calibration test recommended in the audit report §8.
