# TTW NFL 2026 — Preseason Prior Audit & Shadow Reconstruction (2026-09-01)

**Scope:** Phase 1 (read-only baseline verification & source audit) and Phase 2 (shadow calculations & candidate outputs) only.
**Production impact: NONE.** The authoritative workbook was not modified. The live Google Sheet was inspected **read-only** (explicitly authorized for this task) and **was not written to**. No source weight, blend weight, rating, or setting was changed anywhere. Everything below is shadow analysis.

Companion artifacts (all in this repo):

| Artifact | Purpose |
|---|---|
| `audit/TTW_NFL_2026_Preseason_Prior_Provenance_20260901.json` | Machine-readable source values + provenance (single input to the generator) |
| `audit/TTW_NFL_2026_Preseason_Prior_Shadow_20260901.csv` | 32-team shadow ratings/ranks under every scenario + outlier flags |
| `audit/TTW_NFL_2026_Week1_Before_After_Shadow_20260901.csv` | All 16 Week-1 games recomputed under every scenario |
| `scripts/gen_preseason_prior_shadow.py` | Deterministic generator; reproduces both CSVs byte-identically |

---

## 1. Baseline verification (Phase 1)

### 1.1 Fresh read-only live export obtained — staleness stop-condition cleared

The repo workbook (`TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx`, SHA-256 `79923992e9cfe156af47207b1756010af9a375592997be8e194bc75e4e9d313f`) carries as-of **2026-07-13** and no Week-1 market lines — it does **not** match the stated live baseline on its own. Per the task's authorization, a fresh **read-only** export of the live Sheet (`1RXJkgGgnaWKPiNT3DVEvAOQRRaUftzkjpVg35ih9Iew`, last modified 2026-09-01T04:25:11Z) was taken at 2026-09-01T09:56Z. The audit therefore proceeds against **live values + repo formulas** (the repo workbook's formula layer is the frozen v1.1 layer the live Sheet runs; every derived live value below reproduced from repo formulas exactly).

Repo-vs-live divergences (all user-entered inputs or metadata; **zero formula divergences observed**):

| Item | Repo workbook | Live Sheet (2026-09-01) |
|---|---|---|
| SETTINGS as-of | 2026-07-13 | **2026-09-01** |
| ATS BET threshold / BET labels | 3.0 / N | **1.5 / Y** (CHANGELOG 1.1-W1: explicit user operating-policy change) |
| Week-1 market lines | 0 entered | **16 Novig spreads**, line date 2026-08-31, OddsLogic snapshot 2026-09-01 00:17–00:19 ET (0 spreads missing, 16 totals missing by design) |
| QB VALUES | zero-init C/E convention (+ MIN 3.0 / CLE 1.0 / NO 2.5) | Full 32-team **absolute-scale** restatement, all sources rechecked 2026-09-01; **only nonzero delta remains LV +0.50**. Model-identical: C/E feed nothing; only delta F feeds ENGINE |
| CHANGELOG | through NO metadata update | adds **1.1-W1** (2026-09-01) Week-1 promotion entry |
| Tabs | 21 | 22 (adds PRESEASON MONITOR — NON-FEEDING REVIEW QUEUE) |

### 1.2 Task-stated baseline figures — all verified

Settings verified in the live export: season 2026, week 1, as-of 2026-09-01, HFA 1.6 (neutral 0), ATS INVESTIGATE 1.5, prior regression 0.33, source weights A 0.40 / B 0.35 / C 0.25, 2.1 pts/win, win-totals mode VALIDATE-ONLY, Week-1 preseason blend weight 0.80, GP=0 for all 32 teams, SrcB and SrcC blank for all 32 teams. **PRESEASON SrcA raw and regressed values are identical between repo and live for all 32 teams** (programmatic diff, zero mismatches).

DAL / NYG chain, verified value-by-value (live export) and formula-by-formula (repo):

| Step | DAL | NYG | Formula (repo) |
|---|---|---|---|
| SrcA raw | -4.21 | -2.97 | PRESEASON!D (static, TTW 2025 wk1-18 final, as-of 2026-01-05) |
| Regressed | -2.82 | -1.99 | `ROUND(D*(1-0.33),2)` |
| Wk-1 effective | -2.26 | -1.59 | `ROUND(0.8*prior + 0.2*0, 2)` (§3) |
| Rank | 27 | 24 | `RANK(J,J$5:J$36,0)` |

