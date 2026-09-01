#!/usr/bin/env python3
"""Build TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx from the v1.2 QB working copy.
Edits ONLY: LV row 23 approved input cells (QB VALUES), START HERE version banner,
and a new CHANGELOG entry. All other zip members copied verbatim."""
import zipfile, re

SRC="TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx"

SOURCE_NOTE=("Kirk Cousins confirmed Raiders Week 1 QB1 (HC Klint Kubiak named Cousins starter to open camp; "
             "ESPN/Schefter, FOX News, Bleacher Report, Aug 2026). Confirmed Week 1 starter; +0.50 deviation reflects "
             "veteran experience and Kubiak-scheme familiarity, capped by age, immobility, recent efficiency and "
             "turnover concerns. Baseline QB Fernando Mendoza = 0. Approved 2026-08-05.")

BANNER_OLD="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)"
BANNER_NEW="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.2.1)"

CH_CHANGE=("QB preseason activation. QB VALUES manual fields populated from current (Aug 2026) research for all 32 teams: "
           "28 teams initialized at zero (active QB == baseline QB), 3 left blank at Low confidence pending open competitions "
           "(ATL, CLE, MIN), and 1 approved deviation entered — LV: baseline Fernando Mendoza = 0, active Kirk Cousins = +0.50. "
           "No formulas, weights, thresholds, methodology, schedule, market lines, adjustments, ratings, settings, historical "
           "or backtest data changed.")
CH_IMPACT=("Model impact limited to the single approved LV QB delta (+0.50 spread, scaled to totals via QBTotFactor). "
           "All other QB deltas remain 0; backtest metrics unchanged.")

ROW5_OLD='<row r="5"><c r="A5" s="2"/><c r="B5" s="2"/><c r="C5" s="2"/><c r="D5" s="2"/></row>'

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

ROW5_NEW=(
 '<row r="5">'
 '<c r="A5" s="2" t="inlineStr"><is><t>1.2.1</t></is></c>'
 '<c r="B5" s="2" t="inlineStr"><is><t>2026-08-05</t></is></c>'
 f'<c r="C5" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CH_CHANGE)}</t></is></c>'
 f'<c r="D5" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CH_IMPACT)}</t></is></c>'
 '</row>')

def replace_cell(xml, coord, newcell):
    """Replace a cell element. Self-closing form MUST be tried first: a blank cell
    like <c r="C23" s="14"/> would otherwise be matched by the paired-tag pattern
    (since [^>]* can consume the '/'), causing .*?</c> to swallow the NEXT cell."""
    c=re.escape(coord)
    self_closing=re.compile(r'<c r="%s"[^>]*?/>'%c)
    out,n=self_closing.subn(lambda m: newcell, xml, count=1)
    if n==1:
        return out
    paired=re.compile(r'<c r="%s"[^>]*>.*?</c>'%c, re.S)
    out,n=paired.subn(lambda m: newcell, xml, count=1)
    if n!=1: raise RuntimeError(f"replace failed {coord} n={n}")
    return out

zin=zipfile.ZipFile(SRC)

# --- QB VALUES: LV row 23 approved inputs only ---
qb=zin.read("xl/worksheets/sheet6.xml").decode("utf-8")
qb=replace_cell(qb,"C23",'<c r="C23" s="14"><v>0</v></c>')                       # Baseline value = 0
qb=replace_cell(qb,"E23",'<c r="E23" s="14"><v>0.5</v></c>')                     # Active value = +0.50
qb=replace_cell(qb,"I23",'<c r="I23" s="14" t="inlineStr"><is><t>High</t></is></c>')
qb=replace_cell(qb,"J23",f'<c r="J23" s="14" t="inlineStr"><is><t xml:space="preserve">{esc(SOURCE_NOTE)}</t></is></c>')
# D23 (Kirk Cousins), K23 (2026-08-05 = 46239), M23 (2026) already correct in v1.2 — untouched

# --- banner ---
ss=zin.read("xl/sharedStrings.xml").decode("utf-8")
assert ss.count(BANNER_OLD)==1, "banner not unique"
ss=ss.replace(BANNER_OLD,BANNER_NEW)

# --- CHANGELOG ---
ch=zin.read("xl/worksheets/sheet21.xml").decode("utf-8")
assert ch.count(ROW5_OLD)==1, "changelog row5 template not unique"
ch=ch.replace(ROW5_OLD,ROW5_NEW)

zout=zipfile.ZipFile(DST,"w")
for info in zin.infolist():
    data=zin.read(info.filename)
    if info.filename=="xl/worksheets/sheet6.xml": data=qb.encode("utf-8")
    elif info.filename=="xl/sharedStrings.xml":   data=ss.encode("utf-8")
    elif info.filename=="xl/worksheets/sheet21.xml": data=ch.encode("utf-8")
    zout.writestr(info,data)
zout.close(); zin.close()
print("Built",DST)
