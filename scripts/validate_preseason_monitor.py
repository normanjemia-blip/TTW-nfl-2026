#!/usr/bin/env python3
"""Validator for preseason/PRESEASON_MONITOR.csv. Exit 0 = pass."""
import csv, sys, re
PATH="preseason/PRESEASON_MONITOR.csv"
HDR=["PS Wk","Game Date","Game Status","Team","Opponent","Site","Starter Use","Player / Unit",
     "Confirmed Finding","Injury / Availability","Source URL","Source Date","Evidence Type",
     "Confidence","Proposed Destination","Proposed Change","Decision","Workbook Updated?","Blocker"]
STARTER={"TBD","STARTERS PLAYED","LIMITED","RESTED","MIXED"}
CONF={"HIGH","MEDIUM","LOW"}
EVID={"OFFICIAL","MULTI-SOURCE","BEAT REPORT","GAME OBSERVATION","MARKET","OTHER"}
DEST={"NONE","QB VALUES","ADJUSTMENTS","PRESEASON"}
DEC={"MONITOR","UPDATE","IGNORE","PENDING"}
STATUS={"COMPLETE","NOT PLAYED"}
TEAMS={"ARI","ATL","BAL","BUF","CAR","CHI","CIN","CLE","DAL","DEN","DET","GB","HOU","IND","JAX","KC",
       "LA","LAC","LV","MIA","MIN","NE","NO","NYG","NYJ","PHI","PIT","SEA","SF","TB","TEN","WAS"}
DATES={"2026-08-13","2026-08-14","2026-08-15"}

def main():
    errs=[]
    rows=list(csv.DictReader(open(PATH)))
    hdr=list(rows[0].keys()) if rows else []
    if hdr!=HDR: errs.append(f"header mismatch: {hdr}")
    if len(rows)!=32: errs.append(f"expected 32 team-game rows, got {len(rows)}")
    seen=set()
    for i,r in enumerate(rows,2):
        t=r["Team"]
        if t in seen: errs.append(f"r{i}: duplicate team {t}")
        seen.add(t)
        if t not in TEAMS: errs.append(f"r{i}: unknown team {t}")
        if r["Opponent"] not in TEAMS: errs.append(f"r{i}: unknown opponent {r['Opponent']}")
        if r["Game Date"] not in DATES: errs.append(f"r{i}: bad date {r['Game Date']}")
        for col,allowed in (("Starter Use",STARTER),("Confidence",CONF),("Evidence Type",EVID),
                            ("Proposed Destination",DEST),("Decision",DEC),("Game Status",STATUS)):
            if r[col] not in allowed: errs.append(f"r{i} {t}: bad {col}={r[col]!r}")
        # GATE: no live-workbook writes authorized
        # GATE: documented Decision/Workbook-Updated lifecycle consistency
        _d,_u=r["Decision"],r["Workbook Updated?"]
        if _u not in {"Y","N"}: errs.append(f"r{i} {t}: Workbook Updated? must be Y or N, got {_u!r}")
        if _d in {"PENDING","MONITOR","IGNORE"} and _u!="N":
            errs.append(f"r{i} {t}: Decision {_d} requires Workbook Updated? = N")
        if _d=="PENDING" and _u=="Y": errs.append(f"r{i} {t}: PENDING/Y is never permitted")

        # GATE: games not played cannot claim starter usage
        if r["Game Status"]=="NOT PLAYED" and r["Starter Use"]!="TBD":
            errs.append(f"r{i} {t}: NOT PLAYED must have Starter Use=TBD")
        # GATE: a COMPLETE game left at TBD must carry a named blocker (never a silent gap)
        if r["Game Status"]=="COMPLETE" and r["Starter Use"]=="TBD" and not r["Blocker"].strip():
            errs.append(f"r{i} {t}: COMPLETE game left TBD without a named blocker")
        # GATE: every material claim needs a source URL + date
        if not re.match(r"^https?://", r["Source URL"]): errs.append(f"r{i} {t}: missing/invalid Source URL")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", r["Source Date"]): errs.append(f"r{i} {t}: bad Source Date")
        # GATE: unverified rows must carry a named blocker (never silent)
        if ("UNVERIFIED" in r["Confirmed Finding"] or "UNVERIFIED" in r["Injury / Availability"]) and not r["Blocker"].strip():
            errs.append(f"r{i} {t}: UNVERIFIED without a named blocker")
        # GATE: a destination implies a described change
        if r["Proposed Destination"]!="NONE" and not r["Proposed Change"].strip():
            errs.append(f"r{i} {t}: destination set but no Proposed Change")
        # GATE: proposed change must not contain a numeric rating/point value
        if re.search(r"[+-]?\d+(\.\d+)?\s*(pt|point)", r["Proposed Change"], re.I):
            errs.append(f"r{i} {t}: Proposed Change must not carry a point value")
    if set(TEAMS)-seen: errs.append(f"missing teams: {sorted(set(TEAMS)-seen)}")
    if errs:
        print("PRESEASON MONITOR VALIDATOR: FAIL"); [print("  -",e) for e in errs]; return 1
    comp=sum(1 for r in rows if r["Game Status"]=="COMPLETE")
    tbd=sum(1 for r in rows if r["Starter Use"]=="TBD")
    print(f"PRESEASON MONITOR VALIDATOR: PASS ({len(rows)} rows, 32 teams, {comp} complete, "
          f"{len(rows)-comp} not played, {tbd} still TBD w/ blocker, "
          f"{sum(1 for r in rows if r['Blocker'].strip())} blockers)")
    return 0
if __name__=="__main__": sys.exit(main())
