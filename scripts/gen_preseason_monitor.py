#!/usr/bin/env python3
"""Generate/refresh preseason/PRESEASON_MONITOR.csv — repo-local intake for PS Wk1 (Aug 13-15 2026).
Decision stays PENDING and Workbook Updated? = N for every row (no live-workbook authorization)."""
import csv, os
HDR=["PS Wk","Game Date","Game Status","Team","Opponent","Site","Starter Use","Player / Unit",
     "Confirmed Finding","Injury / Availability","Source URL","Source Date","Evidence Type",
     "Confidence","Proposed Destination","Proposed Change","Decision","Workbook Updated?","Blocker"]

SBD13="https://www.sportsbettingdime.com/news/nfl/whos-playing-preseason-week1-thursday-august-13/"
COV13="https://www.covers.com/nfl/preseason-lineup-updates-tonight-august-13-2026"
COV14="https://www.covers.com/nfl/preseason-lineup-updates-tonight-august-14-2026"
SBD14="https://www.sportsbettingdime.com/news/nfl/2026-preseason-week-1-whos-playing-friday-game-by-game-guide/"
ROUND14="https://www.joxfm.com/2026/08/14/nfl-preseason-roundup-new-look-dolphins-offense-finds-stride/"
NFLPS="https://www.nfl.com/scores/2026/preseason-week-1"
VIK="https://www.vikings.com/news/kyler-murray-quarterback-starting-2026-nfl-season"
NFL10="https://www.nfl.com/news/2026-nfl-preseason-week-1-10-things-to-watch"

B="UNVERIFIED — no qualifying source located for starter participation; post-game confirmation outstanding"
R=[]
def row(d,st,t,o,site,su,unit,find,inj,url,sd,et,cf,dest,chg,blk=""):
    R.append(["1",d,st,t,o,site,su,unit,find,inj,url,sd,et,cf,dest,chg,"PENDING","N",blk])

