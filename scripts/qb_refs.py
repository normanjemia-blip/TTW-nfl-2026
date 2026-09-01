#!/usr/bin/env python3
import openpyxl, re
WB="TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx"
wf=openpyxl.load_workbook(WB, data_only=False)

print("=== Defined names containing 'QB' ===")
for name, dn in wf.defined_names.items():
    if 'qb' in name.lower() or 'QB' in name:
        print(f"  {name} -> {dn.value}")

print("\n=== ALL defined names referencing 'QB VALUES' sheet ===")
for name, dn in wf.defined_names.items():
    if 'QB VALUES' in str(dn.value):
        print(f"  {name} -> {dn.value}")

# Which columns of QB VALUES do named ranges cover?
print("\n=== Search all sheets for formulas referencing QB VALUES col C or E (baseline/active value) ===")
hits_C=0; hits_E=0; hits_named={}
named_qb=[n for n,d in wf.defined_names.items() if 'QB VALUES' in str(d.value)]
for ws in wf.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v=c.value
            if isinstance(v,str) and v.startswith("="):
                if re.search(r"'QB VALUES'!\$?C", v): hits_C+=1
                if re.search(r"'QB VALUES'!\$?E", v): hits_E+=1
                for nm in named_qb:
                    if re.search(r'\b'+re.escape(nm)+r'\b', v):
                        hits_named[nm]=hits_named.get(nm,0)+1
print(f"  direct refs to 'QB VALUES'!C*: {hits_C}")
print(f"  direct refs to 'QB VALUES'!E*: {hits_E}")
print(f"  usage counts of QB-VALUES named ranges: {hits_named}")

# Show what each QB named range maps to (column)
print("\n=== QB-VALUES named ranges column mapping ===")
for nm in named_qb:
    print(f"  {nm} -> {wf.defined_names[nm].value}")
