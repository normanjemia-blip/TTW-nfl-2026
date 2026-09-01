#!/usr/bin/env python3
import openpyxl
WB="TTW_NFL_v1_1_1 Version 2.xlsx"
wf=openpyxl.load_workbook(WB, data_only=False)
cells=[("START HERE","A1"),("HISTORY 2025","A2"),("BACKTEST","A82"),
       ("BACKTEST","A83"),("AUDIT","A27"),("AUDIT","A45")]
for sh,co in cells:
    v=wf[sh][co].value
    print(f"\n===== {sh}!{co} =====\n{v}")
