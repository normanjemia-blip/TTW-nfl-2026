#!/usr/bin/env python3
"""Collect every genuine version-label reference (non-formula text) in the workbook.
Read-only. Determines canonical intended version."""
import openpyxl, re, json
WB="TTW_NFL_v1_1_1 Version 2.xlsx"
wf=openpyxl.load_workbook(WB, data_only=False)

# Match version tokens like v1.0 / v1.1 / v1.1.1 / "version 1.1" in human text (not formulas)
tok=re.compile(r'v\s*\d+\.\d+(?:\.\d+)?', re.IGNORECASE)
evidence=[]
for ws in wf.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v=c.value
            if isinstance(v,str) and not v.startswith("="):
                for m in tok.finditer(v):
                    evidence.append({"sheet":ws.title,"cell":c.coordinate,"token":m.group(0),"text":v[:200]})

print("=== Genuine version-label tokens (non-formula text) ===")
tally={}
for e in evidence:
    t=e["token"].lower().replace(" ","")
    tally[t]=tally.get(t,0)+1
    print(f"[{e['sheet']}!{e['cell']}] token={e['token']!r}  ::  {e['text']}")
print("\n=== Token tally ===")
for k in sorted(tally): print(f"  {k}: {tally[k]}")

json.dump(evidence, open("audit/version_evidence.json","w"), indent=2)
print("\nSaved audit/version_evidence.json")
