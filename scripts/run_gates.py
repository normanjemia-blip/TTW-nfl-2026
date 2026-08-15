#!/usr/bin/env python3
"""Workbook invariant gate suite (read-only). Exit 0 = pass."""
import openpyxl, sys, datetime
A="TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx"
def main():
    f=[]
    wf=openpyxl.load_workbook(A,data_only=False); wv=openpyxl.load_workbook(A,data_only=True)
    if len(wf.sheetnames)!=21: f.append(f"sheets={len(wf.sheetnames)} != 21")
    n=sum(1 for sh in wf.worksheets for row in sh.iter_rows() for c in row
          if (isinstance(c.value,str) and c.value.startswith("=")) or c.data_type=="f")
    if n!=57399: f.append(f"formulas={n} != 57399")
    s=wv["SETTINGS"]
    if s.cell(67,2).value!="N": f.append("GATE: BET labels must be OFF (SETTINGS B67 != 'N')")
    if [s.cell(26,2).value,s.cell(27,2).value,s.cell(28,2).value]!=[3.0,1.5,1.0]: f.append("ATS thresholds drifted")
    if [s.cell(29,2).value,s.cell(30,2).value,s.cell(31,2).value]!=[3.0,1.5,1.0]: f.append("Totals thresholds drifted")
    if s.cell(40,2).value!="VALIDATE-ONLY": f.append("win-totals mode must remain VALIDATE-ONLY")
    sch=wf["IMPORT SCHEDULE"]
    reg=sum(1 for r in range(6,sch.max_row+1) if sch.cell(r,2).value==2026 and sch.cell(r,3).value=="REG")
    if reg!=272: f.append(f"2026 REG games={reg} != 272")
    p=wf["PRESEASON"]
    if sum(1 for r in range(5,37) if p.cell(r,9).value not in (None,"")): f.append("PRESEASON SrcB(public) must remain blank")
    if f:
        print("GATE SUITE: FAIL"); [print("  -",x) for x in f]; return 1
    print(f"GATE SUITE: PASS (21 sheets, {n} formulas, BET OFF, thresholds 3.0/1.5/1.0, "
          f"VALIDATE-ONLY, 272 REG, PRESEASON SrcB blank)")
    return 0
if __name__=="__main__": sys.exit(main())
