#!/usr/bin/env python3
import zipfile, hashlib, json, csv, openpyxl
SRC="TTW_NFL_v1_1_1 Version 2.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.1_VERSION_ALIGNMENT_CANDIDATE.xlsx"

# 1) changed cells CSV + JSON
changed=[
 {"sheet":"START HERE","cell":"A1","type":"version-label correction (proven mislabel)",
  "old":"TO THE WINDOW — NFL POWER RATINGS 2026 (v1.0)",
  "new":"TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)"},
 {"sheet":"CHANGELOG","cell":"A4","type":"new changelog entry — Version","old":"", "new":"1.1"},
 {"sheet":"CHANGELOG","cell":"B4","type":"new changelog entry — Date","old":"", "new":"2026-07-23"},
 {"sheet":"CHANGELOG","cell":"C4","type":"new changelog entry — Change",
  "old":"", "new":"Version-label alignment (documentation only). START HERE banner corrected from (v1.0) to (v1.1) to match the canonical version proven across CHANGELOG latest entry 1.1, SETTINGS parameter-freeze note (frozen as of v1.1, 2026-07-13), DICTIONARY v1.1 sections, AUDIT V1.1 safety-pass test report, and BACKTEST parameter freeze v1.1. No formulas, weights, thresholds, methodology, schedule, sample/backtest data, QB values, adjustments, ratings, or settings changed. Historical v1.0 references (BACKTEST archive values A82/A83, AUDIT v1.0 test report A27/A45, HISTORY 2025 spread-provenance note A2) intentionally left untouched."},
 {"sheet":"CHANGELOG","cell":"D4","type":"new changelog entry — Backtest impact",
  "old":"", "new":"None. Documentation-only banner correction; model outputs and backtest metrics unchanged (Spread MAE 10.376; Totals MAE 10.787)."},
]
json.dump(changed, open("audit/changed_cells.json","w"), indent=2)
with open("audit/changed_cells.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=["sheet","cell","type","old","new"]); w.writeheader()
    for c in changed: w.writerow(c)
print(f"Wrote changed_cells.csv/json ({len(changed)} cells)")

# 2) per-member byte parity (which members differ)
zs=zipfile.ZipFile(SRC); zd=zipfile.ZipFile(DST)
def md5(b): return hashlib.md5(b).hexdigest()
differ=[]; same=0
for name in zs.namelist():
    a=zs.read(name); b=zd.read(name)
    if md5(a)!=md5(b): differ.append(name)
    else: same+=1
print(f"\nZip members byte-identical: {same}/{len(zs.namelist())}")
print("Members that DIFFER (expected exactly the 2 edited):", differ)
drawings_persons_ok=all(md5(zs.read(n))==md5(zd.read(n))
                        for n in zs.namelist() if "drawing" in n or "person" in n)
print("All drawings/persons byte-identical:", drawings_persons_ok)

# 3) production-state parity (candidate)
wf=openpyxl.load_workbook(DST,data_only=False)
wv=openpyxl.load_workbook(DST,data_only=True)
def is_input(v):
    if v is None: return False
    if isinstance(v,str) and (v.strip()=="" or v.startswith("=")): return False
    return True
wvm=wv["MARKET LINES"]; usable=sum(1 for r in range(5,wvm.max_row+1) if wvm.cell(r,17).value not in (None,""))
adj=sum(1 for r in range(5,wf["ADJUSTMENTS"].max_row+1) for c in (1,2,3,4,7,8,9,10,11,12) if is_input(wf["ADJUSTMENTS"].cell(r,c).value))
wsq=wf["QB VALUES"]; qbnz=0
for r in range(5,wsq.max_row+1):
    b=wsq.cell(r,3).value; a=wsq.cell(r,5).value
    if isinstance(b,(int,float)) and isinstance(a,(int,float)) and b!=a: qbnz+=1
ovr=sum(1 for r in range(5,wf["TEAM RATINGS"].max_row+1) if is_input(wf["TEAM RATINGS"].cell(r,9).value))
print("\nCandidate production-state: usable_market_spreads=%d adjustments=%d qb_nonzero=%d team_overrides=%d"%(usable,adj,qbnz,ovr))
