#!/usr/bin/env python3
import sys, csv, json, openpyxl
sys.path.insert(0,"scripts")
from qb_dataset import TEAMS
SRC="TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx"
DST="TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx"

# priced-in baseline values from authoritative (for reference in deviation report)
wa=openpyxl.load_workbook(SRC,data_only=False)["QB VALUES"]
priced={wa.cell(r,1).value:{"baseline_qb":wa.cell(r,2).value,"priced_value":wa.cell(r,3).value,
        "baseline_conf":wa.cell(r,9).value} for r in range(5,37)}

# 32-team research CSV + JSON
rows=[]
for (row,team,base,starter,status,conf,active_override,note) in TEAMS:
    active = active_override if active_override else base
    rows.append({
        "team":team,"row":row,
        "baseline_qb":base,
        "projected_week1_starter":starter,
        "active_qb_in_sheet":active,
        "status":status,
        "confidence":conf,
        "baseline_value":(0 if status=="settled" else ""),
        "active_value":(0 if status=="settled" else ""),
        "delta":0,
        "priced_in_value_v1_1":priced[team]["priced_value"],
        "reviewed_season":2026,
        "last_update":"2026-08-05",
        "notes":note,
    })
with open("audit/qb_research_2026.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump({"generated":"2026-08-05","as_of":"2026-08-05","teams":rows}, open("audit/qb_research_2026.json","w"), indent=2)

# changed-cells audit: compare authoritative vs working (ground truth)
a=openpyxl.load_workbook(SRC,data_only=False)["QB VALUES"]
b=openpyxl.load_workbook(DST,data_only=False)["QB VALUES"]
changed=[]
colname={1:"Team",2:"Baseline QB",3:"Baseline value",4:"Active QB",5:"Active value",
         9:"Confidence",10:"Source/Notes",11:"Last update",13:"Reviewed season"}
for r in range(5,37):
    for c in range(1,14):
        va=a.cell(r,c).value; vb=b.cell(r,c).value
        va=va.text if hasattr(va,"text") else va
        vb=vb.text if hasattr(vb,"text") else vb
        if va!=vb:
            changed.append({"cell":a.cell(r,c).coordinate,"column":colname.get(c,f"col{c}"),
                            "team":a.cell(r,1).value,
                            "old":("" if va is None else va),"new":("" if vb is None else vb)})
with open("audit/qb_changed_cells.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["cell","column","team","old","new"]); w.writeheader(); w.writerows(changed)
json.dump(changed, open("audit/qb_changed_cells.json","w"), indent=2, default=str)
print("research rows:",len(rows),"| changed cells:",len(changed))
print("by column:", {k:sum(1 for x in changed if x['column']==k) for k in set(x['column'] for x in changed)})
