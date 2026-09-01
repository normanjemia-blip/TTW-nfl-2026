#!/usr/bin/env python3
"""Build v1.3 MARKET candidate from v1.2.1 QB candidate.
Edits ONLY MARKET LINES Week-1 input cells (G,H,I,N,O,P rows 5-20), the version
banner, and a new CHANGELOG entry. All other zip members copied verbatim.
Does NOT touch QB VALUES, ADJUSTMENTS, TEAM RATINGS, SETTINGS, schedule, or any formula."""
import zipfile, re, sys
sys.path.insert(0,"scripts")
from market_dataset import WEEK1, LINE_DATE, SOURCE, NOTE

SRC="TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.3_MARKET_CANDIDATE.xlsx"

BANNER_OLD="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.2.1)"
BANNER_NEW="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.3)"
ROW6_OLD='<row r="6"><c r="A6" s="2"/><c r="B6" s="2"/><c r="C6" s="2"/><c r="D6" s="2"/></row>'

CH_CHANGE=("Week 1 market line population (Phase 2). MARKET LINES rows 5-20 populated with the "
           "2026-05-15 DraftKings OPENING lines from the schedule release (favorite + positive spread + total), "
           "recorded with true source and line date. These are OPENING lines, not current: the sheet's own "
           "staleness rule flags all 16 as STALE against the 2026-07-13 As-of date. Refresh with Novig lines "
           "before any live use. No formulas, weights, thresholds, methodology, schedule, QB values, "
           "adjustments, team ratings, settings, historical or backtest data changed.")
CH_IMPACT=("No methodology impact. Enables the spread/total edge pipeline for Week 1 against opening lines only; "
           "every row is flagged STALE until current lines are entered.")

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

ROW6_NEW=('<row r="6">'
 '<c r="A6" s="2" t="inlineStr"><is><t>1.3</t></is></c>'
 '<c r="B6" s="2" t="inlineStr"><is><t>2026-08-06</t></is></c>'
 f'<c r="C6" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CH_CHANGE)}</t></is></c>'
 f'<c r="D6" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CH_IMPACT)}</t></is></c>'
 '</row>')

def replace_cell(xml, coord, newcell):
    """Self-closing form MUST be tried first (see v1.2.1 build defect)."""
    c=re.escape(coord)
    out,n=re.subn(r'<c r="%s"[^>]*?/>'%c, lambda m: newcell, xml, count=1)
    if n==1: return out
    out,n=re.subn(r'<c r="%s"[^>]*>.*?</c>'%c, lambda m: newcell, xml, count=1, flags=re.S)
    if n!=1: raise RuntimeError(f"replace failed {coord} n={n}")
    return out

def style_of(xml,coord):
    m=re.search(r'<c r="%s"([^>]*?)/>|<c r="%s"([^>]*?)>'%(re.escape(coord),re.escape(coord)),xml)
    attrs=(m.group(1) or m.group(2) or "")
    sm=re.search(r'\bs="(\d+)"',attrs)
    return sm.group(1) if sm else "0"

zin=zipfile.ZipFile(SRC)
ml=zin.read("xl/worksheets/sheet4.xml").decode("utf-8")

edits=0
for (row,away,home,fav,spread,total) in WEEK1:
    sG=style_of(ml,f"G{row}"); sH=style_of(ml,f"H{row}"); sI=style_of(ml,f"I{row}")
    sN=style_of(ml,f"N{row}"); sO=style_of(ml,f"O{row}"); sP=style_of(ml,f"P{row}")
    ml=replace_cell(ml,f"G{row}",f'<c r="G{row}" s="{sG}" t="inlineStr"><is><t>{esc(fav)}</t></is></c>')
    ml=replace_cell(ml,f"H{row}",f'<c r="H{row}" s="{sH}"><v>{spread}</v></c>')
    ml=replace_cell(ml,f"I{row}",f'<c r="I{row}" s="{sI}"><v>{total}</v></c>')
    ml=replace_cell(ml,f"N{row}",f'<c r="N{row}" s="{sN}" t="inlineStr"><is><t xml:space="preserve">{esc(SOURCE)}</t></is></c>')
    ml=replace_cell(ml,f"O{row}",f'<c r="O{row}" s="{sO}" t="inlineStr"><is><t>{LINE_DATE}</t></is></c>')
    ml=replace_cell(ml,f"P{row}",f'<c r="P{row}" s="{sP}" t="inlineStr"><is><t xml:space="preserve">{esc(NOTE)}</t></is></c>')
    edits+=6

ss=zin.read("xl/sharedStrings.xml").decode("utf-8")
assert ss.count(BANNER_OLD)==1, "banner not unique"
ss=ss.replace(BANNER_OLD,BANNER_NEW)

ch=zin.read("xl/worksheets/sheet21.xml").decode("utf-8")
assert ch.count(ROW6_OLD)==1, "changelog row6 template not unique"
ch=ch.replace(ROW6_OLD,ROW6_NEW)

zout=zipfile.ZipFile(DST,"w")
for info in zin.infolist():
    data=zin.read(info.filename)
    if   info.filename=="xl/worksheets/sheet4.xml":  data=ml.encode("utf-8")
    elif info.filename=="xl/sharedStrings.xml":      data=ss.encode("utf-8")
    elif info.filename=="xl/worksheets/sheet21.xml": data=ch.encode("utf-8")
    zout.writestr(info,data)
zout.close(); zin.close()
print(f"Built {DST}; market input cells written: {edits}")
