#!/usr/bin/env python3
"""Build TTW_NFL_Power_Ratings_2026_v1.4_SRCB_BLENDFIX_CANDIDATE.xlsx.

Base: a FRESH read-only export of the live Google Sheet (not the stale repo workbook).
Two authorized changes only:
  (1) PRESEASON Source B populated for all 32 teams with the audited equal-weight
      VSiN(Makinen p29) / ESPN FPI composite  -> cols I (paste), K (source), L (as-of)
  (2) TEAM RATINGS D5:D36 blank-preservation fix so a blank CalcGoverned no longer
      coerces to numeric 0, letting the existing H-column fallback use 100% prior at GP=0

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

    zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == PRESEASON:
            data = ps.encode("utf-8")
        elif info.filename == TEAM_RATINGS:
            data = tr.encode("utf-8")
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
