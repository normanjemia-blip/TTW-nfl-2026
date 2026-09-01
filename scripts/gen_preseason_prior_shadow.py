#!/usr/bin/env python3
"""Generate the 2026-09-01 preseason-prior SHADOW artifacts (byte-identical, deterministic).

Reads  audit/TTW_NFL_2026_Preseason_Prior_Provenance_20260901.json
Writes audit/TTW_NFL_2026_Preseason_Prior_Shadow_20260901.csv
       audit/TTW_NFL_2026_Week1_Before_After_Shadow_20260901.csv

SHADOW ONLY — nothing here writes to the authoritative workbook or the live Sheet.
All arithmetic replicates the workbook's own formulas:
  SrcB centered      = ROUND(paste - AVERAGE(paste), 2)                    (PRESEASON!J)
  SrcC implied pts   = ROUND((wintotal - AVERAGE(wintotal)) * 2.1, 2)      (PRESEASON!O)
  Effective prior    = ROUND(weight-renormalized average of present srcs, 2)  (PRESEASON!S)
  Wk1 blended (W1-A) = ROUND(0.8*prior + 0.2*0, 2)                         (TEAM RATINGS!H, current production)
  Wk1 blended (W1-B) = prior (GP=0 renormalized to 100% prior — shadow scenario)
  FinalMargin        = (HomeEff - AwayEff) + HFA + QBadjHome               (ENGINE bridge; HFA 1.6, 0 neutral)
  SpreadEdge         = FinalMargin + MarketHomeSpread                      (positive = value on HOME)
ROUND is Excel-style half-away-from-zero (decimal.ROUND_HALF_UP).
"""
import csv, json, os
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROV = os.path.join(ROOT, "audit", "TTW_NFL_2026_Preseason_Prior_Provenance_20260901.json")
OUT_SHADOW = os.path.join(ROOT, "audit", "TTW_NFL_2026_Preseason_Prior_Shadow_20260901.csv")
OUT_WK1 = os.path.join(ROOT, "audit", "TTW_NFL_2026_Week1_Before_After_Shadow_20260901.csv")


def xround(x, nd=2):
    """Excel ROUND: half away from zero."""
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def centered(vals):
    """PRESEASON!J semantics: ROUND(v - mean(entered), 2) per team."""
    m = sum(vals.values()) / len(vals)
    return {t: xround(v - m) for t, v in vals.items()}


def fmt(x):
    """Trim trailing zeros so 2.50 -> 2.5, -0.00 -> 0."""
    if x is None:
        return ""
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def rank_map(ratings):
    """RANK(...,0) semantics: descending, ties share the top position."""
    return {t: 1 + sum(1 for u in ratings.values() if u > ratings[t]) for t in ratings}


