#!/usr/bin/env python3
"""Build TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx.

Base: a FRESH read-only export of the live Google Sheet (not the stale repo workbook).
Four authorized changes only:
  (1) PRESEASON Source B populated for all 32 teams with the audited equal-weight
      VSiN(Makinen p29) / ESPN FPI composite  -> cols I (paste), K (source), L (as-of)
  (2) TEAM RATINGS D5:D36 blank-preservation fix so a blank CalcGoverned no longer
      coerces to numeric 0, letting the existing H-column fallback use 100% prior at GP=0
  (3) START HERE version banner v1.1 -> v1.4                        (Phase 5A)
  (4) One new CHANGELOG row (row 7) documenting the v1.4 release    (Phase 5A)

Everything else is copied verbatim: every market line, QB value, setting, weight,
threshold, formula, named range, drawing, and the live-only PRESEASON MONITOR tab.
Source C stays unpopulated and WinTotalsMode stays VALIDATE-ONLY.

Cached <v> values are refreshed for the edited cells and their same-sheet dependents
(PRESEASON I/J/K/L/S/T, TEAM RATINGS D/F/H/J/K). Downstream sheets (ENGINE, DASHBOARD,
DATA QUALITY) are left to recalculate on open -- the workbook carries <calcPr/> with no
calcId, so Excel full-recalculates on load and Google Sheets recalculates on import.
Expected recalculated values are published in the verification report and slate CSV.
"""
import hashlib
import json
import os
import re
import shutil
import zipfile
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROV = os.path.join(ROOT, "audit", "TTW_NFL_2026_Preseason_Prior_Provenance_20260901.json")
DST = os.path.join(ROOT, "TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx")

PRESEASON = "xl/worksheets/sheet17.xml"
TEAM_RATINGS = "xl/worksheets/sheet8.xml"
CHANGELOG = "xl/worksheets/sheet22.xml"
SHARED = "xl/sharedStrings.xml"

BANNER_OLD = "TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)"
BANNER_NEW = "TO THE WINDOW — NFL POWER RATINGS 2026 (v1.4)"

CH_ROW = 7                       # first empty CHANGELOG row in the base
CH_VERSION = "1.4"
CH_DATE = "2026-09-01"
CH_CHANGE = (
    "Preseason prior sources completed and the Week-1 blend coercion fixed. "
    "(1) PRESEASON Source B populated for all 32 teams from the equal-weight composite of Steve Makinen's "
    "2026 VSiN NFL Betting Guide 2.0 page-29 power ratings and ESPN FPI numeric values (ESPN last updated "
    "2026-08-31T14:44Z); per-row source citation and as-of date recorded. The workbook's own centering and "
    "weight-renormalization formulas are unchanged. "
    "(2) TEAM RATINGS!D5:D36 changed to the ISNUMBER-protected lookup "
    "IFERROR(IF(ISNUMBER(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0))),ROUND(INDEX(CalcGoverned,MATCH($A5,CalcTeams,0)),2),\"\"),\"\"). "
    "A blank CalcGoverned previously coerced to numeric 0 in Google Sheets, silently compressing every Week-1 "
    "rating to 80% of its preseason prior. "
    "(3) With D blank at GP=0 the existing, unmodified H-column fallback now applies, so Week 1 retains 100% of "
    "the preseason prior. The blend schedule itself is unchanged and still 0.80 at week 1. "
    "(4) Source C (market win totals) remains blank for all 32 teams. "
    "(5) Win-totals mode remains VALIDATE-ONLY. "
    "(6) No change to source weights (A 0.40 / B 0.35 / C 0.25), recommendation thresholds, QB values, market "
    "lines, team overrides or adjustments. "
    "Formula behaviour verified natively in Google Sheets on a disposable probe sheet, 2026-09-01.")
CH_IMPACT = (
    "No retune and no backtest change: the 2025 walk-forward metrics are unaffected because Source B and the "
    "GP=0 fallback act only on 2026 preseason priors at zero games played. 2026 Week-1 effective ratings change "
    "for all 32 teams (mean absolute 0.84 pts, max 2.09) as the intended combined effect of adding Source B and "
    "removing the unintended 20% Week-1 compression. Edges of 3.0+ on the Week-1 board fall from five to two.")

SRCB_SOURCE = ("Equal-weight composite: Steve Makinen power ratings, 2026 VSiN NFL Betting Guide 2.0 p29 "
               "(private subscriber guide, numeric table only) + ESPN FPI numeric values "
               "(https://www.espn.com/nfl/fpi, ESPN last updated 2026-08-31T14:44Z). Audited 2026-09-01.")
SRCB_ASOF = "2026-09-01"

