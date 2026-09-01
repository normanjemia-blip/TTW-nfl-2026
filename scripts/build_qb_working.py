#!/usr/bin/env python3
"""Create TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx from the authoritative v1.1
by surgically editing ONLY QB VALUES (sheet6.xml) manual cells. All other zip members
copied verbatim (drawings, persons, formulas, other sheets untouched)."""
import zipfile, re, sys, datetime
sys.path.insert(0,"scripts")
from qb_dataset import TEAMS
from openpyxl.utils.datetime import to_excel

SRC="TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx"
KSERIAL=int(to_excel(datetime.datetime(2026,8,5)))   # Last update date

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def cell_style(xml, coord):
    m=re.search(r'<c r="%s"([^>]*)>.*?</c>'%coord, xml) or re.search(r'<c r="%s"([^>]*)/>'%coord, xml)
    if not m: raise RuntimeError("cell %s not found"%coord)
    sm=re.search(r'\bs="(\d+)"', m.group(1))
    return sm.group(1) if sm else None

def replace_cell(xml, coord, newcell):
    # match either <c ...>...</c> or self-closing <c .../>
    pat=re.compile(r'<c r="%s"(?:[^>]*)>.*?</c>|<c r="%s"[^>]*/>'%(re.escape(coord),re.escape(coord)))
    new_xml, n = pat.subn(lambda m: newcell, xml, count=1)
    if n!=1: raise RuntimeError("replace failed for %s (n=%d)"%(coord,n))
    return new_xml

def num_cell(coord, s, val):
    return f'<c r="{coord}" s="{s}"><v>{val}</v></c>'
def empty_cell(coord, s):
    return f'<c r="{coord}" s="{s}"/>'
def inline_cell(coord, s, text):
    return f'<c r="{coord}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{esc(text)}</t></is></c>'

zin=zipfile.ZipFile(SRC)
xml=zin.read("xl/worksheets/sheet6.xml").decode("utf-8")

changes=[]
for (row,team,base_qb,starter,status,conf,active_override,note) in TEAMS:
    sC=cell_style(xml,f"C{row}"); sE=cell_style(xml,f"E{row}")
    sI=cell_style(xml,f"I{row}"); sJ=cell_style(xml,f"J{row}")
    sK=cell_style(xml,f"K{row}"); sD=cell_style(xml,f"D{row}")
    # C / E (baseline value / active value)
    if status=="settled":
        xml=replace_cell(xml,f"C{row}",num_cell(f"C{row}",sC,0)); changes.append((team,f"C{row}","->0"))
        xml=replace_cell(xml,f"E{row}",num_cell(f"E{row}",sE,0)); changes.append((team,f"E{row}","->0"))
    else:  # uncertain / deviation -> blank
        xml=replace_cell(xml,f"C{row}",empty_cell(f"C{row}",sC)); changes.append((team,f"C{row}","->blank"))
        xml=replace_cell(xml,f"E{row}",empty_cell(f"E{row}",sE)); changes.append((team,f"E{row}","->blank"))
    # D (active QB) only if override (deviation)
    if active_override:
        xml=replace_cell(xml,f"D{row}",inline_cell(f"D{row}",sD,active_override)); changes.append((team,f"D{row}","->"+active_override))
    # I confidence
    xml=replace_cell(xml,f"I{row}",inline_cell(f"I{row}",sI,conf)); changes.append((team,f"I{row}","->"+conf))
    # J source/notes
    xml=replace_cell(xml,f"J{row}",inline_cell(f"J{row}",sJ,note)); changes.append((team,f"J{row}","source"))
    # K last update -> 2026-08-05
    xml=replace_cell(xml,f"K{row}",num_cell(f"K{row}",sK,KSERIAL)); changes.append((team,f"K{row}",str(KSERIAL)))
    # M already 2026 (CurrentSeason) -> leave unchanged

# write DST copying all members verbatim except sheet6.xml
zout=zipfile.ZipFile(DST,"w")
for info in zin.infolist():
    data=zin.read(info.filename)
    if info.filename=="xl/worksheets/sheet6.xml":
        data=xml.encode("utf-8")
    zout.writestr(info, data)
zout.close(); zin.close()
print(f"Built {DST}")
print(f"K serial (2026-08-05) = {KSERIAL}")
print(f"Total QB manual-cell edits: {len(changes)}")