def main():
    prov = json.load(open(PROV))
    srcA_raw = {t: v[0] for t, v in prov["source_A"]["values_raw"].items()}
    srcA_reg = {t: xround(v * (1 - 0.33)) for t, v in srcA_raw.items()}
    teams = sorted(srcA_raw)

    vsin = prov["source_B_vsin"]["values"]
    fpi = prov["source_B_fpi"]["values"]
    comb = {t: (vsin[t] + fpi[t]) / 2 for t in teams}
    vsin_c, fpi_c, comb_c = centered(vsin), centered(fpi), centered(comb)

    books = prov["source_C_win_totals"]["books"]
    mgm, fan = books["betmgm"]["totals"], books["fanatics"]["totals"]
    cons = {t: (mgm[t] + fan[t]) / 2 for t in teams}
    mwt = sum(cons.values()) / 32
    implied = {t: xround((cons[t] - mwt) * 2.1) for t in teams}

    def eff_AB(bc):
        return {t: xround((0.4 * srcA_reg[t] + 0.35 * bc[t]) / 0.75) for t in teams}

    def eff_ABC(bc):
        return {t: xround(0.4 * srcA_reg[t] + 0.35 * bc[t] + 0.25 * implied[t]) for t in teams}

    S = {
        "current": dict(srcA_reg),
        "AB_vsin": eff_AB(vsin_c),
        "AB_fpi": eff_AB(fpi_c),
        "AB_comb": eff_AB(comb_c),
        "ABC_comb": eff_ABC(comb_c),
    }
    W1A = {k: {t: xround(0.8 * v[t]) for t in teams} for k, v in S.items()}
    W1B = {k: dict(v) for k, v in S.items()}  # GP=0 renorm: 100% prior
    ranks = {k: rank_map(W1A[k]) for k in S}  # rank order identical under W1A/W1B (monotone scale)
    fpi_rank = rank_map(fpi)

    # ---- team-level shadow CSV ----
    hdr = ["Team", "SrcA raw", "SrcA regressed",
           "VSiN Makinen raw", "VSiN centered", "ESPN FPI raw", "FPI centered", "Combined B centered",
           "Win total BetMGM", "Win total Fanatics", "Win total consensus", "WinTotal conflict?", "SrcC implied pts",
           "Prior current (A only)", "Prior A+B VSiN", "Prior A+B FPI", "Prior A+B combined", "Prior A+B+C combined",
           "Wk1 eff current (W1-A)", "Wk1 eff current (W1-B)",
           "Wk1 eff A+B VSiN (W1-A)", "Wk1 eff A+B FPI (W1-A)", "Wk1 eff A+B comb (W1-A)", "Wk1 eff A+B comb (W1-B)",
           "Wk1 eff A+B+C comb (W1-A)",
           "Rank current", "Rank A+B VSiN", "Rank A+B FPI", "Rank A+B comb", "Rank A+B+C comb", "FPI rank",
           "Flag TTW-vs-FPI >=2.5", "Flag rank gap >=8", "Flag movement >=1.5", "Flag SrcC direction",
           "Flag GP0-dependent >=0.8"]
    rows = []
    for t in teams:
        gap = abs(W1A["current"][t] - fpi_c[t])
        rgap = abs(ranks["current"][t] - fpi_rank[t])
        move = abs(S["AB_comb"][t] - S["current"][t])
        c_pull = S["ABC_comb"][t] - S["AB_comb"][t]
        b_pull = S["AB_comb"][t] - S["current"][t]
        cdir = (abs(c_pull) >= 0.5 and c_pull * b_pull < 0)
        gp0 = abs(W1B["current"][t] - W1A["current"][t])
        rows.append([t, fmt(srcA_raw[t]), fmt(srcA_reg[t]),
                     fmt(vsin[t]), fmt(vsin_c[t]), fmt(fpi[t]), fmt(fpi_c[t]), fmt(comb_c[t]),
                     fmt(mgm[t]), fmt(fan[t]), fmt(cons[t]), "Y" if mgm[t] != fan[t] else "N", fmt(implied[t]),
                     fmt(S["current"][t]), fmt(S["AB_vsin"][t]), fmt(S["AB_fpi"][t]), fmt(S["AB_comb"][t]), fmt(S["ABC_comb"][t]),
                     fmt(W1A["current"][t]), fmt(W1B["current"][t]),
                     fmt(W1A["AB_vsin"][t]), fmt(W1A["AB_fpi"][t]), fmt(W1A["AB_comb"][t]), fmt(W1B["AB_comb"][t]),
                     fmt(W1A["ABC_comb"][t]),
                     ranks["current"][t], ranks["AB_vsin"][t], ranks["AB_fpi"][t], ranks["AB_comb"][t], ranks["ABC_comb"][t], fpi_rank[t],
                     "Y" if gap >= 2.5 else "N", "Y" if rgap >= 8 else "N", "Y" if move >= 1.5 else "N",
                     "Y" if cdir else "N", "Y" if gp0 >= 0.8 else "N"])
    with open(OUT_SHADOW, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(hdr)
        w.writerows(rows)

    # ---- game-level before/after CSV ----
    qb = prov["engine_semantics"]["qb_deltas"]
    scen = [("current_W1A", W1A["current"]), ("current_W1B", W1B["current"]),
            ("AB_vsin_W1A", W1A["AB_vsin"]), ("AB_fpi_W1A", W1A["AB_fpi"]),
            ("AB_comb_W1A", W1A["AB_comb"]), ("AB_comb_W1B", W1B["AB_comb"]),
            ("ABC_comb_W1A", W1A["ABC_comb"])]
    hdr2 = ["Seq", "GameID", "Date", "Away", "Home", "Neutral", "Market home spread"]
    for name, _ in scen:
        hdr2 += [f"{name} FinalMargin", f"{name} edge", f"{name} side"]
    hdr2 += ["Edge>=3 any scenario", "Side flips vs current"]
    rows2 = []
    for g in prov["market_lines_week1"]["games"]:
        hfa = 0 if g["neutral"] else 1.6
        qadj = qb.get(g["home"], 0) - qb.get(g["away"], 0)
        row = [g["seq"], g["game_id"], g["date"], g["away"], g["home"],
               "Y" if g["neutral"] else "", fmt(g["mkt_home_spread"])]
        sides, any3 = [], False
        for name, eff in scen:
            fm = xround(eff[g["home"]] - eff[g["away"]] + hfa + qadj)
            edge = xround(fm + g["mkt_home_spread"])
            side = g["home"] if edge > 0 else (g["away"] if edge < 0 else "-")
            if abs(edge) >= 3:
                any3 = True
            sides.append(side)
            row += [fmt(fm), fmt(edge), side]
        row += ["Y" if any3 else "N", "Y" if len(set(sides)) > 1 else "N"]
        rows2.append(row)
    with open(OUT_WK1, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(hdr2)
        w.writerows(rows2)

    # ---- validations ----
    assert len(teams) == 32
    assert abs(sum(vsin.values()) / 32 - 24.0) < 1e-9, "VSiN mean must be exactly 24.0"
    for name, c in (("vsin", vsin_c), ("fpi", fpi_c), ("comb", comb_c)):
        assert abs(sum(c.values())) <= 0.16, f"{name} centered sum drifted: {sum(c.values())}"
    assert abs(sum(implied.values())) <= 0.16, "implied pts not centered"
    # spot-verify task-stated DAL/NYG production figures
    assert srcA_reg["DAL"] == -2.82 and srcA_reg["NYG"] == -1.99
    assert W1A["current"]["DAL"] == -2.26 and W1A["current"]["NYG"] == -1.59
    dal_nyg = [g for g in prov["market_lines_week1"]["games"] if g["game_id"] == "2026_01_DAL_NYG"][0]
    fm = xround(W1A["current"]["NYG"] - W1A["current"]["DAL"] + 1.6)
    assert fm == 2.27 and xround(fm + dal_nyg["mkt_home_spread"]) == 4.77
    print("wrote", OUT_SHADOW)
    print("wrote", OUT_WK1)
    print("validations passed")


if __name__ == "__main__":
    main()