# TEAM RATINGS D: blank CalcGoverned must stay blank instead of coercing to numeric 0.
# ISNUMBER is a type test, so it is FALSE for both a formula-blank ("" ) and a truly empty
# cell, and FALSE (never propagating) for the #N/A a missing team produces; the outer
# IFERROR is retained from the original formula.
D_FORMULA_OLD = 'IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A{r},CalcTeams,0)),2),"")'
D_FORMULA_NEW = ('IFERROR(IF(ISNUMBER(INDEX(CalcGoverned,MATCH($A{r},CalcTeams,0))),'
                 'ROUND(INDEX(CalcGoverned,MATCH($A{r},CalcTeams,0)),2),""),"")')


def xround(x, nd=2):
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def num(x):
    """Excel-style numeric literal for a cached value."""
    s = repr(float(x))
    return s[:-2] if s.endswith(".0") else s


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def replace_cell(xml, coord, newcell):
    """Replace one <c> element. Self-closing form MUST be tried first: a blank cell like
    <c r="I5" s="12"/> would otherwise be matched by the paired-tag pattern (since [^>]*
    can consume the '/'), making .*?</c> swallow the NEXT cell."""
    c = re.escape(coord)
    out, n = re.subn(r'<c r="%s"[^>]*?/>' % c, lambda m: newcell, xml, count=1)
    if n == 1:
        return out
    out, n = re.subn(r'<c r="%s"[^>]*>.*?</c>' % c, lambda m: newcell, xml, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("replace failed %s n=%d" % (coord, n))
    return out


def build(src):
    prov = json.load(open(PROV))
    vsin = prov["source_B_vsin"]["values"]
    fpi = prov["source_B_fpi"]["values"]
    srcA_raw = {t: v[0] for t, v in prov["source_A"]["values_raw"].items()}
    teams = sorted(srcA_raw)
    assert len(teams) == 32 and set(vsin) == set(fpi) == set(teams)

    # PRESEASON row order is alphabetical by team, rows 5..36 (verified against the export).
    comp = {t: (vsin[t] + fpi[t]) / 2 for t in teams}
    mean = sum(comp.values()) / 32
    centered = {t: xround(comp[t] - mean) for t in teams}                       # PRESEASON!J
    srcA_reg = {t: xround(srcA_raw[t] * (1 - 0.33)) for t in teams}             # PRESEASON!E (unchanged)
    prior = {t: xround((0.4 * srcA_reg[t] + 0.35 * centered[t]) / 0.75) for t in teams}  # PRESEASON!S
    rank = {t: 1 + sum(1 for u in teams if prior[u] > prior[t]) for t in teams}          # TEAM RATINGS!K

    # Never assume row order: read the team column out of the source and assert it.
    import openpyxl
    _wb = openpyxl.load_workbook(src, read_only=True)
    for _sheet, _col, _label in (("PRESEASON", 2, "PRESEASON!B"), ("TEAM RATINGS", 1, "TEAM RATINGS!A")):
        got = [_wb[_sheet].cell(5 + i, _col).value for i in range(32)]
        assert got == teams, "%s row order is %s, expected alphabetical" % (_label, got)
    _wb.close()

    zin = zipfile.ZipFile(src)
    ps = zin.read(PRESEASON).decode("utf-8")
    tr = zin.read(TEAM_RATINGS).decode("utf-8")
    manifest = []

    for i, t in enumerate(teams):
        r = 5 + i
        # --- PRESEASON: Source B inputs + refreshed same-sheet cached values ---
        ps = replace_cell(ps, "I%d" % r, '<c r="I%d" s="12"><v>%s</v></c>' % (r, num(comp[t])))
        manifest.append(("PRESEASON", "I%d" % r, t, "(blank)", num(comp[t]), "SrcB composite paste"))
        ps = replace_cell(ps, "K%d" % r,
                          '<c r="K%d" s="12" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                          % (r, esc(SRCB_SOURCE)))
        manifest.append(("PRESEASON", "K%d" % r, t, "(blank)", "<source citation>", "SrcB source"))
        ps = replace_cell(ps, "L%d" % r,
                          '<c r="L%d" s="12" t="inlineStr"><is><t>%s</t></is></c>' % (r, SRCB_ASOF))
        manifest.append(("PRESEASON", "L%d" % r, t, "(blank)", SRCB_ASOF, "SrcB as-of"))
        # J (centered) keeps its shared formula; only the cached value/type changes.
        jf = ('<f t="shared" ref="J5:J36" si="2">IF($I5=&quot;&quot;,&quot;&quot;,'
              'ROUND($I5-AVERAGE($I$5:$I$36),2))</f>') if r == 5 else '<f t="shared" si="2"/>'
        ps = replace_cell(ps, "J%d" % r, '<c r="J%d" s="3">%s<v>%s</v></c>' % (r, jf, num(centered[t])))
        manifest.append(("PRESEASON", "J%d" % r, t, "(blank)", num(centered[t]), "SrcB centered (cached)"))
        # S (effective prior) and T (sources used): formulas untouched, cached values refreshed.
        m = re.search(r'<c r="S%d"[^>]*>(<f>.*?</f>)' % r, ps, re.S)
        ps = replace_cell(ps, "S%d" % r, '<c r="S%d" s="3">%s<v>%s</v></c>' % (r, m.group(1), num(prior[t])))
        manifest.append(("PRESEASON", "S%d" % r, t, num(srcA_reg[t]), num(prior[t]), "Effective prior (cached)"))
        m = re.search(r'<c r="T%d"[^>]*>(<f>.*?</f>)' % r, ps, re.S)
        ps = replace_cell(ps, "T%d" % r, '<c r="T%d" s="3">%s<v>2</v></c>' % (r, m.group(1)))
        manifest.append(("PRESEASON", "T%d" % r, t, "1", "2", "Sources used (cached)"))

        # --- TEAM RATINGS: D formula fix + refreshed same-sheet cached values ---
        old_f = D_FORMULA_OLD.format(r=r)
        assert esc(old_f) in tr, "D%d old formula not found" % r
        tr = replace_cell(tr, "D%d" % r,
                          '<c r="D%d" s="3" t="str"><f t="array" ref="D%d">%s</f><v></v></c>'
                          % (r, r, esc(D_FORMULA_NEW.format(r=r))))
        manifest.append(("TEAM RATINGS", "D%d" % r, t, "0 (coerced)", "(blank)", "In-season governed: blank-preserving fix"))
        for col, val, note in (("F", prior[t], "Preseason prior (cached)"),
                               ("H", prior[t], "Blended base -> 100% prior at GP=0 (cached)"),
                               ("J", prior[t], "EFFECTIVE RATING (cached)")):
            m = re.search(r'<c r="%s%d"[^>]*>(<f.*?(?:</f>|/>))' % (col, r), tr, re.S)
            tr = replace_cell(tr, "%s%d" % (col, r),
                              '<c r="%s%d" s="3">%s<v>%s</v></c>' % (col, r, m.group(1), num(val)))
            manifest.append(("TEAM RATINGS", "%s%d" % (col, r), t, "", num(val), note))
        m = re.search(r'<c r="K%d"[^>]*>(<f.*?(?:</f>|/>))' % r, tr, re.S)
        tr = replace_cell(tr, "K%d" % r, '<c r="K%d" s="3">%s<v>%d</v></c>' % (r, m.group(1), rank[t]))
        manifest.append(("TEAM RATINGS", "K%d" % r, t, "", str(rank[t]), "Rank (cached)"))

    # --- (3) START HERE version banner ---
    ss = zin.read(SHARED).decode("utf-8")
    assert ss.count(BANNER_OLD) == 1, "banner string not unique in sharedStrings"
    ss = ss.replace(BANNER_OLD, BANNER_NEW)
    manifest.append(("START HERE", "banner", "", BANNER_OLD, BANNER_NEW, "Version banner (sharedStrings)"))

    # --- (4) one new CHANGELOG row, styles matched to the row above ---
    ch = zin.read(CHANGELOG).decode("utf-8")
    old_row = ('<row r="%d"><c r="A%d" s="3"/><c r="B%d" s="3"/><c r="C%d" s="3"/><c r="D%d" s="3"/></row>'
               % ((CH_ROW,) * 5))
    assert ch.count(old_row) == 1, "CHANGELOG row %d is not the expected empty row" % CH_ROW
    cell = lambda col, style, txt: (
        '<c r="%s%d" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
        % (col, CH_ROW, style, esc(txt)))
    ch = ch.replace(old_row, '<row r="%d">%s%s%s%s</row>' % (
        CH_ROW, cell("A", 44, CH_VERSION), cell("B", 43, CH_DATE),
        cell("C", 44, CH_CHANGE), cell("D", 44, CH_IMPACT)))
    for col, val in (("A", CH_VERSION), ("B", CH_DATE), ("C", "<v1.4 change entry>"),
                     ("D", "<v1.4 backtest impact>")):
        manifest.append(("CHANGELOG", "%s%d" % (col, CH_ROW), "", "(blank)", val, "New CHANGELOG entry"))

    zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == PRESEASON:
            data = ps.encode("utf-8")
        elif info.filename == TEAM_RATINGS:
            data = tr.encode("utf-8")
        elif info.filename == SHARED:
            data = ss.encode("utf-8")
        elif info.filename == CHANGELOG:
            data = ch.encode("utf-8")
        zout.writestr(info, data)
    zout.close()
    zin.close()
    return prior, rank, centered, comp, manifest


if __name__ == "__main__":
    import sys
    src = sys.argv[1]
    prior, rank, centered, comp, manifest = build(src)
    print("built", DST)
    print("sha256", hashlib.sha256(open(DST, "rb").read()).hexdigest())
    print("cells written:", len(manifest))
    for t in ("DAL", "NYG"):
        print(f"  {t}: SrcB paste {comp[t]:.4f} -> centered {centered[t]} -> prior {prior[t]} -> rank {rank[t]}")
