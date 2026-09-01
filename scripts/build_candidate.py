#!/usr/bin/env python3
"""Build the v1.1 version-alignment candidate by surgical XML edits.
Changes ONLY:
  - xl/sharedStrings.xml : START HERE!A1 banner (v1.0)->(v1.1)  [si index 0, unique]
  - xl/worksheets/sheet21.xml (CHANGELOG): populate existing empty row 4 with a new entry
Every other zip member is copied byte-for-byte. Source is never modified."""
import zipfile, sys

SRC="TTW_NFL_v1_1_1 Version 2.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx"

BANNER_OLD="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.0)"
BANNER_NEW="TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)"

ROW4_OLD='<row r="4"><c r="A4" s="2"/><c r="B4" s="2"/><c r="C4" s="2"/><c r="D4" s="2"/></row>'

CHANGE=("Version-label alignment (documentation only). START HERE banner corrected from "
        "(v1.0) to (v1.1) to match the canonical version proven across CHANGELOG latest entry 1.1, "
        "SETTINGS parameter-freeze note (frozen as of v1.1, 2026-07-13), DICTIONARY v1.1 sections, "
        "AUDIT V1.1 safety-pass test report, and BACKTEST parameter freeze v1.1. No formulas, weights, "
        "thresholds, methodology, schedule, sample/backtest data, QB values, adjustments, ratings, or "
        "settings changed. Historical v1.0 references (BACKTEST archive values A82/A83, AUDIT v1.0 test "
        "report A27/A45, HISTORY 2025 spread-provenance note A2) intentionally left untouched.")
IMPACT=("None. Documentation-only banner correction; model outputs and backtest metrics unchanged "
        "(Spread MAE 10.376; Totals MAE 10.787).")

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

ROW4_NEW=(
    '<row r="4">'
    '<c r="A4" s="2" t="inlineStr"><is><t>1.1</t></is></c>'
    '<c r="B4" s="2" t="inlineStr"><is><t>2026-07-23</t></is></c>'
    f'<c r="C4" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(CHANGE)}</t></is></c>'
    f'<c r="D4" s="2" t="inlineStr"><is><t xml:space="preserve">{esc(IMPACT)}</t></is></c>'
    '</row>'
)

zin=zipfile.ZipFile(SRC,"r")
names=zin.namelist()

# sanity checks first
ss=zin.read("xl/sharedStrings.xml").decode("utf-8")
assert ss.count(BANNER_OLD)==1, f"banner not unique: {ss.count(BANNER_OLD)}"
sh=zin.read("xl/worksheets/sheet21.xml").decode("utf-8")
assert sh.count(ROW4_OLD)==1, f"row4 template not found uniquely: {sh.count(ROW4_OLD)}"

ss_new=ss.replace(BANNER_OLD, BANNER_NEW)
sh_new=sh.replace(ROW4_OLD, ROW4_NEW)
assert ss_new.count("(v1.1)")>=1 and ss_new.count(BANNER_OLD)==0
assert "Version-label alignment" in sh_new

zout=zipfile.ZipFile(DST,"w")
for info in zin.infolist():
    data=zin.read(info.filename)
    if info.filename=="xl/sharedStrings.xml":
        data=ss_new.encode("utf-8")
    elif info.filename=="xl/worksheets/sheet21.xml":
        data=sh_new.encode("utf-8")
    # preserve original name & compression type
    zout.writestr(info, data)
zout.close(); zin.close()
print("Built", DST)
print("Members:", len(names))