# ---- Aug 13 (COMPLETE) ----
row("2026-08-13","COMPLETE","DET","CIN","Away","RESTED","Jared Goff","HC rested QB1 Goff; few starters used","No injury tied to rest",COV13,"2026-08-13","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-13","COMPLETE","CIN","DET","Home","LIMITED","Joe Burrow + offensive starters","Burrow and most offensive starters played a limited number of reps/drives","None reported",SBD13,"2026-08-13","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-13","COMPLETE","GB","PIT","Away","LIMITED","Jordan Love","Love expected to get some playing time; HC: anybody healthy ready to play","None reported",SBD13,"2026-08-13","BEAT REPORT","LOW","NONE","PRESEASON MONITOR log only","Pre-game expectation only; post-game snap confirmation UNVERIFIED")
row("2026-08-13","COMPLETE","PIT","GB","Home","RESTED","Aaron Rodgers","CONFLICT: HC wanted Rodgers snaps; reporting indicates Rodgers likely sat with Rudolph/Allar/Howard under center","None reported",SBD13,"2026-08-13","BEAT REPORT","LOW","NONE","PRESEASON MONITOR log only","Unresolved conflict on whether Rodgers took any snaps")
row("2026-08-13","COMPLETE","IND","NE","Away","TBD","UNVERIFIED","No qualifying source for starter participation","UNVERIFIED",NFLPS,"2026-08-13","OTHER","LOW","NONE","None",B)
row("2026-08-13","COMPLETE","NE","IND","Home","TBD","UNVERIFIED","No qualifying source for starter participation","UNVERIFIED",NFLPS,"2026-08-13","OTHER","LOW","NONE","None",B)
row("2026-08-13","COMPLETE","LAC","HOU","Away","RESTED","Justin Herbert","HC rested QB1 Herbert","No injury tied to rest",SBD13,"2026-08-13","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-13","COMPLETE","HOU","LAC","Home","TBD","UNVERIFIED","No qualifying source for starter participation","UNVERIFIED",NFLPS,"2026-08-13","OTHER","LOW","NONE","None",B)
row("2026-08-13","COMPLETE","ARI","LV","Away","TBD","UNVERIFIED","No qualifying source for ARI starter participation","UNVERIFIED",NFLPS,"2026-08-13","OTHER","LOW","NONE","None",B)
row("2026-08-13","COMPLETE","LV","ARI","Home","LIMITED","Fernando Mendoza (QB2)","No.1 overall pick Mendoza took the field; consistent with staged-development plan behind Cousins","None reported",SBD13,"2026-08-13","BEAT REPORT","MEDIUM","QB VALUES","QB VALUES: LV Source/Last-update fields (re-verification only; no value change)","Kirk Cousins' own snap count UNVERIFIED")
row("2026-08-13","COMPLETE","TEN","SF","Away","TBD","UNVERIFIED","No qualifying source for starter participation","UNVERIFIED",NFLPS,"2026-08-13","OTHER","LOW","NONE","None",B)
row("2026-08-13","COMPLETE","SF","TEN","Home","TBD","UNVERIFIED","No qualifying source for starter participation","UNVERIFIED",NFLPS,"2026-08-13","OTHER","LOW","NONE","None",B)
# ---- Aug 14 (COMPLETE) ----
row("2026-08-14","COMPLETE","DEN","ATL","Away","MIXED","Bo Nix / starters","HC gave starters early snaps but QB1 Bo Nix was held out entirely; Stidham took QB reps","Nix held out — no diagnosis reported",COV14,"2026-08-14","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only","Reason for Nix hold-out not stated (rest vs precaution)")
row("2026-08-14","COMPLETE","ATL","DEN","Home","STARTERS PLAYED","Tua Tagovailoa","Tua started the preseason opener with a full complement of offensive weapons","Michael Penix Jr. sidelined (ACL)",SBD14,"2026-08-14","BEAT REPORT","MEDIUM","QB VALUES","QB VALUES: ATL Source/Notes + Last-update fields","Post-game snap total for Tua UNVERIFIED")
row("2026-08-14","COMPLETE","TB","NYJ","Away","RESTED","Baker Mayfield","Mayfield expected to be held back as incumbent QB1","Jake Browning (QB2) nursing a back injury",SBD14,"2026-08-14","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only","Browning diagnosis/timeline not specified")
row("2026-08-14","COMPLETE","NYJ","TB","Home","STARTERS PLAYED","Geno Smith, Breece Hall, Garrett Wilson","HC Aaron Glenn: 'everyone's playing'; QB1 Geno Smith played with Hall and Wilson","None reported",SBD14,"2026-08-14","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-14","COMPLETE","MIA","WAS","Away","STARTERS PLAYED","Malik Willis","First look at new QB1 Malik Willis (3yr/$67.5M); new-look offense worked with starters","None reported",ROUND14,"2026-08-14","BEAT REPORT","MEDIUM","QB VALUES","QB VALUES: MIA Source/Last-update fields (confirms baseline QB role)")
row("2026-08-14","COMPLETE","WAS","MIA","Home","RESTED","Jayden Daniels / Marcus Mariota","QB1 Daniels not expected to suit up; QB2 Mariota started","LT Laremy Tunsil torn triceps (reported 2026-08-12), expected to miss significant time",SBD14,"2026-08-14","BEAT REPORT","MEDIUM","ADJUSTMENTS","ADJUSTMENTS: create documented entry for WAS starting-LT availability (field creation only, no point value)")
# ---- Aug 15 (NOT PLAYED) ----
for t,o,site in [("CAR","BUF","Away"),("BUF","CAR","Home"),("CLE","CHI","Away"),("CHI","CLE","Home"),
                 ("MIN","NYG","Away"),("NYG","MIN","Home"),("LA","KC","Away"),("KC","LA","Home"),
                 ("JAX","NO","Away"),("NO","JAX","Home"),("PHI","BAL","Away"),("BAL","PHI","Home"),
                 ("DAL","SEA","Away"),("SEA","DAL","Home")]:
    if t=="MIN":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Kyler Murray / J.J. McCarthy",
            "Pre-game (2026-08-12, OFFICIAL): HC named Murray the regular-season Week 1 starter; McCarthy backup",
            "None reported",VIK,"2026-08-12","OFFICIAL","HIGH","QB VALUES",
            "QB VALUES: MIN Confidence field (Medium -> High) + Source/Last-update fields; Active QB already equals Baseline")
    elif t=="CLE":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Deshaun Watson / Shedeur Sanders",
            "Pre-game (OFFICIAL): Watson starts the opener, Sanders starts PS Wk2; HC 'not shutting the door' — competition NOT settled",
            "None reported",NFL10,"2026-08-12","OFFICIAL","HIGH","QB VALUES",
            "QB VALUES: CLE Source/Last-update fields; remains UNCERTAIN (no confidence change)")
    elif t=="KC":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Patrick Mahomes",
            "Pre-game: HC indicated Mahomes will not play the opener; cleared for camp after Dec ACL/LCL surgery",
            "Cleared for camp; participation withheld by choice",NFL10,"2026-08-12","MULTI-SOURCE","HIGH","NONE",
            "PRESEASON MONITOR log only")
    elif t=="JAX":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Starters","Pre-game: HC said starters will not play the opener","None reported",
            NFL10,"2026-08-12","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
    elif t=="CAR":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Bryce Young + starters","Pre-game: HC said Young and starters will play the opener",
            "EDGE Nic Scourton torn ACL (first practice)",NFL10,"2026-08-12","MULTI-SOURCE","MEDIUM","ADJUSTMENTS",
            "ADJUSTMENTS: create documented entry for CAR EDGE availability (field creation only, no point value)")
    elif t=="DAL":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Starters","Pre-game: HC said 'we're not going to play a lot of our starters'","None reported",
            NFL10,"2026-08-12","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
    elif t=="CHI":
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","Secondary / LT","Pre-game: multiple secondary absences; starting LT undecided",
            "Gordon PUP (calf); Bryant 4-6 mo post knee surgery; Flowers out for season; Bishop suspended 3 games",
            NFL10,"2026-08-12","OFFICIAL","HIGH","ADJUSTMENTS","ADJUSTMENTS: create documented entries for CHI secondary availability (field creation only)")
    else:
        row("2026-08-15","NOT PLAYED",t,o,site,"TBD","UNVERIFIED","Game not yet played; no qualifying pre-game starter-usage statement located",
            "UNVERIFIED",NFLPS,"2026-08-15","OTHER","LOW","NONE","None","Awaiting kickoff; post-game intake required")

os.makedirs("preseason",exist_ok=True)
with open("preseason/PRESEASON_MONITOR.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(HDR); w.writerows(R)
with open("preseason/intake_template.csv","w",newline="") as f:
    csv.writer(f).writerow(HDR)
print(f"rows={len(R)} teams={len(set(r[3] for r in R))}")