Engine bridge for 2026_01_DAL_NYG (live ENGINE row 15): NeutralDiff = -1.59 − (-2.26) = **+0.67 NYG**; + HFA 1.6 → FinalMargin **+2.27** → model spread **NYG -2.3**; market **NYG +2.5** (Novig DAL -2.5); SpreadEdge = 2.27 + 2.5 = **+4.77 on NYG**, label INVESTIGATE. All figures match the task's stated baseline exactly. Working position confirmed (§7): this is a **prior-construction warning, not a valid 4.77-point betting edge**.

---

## 2. Source audit (Phase 1)

### 2.1 Source B-1 — VSiN / Steve Makinen power ratings (page 29)

- **Provenance:** user-supplied private PDF `2026-VSiN-NFL-Betting-Guide-UPDATE.pdf` (Drive file `19lMuQAbYPL_AhQZZC4inC-pEZ-kYfXsN`, 6,429,473 bytes, uploaded to the user's Drive 2026-09-01). This is the **post-preseason "Guide 2.0" update** ("The preseason is in the books…"), i.e. current as of late August 2026.
- **Confidentiality honored:** the PDF is **not committed** to the repository; team writeups are not reproduced; only the numeric page-29 ratings table (facts, not expression) was extracted into the provenance JSON.
- **Validation:** 32 teams, sum 768.0, **league mean exactly 24.0** as expected. DAL **24.0** (centered 0.0) and NYG **22.0** (centered -2.0) — the task's expected values, independently verified from the PDF text layer.
- **Opinion/ratings separation:** the guide's Week-1 betting plays — including **"NY GIANTS +2.5 (-105) VS. DALLAS"** — come from Makinen's *Week-1 betting-systems* article (angle-based), not from the power ratings, and were kept out of the ratings layer entirely. They are noted only as market-context corroboration in §7.

### 2.2 Source B-2 — ESPN FPI (numeric, no ordinal conversion)

- **Provenance:** https://www.espn.com/nfl/fpi renders client-side; numeric values retrieved from ESPN's own data API for that page (`site.web.api.espn.com/apis/fitt/v3/sports/football/nfl/powerindex`), **ESPN lastUpdated 2026-08-31T14:44Z**, retrieved 2026-09-01. All 32 numeric FPI values captured to 3 decimals with ESPN's own FPI ranks; no gap-filling, no ordinal conversion.
- **Centering check:** raw mean +0.044 (ESPN publishes approximately-centered values); the workbook's SrcB formula centers on the entry mean, which removes this drift exactly.
- Headline: FPI has **LA #1 (+5.85)**, and **DAL #11 (+1.88)** vs TTW rank 27 — the single largest public-vs-TTW divergence in the league (§6).

### 2.3 Source C — market win totals (all 32, with prices)

Two same-day (2026-09-01) boards were captured; consensus = mean of the two. A stale 2026-07-23 board is retained **only** for line-movement context and is excluded from consensus.

- **BetMGM** (2026-09-01, with over/under prices) — primary.
- **Fanatics** (2026-09-01, lines only).
- **DraftKings via FOX Sports** (updated 2026-07-23, with prices) — movement reference only.

**Conflicts (reported, not silently resolved)** — six teams differ by exactly 1.0 game between the two same-day books: ARI (3.5 MGM / 4.5 FAN), DAL (9.5 / 8.5), GB (9.5 / 10.5), JAX (9.5 / 8.5), LAC (10.5 / 9.5), NE (10.5 / 9.5). Consensus takes the mid-point and the conflict is flagged per-row in the shadow CSV. Prices are recorded per book in the provenance JSON (note DAL -110/-110 at MGM: a genuinely two-sided 9.5).

Movement since late July (DK Jul-23 → Sep-01 consensus): ATL +1.0, ARI +0.5, SF +1.0, LAC +0.5, JAX +0.5, GB +0.5, NE −0.5, CIN −1.0, DAL −0.5. Direction is coherent with August news flow and matters for §8.

### 2.4 Week-1 market spreads (post-hoc reference only — never inputs)

The 16 Novig spreads were taken from the live Sheet's own MARKET LINES tab (line date 2026-08-31, OddsLogic snapshot 2026-09-01 00:17–00:19 ET). They are used exclusively to compute edges *after* each shadow model is built. No market spread feeds any rating in any scenario.

---

## 3. Week-1 blend audit (W1-A vs W1-B)

**Mechanism (traced in the repo formula layer, which is the live layer):**

- `TEAM RATINGS!H5` (Blended base): `=IF(AND($D5="",$F5=""),"",IF($D5="",$F5,ROUND($G5*IF($F5="",0,$F5)+(1-$G5)*$D5,2)))`
- `TEAM RATINGS!D5` (In-season governed): `=IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),"")`
- `CALC!AD` (CalcGoverned) is **blank** at GP=0: the whole P0→P3c chain starts with `=IF($D2=0,"",…)` and every downstream step propagates the blank. Verified in the repo's cached values: CALC!AD2 is empty while TEAM RATINGS!D5 caches **numeric 0**.

**Finding:** the blend formula *contains its own designed fallback* — `IF($D5="", $F5, …)` = **use 100% prior when there is no in-season rating**. That branch is unreachable: `INDEX()` over an *empty* cell returns numeric 0, not "", so D5 is always 0 at GP=0 and Week 1 computes `0.8×prior + 0.2×0` — a uniform 20% compression of every rating toward zero.

**Intent evidence (documentation review):** the DICTIONARY documents only the *reverse* asymmetry — "Preseason blend | Week-indexed weight (80% wk1 → 10% wk8+)… **No prior → 100% in-season** + LOW SAMPLE flags do the warning." Nowhere does any documentation state that Week-1 ratings are deliberately shrunk 20% toward the league mean; yet the formula's dead branch shows the author *did* intend a no-in-season→100%-prior path. **Assessment: defect-like (an unreachable intended fallback), not a documented design choice.** Mitigating context: the compression is uniform, so ranks are unchanged and every neutral-field margin is scaled by exactly 0.8 — it shrinks Week-1 edge magnitudes symmetrically rather than distorting any single team.

**Scenarios:** W1-A = current production (0.8 blend against zero); W1-B = GP=0 renormalization to 100% prior. Both are carried through every shadow model in the CSVs. Under W1-B, neutral diffs scale ×1.25; five teams move ≥0.8 pts in absolute rating (JAX, LA, LV, NYJ, SEA — the largest-magnitude priors). Only 3 of 16 games change edge by >0.9, and no INVESTIGATE-tier conclusion flips on W1-B alone.

**No fix is implemented.** Candidate remediation (owner decision, out of scope): either make `CalcGoverned` return "" through the INDEX (e.g. `IF(INDEX(...)="","",...)` guard in TEAM RATINGS!D) so the existing fallback fires, or document the 20% Week-1 shrinkage as intentional conservatism and re-derive the blend schedule accordingly.

---

## 4. Shadow models (Phase 2)

All arithmetic replicates workbook formulas exactly (Excel half-away-from-zero rounding; SrcB centered on entry mean; SrcC implied = (win total − entry mean) × 2.1; effective prior = weight-renormalized average — A+B weights renormalize to 0.40/0.75 = 53.333% and 0.35/0.75 = 46.667%). Centering validated at every pass (|Σ| ≤ 0.16, pure 2-dp rounding residue).

| # | Model | Composition | Wk-1 treatment |
|---|---|---|---|
| 1 | Current production | A only (regressed prior) | W1-A and W1-B |
| 2 | A+B renormalized | 53.333% A + 46.667% B | W1-A and W1-B |
| 3 | A+B+C shadow | 0.40 A + 0.35 B + 0.25 C | W1-A (VALIDATE-ONLY stays production default) |
| 4 | A+B, GP=0 renorm | model 2 under W1-B | W1-B |

Source-B variants computed for models 2–3: **VSiN-only**, **FPI-only**, and **combined (VSiN+FPI)/2**. (Centering is linear, so averaging raws then centering ≡ averaging the centered values.)

Headline shadow ratings (combined-B, effective prior, vs current):

- **Biggest upgrades:** DAL −2.82 → **−1.07** (A+B) → **−0.58** (A+B+C); ARI −2.59 → −4.16 (downgrade — see below); CIN −1.91 → −0.60 → +0.04; KC −0.05 → +1.02 → +1.79; GB +0.64 → +1.55 → +1.92; BUF +2.19 → +3.17 → +3.39; BAL +1.15 → +2.46 → +3.39.
- **Biggest downgrades:** JAX +4.03 → **+2.40** → +2.03; HOU +3.39 → +2.30 → +2.22; ARI −2.59 → **−4.16** → −5.52; MIA −3.30 → −4.49 → −5.50; IND +1.02 → +0.22 → −0.39; PIT +0.82 → +0.06 → +0.02; MIN +0.62 → −0.01 → −0.04.
- **Essentially unmoved:** NYG (−1.99 → −1.90 → −1.98), LV (−4.40 → −4.50 → −4.98), TEN, CAR, TB, NO (mild), SEA/LA stay 1–2.

---

## 5. Week-1 games — before/after (all 16, every scenario)

Full table in `TTW_NFL_2026_Week1_Before_After_Shadow_20260901.csv`. Summary:

- **Edges ≥3.0 under current production (W1-A):** BAL@IND +5.0 (IND), DAL@NYG +4.77 (NYG), BUF@HOU +4.06 (HOU), ARI@LAC −6.27 (ARI), NO@DET −3.10 (NO). TB@CIN −2.95 and DEN@KC −2.87 sit just under.
- **Under A+B combined (W1-A)** every one of those edges shrinks: IND +3.31, NYG +3.44, HOU +2.40, ARI −4.64, NO −2.28, TB −1.94, DEN −1.94. **Under A+B+C** they shrink further (IND +2.08, NYG +2.98, ARI −3.18). Pattern: the market agrees with the public sources far more than with the TTW-2025-only prior — large "edges" are mostly prior-construction artifacts.
- **Side flips vs current** (any scenario): NE@SEA, CLE@JAX, GB@MIN, WAS@PHI — all games whose current edge is ≤0.12, i.e. noise-level flips only. **No INVESTIGATE-tier side ever flips.**
- **Survivors:** ARI@LAC (ARI +10.5) keeps ≥3.0 in every A+B scenario — and VSiN's own systems article independently plays ARI +10.5. DAL@NYG stays ≥3.0 through A+B but drops to +2.98 with Source C in.

---

## 6. Outlier flags (definitions in generator; per-row flags in shadow CSV)

- **TTW-vs-FPI ≥2.5 pts** (|Wk-1 effective − FPI centered|): ARI, CIN, CLE, DAL, KC, MIA.
- **Rank gap ≥8** (TTW rank vs FPI rank): CIN, DAL, DEN, GB, HOU, JAX, KC, LAC, NE.
- **Movement ≥1.5** (|A+B prior − current prior|): ARI, DAL, JAX.
- **Source-C direction-dependent** (C pulls ≥0.5 against B's direction): **none** — win totals corroborate the public ratings' direction for every team, which materially strengthens the B-side evidence.
- **GP=0-dependent ≥0.8** (|W1-B − W1-A|): JAX, LA, LV, NYJ, SEA.
- **Win-total book conflict:** ARI, DAL, GB, JAX, LAC, NE.

---

## 7. Priority teams & DAL/NYG deep dive

**Likely-underrated list (task):** confirmed for **DAL** (rank 27 → 22 A+B → ~19 A+B+C; largest league-wide gap: FPI #11, Makinen exactly league-average, win total 9.0–9.5), **CIN** (23 → 20 → ~12-equivalent by FPI; Makinen 24.0 = average vs TTW −1.91), **KC** (18 → 15; FPI #9, win total 10.5 — but note live QB VALUES holds KC confidence **Low**, so the QB layer already carries caution), **GB** (16 → 12; FPI #7, total 10.0), **BUF** (8 → 3; all sources top-4), **WAS** (mildly: −2.53 → −1.92). **Not supported for LV:** every source agrees with TTW (prior −4.40 vs public −4.61 combined, total 5.5); LV is *not* underrated by this evidence.
**Likely-overrated list (task):** confirmed for **JAX** (+4.03 vs public +0.5–1.1; FPI #16; nonetheless still favored −7.4 vs CLE and market agrees at −7.5), **HOU** (+3.39 vs public ~+1.1), **IND**, **PIT**, **MIN** (all cross zero under A+B+C), **ATL** (mild), **NO** (mild: −1.17 → −1.64; the QB layer, not the prior, is where NO's uncertainty was already resolved).

**DAL@NYG:** the +4.77 NYG edge decomposes as ≈1.33 pts of DAL-underrating by SrcA (edge falls to +3.44 under A+B) plus ≈0.46 more with Source C (+2.98), leaving ≈3 pts that is genuine model-vs-market disagreement about this matchup (even public-source-blended TTW still makes NYG about −0.4 to −1.0 at home while the market has DAL −2.5). Conclusion — the baseline working position is **confirmed and sharpened**: at least ~40% of the displayed edge is prior-construction artifact; what remains is an ordinary-sized disagreement, not a 4.77-point outlier. Market context (separate opinion layer, not evidence): VSiN's Week-1 systems article independently plays NY GIANTS +2.5 (-105); the guide's NFC preview also leaned Giants win-total Over. These are betting opinions and were given zero weight in any rating.

**Team-specific reconciliation / post-source-date developments:** every source in this audit is dated 2026-08-31 or 2026-09-01, and the live Sheet's own QB layer was re-verified league-wide on 2026-09-01 (all starters rechecked; only nonzero delta LV +0.50; ATL and KC deliberately held at Low confidence). No development post-dating the sources was identified that would justify a manual prior-layer proposal, and **no ≥1.0-pt manual correction is proposed for any team** — the observed gaps are systematic (source-composition) rather than team-specific, and the correct remedy is source population, not manual edits. QB-driven considerations remain in the QB layer; FPI already includes QB effects, so no FPI-derived value was double-counted into any QB or adjustment proposal.

---

## 8. Source-C evaluation (the four questions)

1. **Does the 2.1 pts/win conversion produce sane magnitudes?** Yes at the extremes' *order* (spread: LA/BAL +6.17 to ARI −9.58) but the tails are hotter than both B sources (ARI −9.58 vs −5.4/−6.5; MIA −8.53 vs −5.5/−6.2). 2.1 linearly applied to win totals overweights the tails; a fitted conversion on 2025 (totals vs final ratings) is the right calibration test before ever flipping BLEND.
2. **Does C corroborate B?** Strongly: zero direction conflicts (§6); rank correlation with combined-B is near-perfect at the top and bottom.
3. **Is consensus quality adequate?** Adequate with caveats: two current books disagree by a full game on six teams (ARI, DAL, GB, JAX, LAC, NE), and prices matter (DAL 9.5 at −110/−110 vs Fanatics 8.5 implies true ~9.0). Consensus-of-two is thin; add a third live book before promotion.
4. **Should VALIDATE-ONLY flip to BLEND?** **No — keep VALIDATE-ONLY** (production default unchanged). C adds no directional information beyond B, has hotter tails under the unverified 2.1 conversion, and its book-level disagreement is largest on exactly the teams already flagged. Revisit only after the 2.1 calibration test.

---

## 9. Recommendations (candidate-only; nothing implemented)

1. **Populate SrcB in production** with combined (VSiN+FPI)/2 — this is the workbook's designed mechanism for exactly this problem, needs no formula change, and moves every flagged team toward every independent source. (Owner action in the live Sheet; a repo candidate can be built on request.)
2. **Decide the GP=0 blend question explicitly** (§3): fix the unreachable fallback or document the 20% Week-1 shrinkage as intended. Either is defensible; silence is not.
3. **Keep Source C VALIDATE-ONLY** pending a 2025-calibrated pts/win test (§8).
4. **No isolated manual team corrections** — expressly out of scope and also unsupported by the evidence (§7).
5. Optional SHADOW workbook: **not built.** The task lists it as optional; both CSVs plus the generator carry every number a SHADOW workbook would, with zero risk of a shadow file being mistaken for the authoritative one. Can be produced with the established surgical-copy tooling on request.

## 10. Validations & limitations

- Generator asserts: 32 teams everywhere; VSiN mean exactly 24.0; all centered sets sum to rounding residue only; DAL/NYG production chain reproduced to the cent (−2.82/−1.99, −2.26/−1.59, FinalMargin +2.27, edge +4.77). Both CSVs regenerate byte-identically from the provenance JSON (tested in `tests/run_tests.py`).
- Repo four-suite status at commit time is recorded in the commit/PR notes; the authoritative workbook SHA is unchanged.
- Limitations: (a) win-total consensus rests on two books; (b) BetMGM/Fanatics/FOX tables were extracted via summarizing fetches — spot-corroborated across three independent boards but not screenshot-verified; (c) the live export is a values snapshot — formulas were verified from the repo layer, not re-read from Google; (d) FPI is a full model including QB/injury priors, so blending it imports ESPN's opinions wholesale — acceptable for Source B by design, but the reason no FPI-derived team-specific proposals are made on top of it.
