#!/usr/bin/env python3
"""Aug-10 QB sweep candidate, built from the v1.2.1 QB checkpoint (NOT the v1.3 market candidate).
Edits ONLY QB VALUES manual inputs for ATL/CLE/MIN/LV, plus version banner + CHANGELOG.
All zero-delta: no new nonzero deviation is introduced; LV stays at the approved +0.50."""
import zipfile, re

SRC="TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.2.2_QB_SWEEP_CANDIDATE.xlsx"
K=46244  # 2026-08-10

BANNER_OLD="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.2.1)"
BANNER_NEW="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.2.2)"
ROW6_OLD='<row r="6"><c r="A6" s="2"/><c r="B6" s="2"/><c r="C6" s="2"/><c r="D6" s="2"/></row>'

ATL_NOTE=("RESOLVED to baseline QB. Rapoport/NFL Network 2026-08-09: Tua projected Week 1 starter; Michael Penix Jr. "
          "NOT medically cleared after third ACL surgery and not fully practicing — 'this is not a competition until "
          "he is fully practicing.' Tua healthy, taking first-team reps (early-camp issue resolved; Cooper Rush signed "
          "as veteran depth). Not officially announced and job is conditional, hence Medium. Active == Baseline, delta 0.")
CLE_NOTE=("STILL OPEN — not resolvable. Monken has NOT named a starter; Watson and Sanders alternate first-team days and "
          "each starts one of the first two preseason games. Decision not expected until after the 2026-08-22 game vs BUF "
          "(Washington Post/CBS/ESPN, Aug 2026). Values left blank, Low confidence. Re-verified 2026-08-10.")
MIN_NOTE=("RESOLVED to baseline QB. Murray out-snapped McCarthy 63-33 with the first team over the last four practices and "
          "is 'pulling away'/'separating' (Athlon, MinnesotaSportsFan, TheVikingAge, Aug 2026); ~2/3 of first-team 11-on-11 "
          "snaps. The one McCarthy snap edge (32-26) was 2026-08-01 total team snaps incl. scout team, a single-day reversal. "
          "No official announcement yet, hence Medium. Active == Baseline, delta 0.")
LV_NOTE=("Kirk Cousins confirmed Raiders Week 1 QB1 — re-verified 2026-08-10. HC Klint Kubiak named Cousins QB1 to open camp "
         "(Raiders.com official, NFL.com, ESPN); Cousins healthy entering 2026; Mendoza developing gradually as QB2 "
         "('competing with, not against'). No credible contradicting evidence. Approved deviation +0.50 unchanged: veteran "
         "experience and Kubiak-scheme familiarity, capped by age, immobility, recent efficiency and turnover concerns. "
         "Baseline QB Fernando Mendoza = 0.")

CH_CHANGE=("Aug-10 QB preseason sweep (no valuation change). Fresh current-source review of the flagged QB situations. "
           "ATL resolved to baseline Tua Tagovailoa (Penix not medically cleared) and MIN resolved to baseline Kyler Murray "
           "(separating in first-team snaps) — both Active == Baseline, initialized 0/0 at Medium confidence. CLE remains "
           "genuinely open (no starter named; decision after the 2026-08-22 preseason game) and stays blank at Low. LV "
           "re-verified: Cousins confirmed QB1 and healthy, approved +0.50 deviation unchanged. No new nonzero deviation. "
           "No formulas, market lines, adjustments, team ratings, settings, schedule, historical or backtest data changed.")
CH_IMPACT=("No model impact: every changed row is zero-delta. The only nonzero QB delta league-wide remains LV +0.50. "
           "QB readiness moves from 29 OK / 3 UNCERTAIN to 31 OK / 1 UNCERTAIN.")

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

ROW6_NEW=('<row r="6">'
 '<c r="A6" s="2" t="inlineStr"><is><t>1.2.2</t></is></c>'
 '<c r="B6" s="2" t="inlineStr"><is><t>2026-08-10</t></is></c>'
 f'<c r="C6" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CH_CHANGE)}</t></is></c>'
 f'<c r="D6" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CH_IMPACT)}</t></is></c>'
 '</row>')

def replace_cell(xml, coord, newcell):
    """Self-closing form MUST be tried first (v1.2.1 build defect)."""
    c=re.escape(coord)
    out,n=re.subn(r'<c r="%s"[^>]*?/>'%c, lambda m: newcell, xml, count=1)
    if n==1: return out
    out,n=re.subn(r'<c r="%s"[^>]*>.*?</c>'%c, lambda m: newcell, xml, count=1, flags=re.S)
    if n!=1: raise RuntimeError(f"replace failed {coord} n={n}")
    return out

zin=zipfile.ZipFile(SRC)
qb=zin.read("xl/worksheets/sheet6.xml").decode("utf-8")

def set_note(x,row,note): return replace_cell(x,f"J{row}",
    f'<c r="J{row}" s="14" t="inlineStr"><is><t xml:space="preserve">{esc(note)}</t></is></c>')
def set_date(x,row): return replace_cell(x,f"K{row}",f'<c r="K{row}" s="15"><v>{K}</v></c>')
def set_conf(x,row,v): return replace_cell(x,f"I{row}",
    f'<c r="I{row}" s="14" t="inlineStr"><is><t>{v}</t></is></c>')

# ATL row 6 -> resolved to baseline, 0/0, Medium
qb=replace_cell(qb,"C6",'<c r="C6" s="14"><v>0</v></c>')
qb=replace_cell(qb,"E6",'<c r="E6" s="14"><v>0</v></c>')
qb=set_conf(qb,6,"Medium"); qb=set_note(qb,6,ATL_NOTE); qb=set_date(qb,6)
# CLE row 12 -> unchanged values/confidence; refresh note+date only
qb=set_note(qb,12,CLE_NOTE); qb=set_date(qb,12)
# LV row 23 -> values unchanged (0 / 0.5, High); refresh note+date only
qb=set_note(qb,23,LV_NOTE); qb=set_date(qb,23)
# MIN row 25 -> resolved to baseline, 0/0, Medium
qb=replace_cell(qb,"C25",'<c r="C25" s="14"><v>0</v></c>')
qb=replace_cell(qb,"E25",'<c r="E25" s="14"><v>0</v></c>')
qb=set_conf(qb,25,"Medium"); qb=set_note(qb,25,MIN_NOTE); qb=set_date(qb,25)

ss=zin.read("xl/sharedStrings.xml").decode("utf-8")
assert ss.count(BANNER_OLD)==1
ss=ss.replace(BANNER_OLD,BANNER_NEW)
ch=zin.read("xl/worksheets/sheet21.xml").decode("utf-8")
assert ch.count(ROW6_OLD)==1
ch=ch.replace(ROW6_OLD,ROW6_NEW)

zout=zipfile.ZipFile(DST,"w")
for info in zin.infolist():
    d=zin.read(info.filename)
    if   info.filename=="xl/worksheets/sheet6.xml":  d=qb.encode("utf-8")
    elif info.filename=="xl/sharedStrings.xml":      d=ss.encode("utf-8")
    elif info.filename=="xl/worksheets/sheet21.xml": d=ch.encode("utf-8")
    zout.writestr(info,d)
zout.close(); zin.close()
print("Built",DST)
