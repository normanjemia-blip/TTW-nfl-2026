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
SBD15="https://www.sportsbettingdime.com/news/nfl/preseason-week-1-whos-playing-starting-saturday-aug-15/"
VIKG="https://www.vikings.com/news/jj-mccarthy-kyler-murray-preseason-debut-giants-2026"
STRIB="https://www.startribune.com/minnesota-vikings-new-york-giants-score-updates-nfl-preseason-game-today-channel-kyler-murray-stats/601873734"
ESPNBUF="https://www.espn.com/nfl/recap?gameId=401873282"
PFN15="https://www.profootballnetwork.com/nfl-starters-saturday-preseason-bills-browns/"
VIKSTART="https://www.vikings.com/news/kyler-murray-quarterback-starting-2026-nfl-season"
NFLTUNSIL="https://www.nfl.com/news/commanders-lt-laremy-tunsil-suffered-torn-triceps-likely-to-miss-significant-portion-of-season"
SAINTS1="https://www.neworleanssaints.com/news/garrett-nelson-edge-new-orleans-saints-roster-moves-august-7-2026"
SAINTS2="https://www.neworleanssaints.com/news/kahlil-saunders-saints-roster-moves-training-camp-august-12-2026"
CLEQB1="https://sports.yahoo.com/nfl/live/nfl-news-injury-updates-preseason-week-2-schedule-whos-playing-starters-143714619.html"

B="UNVERIFIED — no qualifying source located for starter participation; post-game confirmation outstanding"
R=[]
def row(d,st,t,o,site,su,unit,find,inj,url,sd,et,cf,dest,chg,blk="",dec="PENDING",upd="N"):
    R.append(["1",d,st,t,o,site,su,unit,find,inj,url,sd,et,cf,dest,chg,dec,upd,blk])

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
row("2026-08-14","COMPLETE","WAS","MIA","Home","RESTED","Jayden Daniels / Marcus Mariota",
    "QB1 Daniels not expected to suit up; QB2 Mariota started",
    "LT Laremy Tunsil suffered a torn triceps and is expected to miss a significant portion of the season. "
    "Replacement left tackle not officially named.",
    NFLTUNSIL,"2026-08-08","OFFICIAL","HIGH","NONE",
    "Monitor-layer record only: starting-LT availability. No points, rating, formula or model change proposed.",
    "Replacement left tackle unconfirmed; no source names a designated starter.","MONITOR","N")
# ---- Aug 15 (COMPLETE — post-game evidence) ----
row("2026-08-15","COMPLETE","CAR","BUF","Away","STARTERS PLAYED","Bryce Young + starters",
    "Young started and played roughly 10-20 snaps; starters opened with a three-and-out",
    "Haynes King (hamstring); Damien Lewis doubtful; Derrick Brown questionable (knee soreness)",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","BUF","CAR","Home","STARTERS PLAYED","Josh Allen + first-string offense",
    "Allen played a limited series with the first-string starters","None reported",
    ESPNBUF,"2026-08-15","MULTI-SOURCE","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","CLE","CHI","Away","STARTERS PLAYED","Deshaun Watson / Shedeur Sanders",
    "Watson started and played the first half; Sanders took the second half. RESOLVED 2026-08-24: the Browns "
    "officially named Deshaun Watson the 2026 starting quarterback over Shedeur Sanders, who becomes the backup.",
    "None reported",CLEQB1,"2026-08-24","OFFICIAL","HIGH","QB VALUES",
    "QB VALUES: CLE Confidence Low->High, Source citation and Last-update applied in v1.1_AUTHORITATIVE "
    "(I12/J12/K12). C12/E12 unchanged at 1.0; no model output changed.",
    "","UPDATE","Y")
row("2026-08-15","COMPLETE","CHI","CLE","Home","RESTED",
    "Caleb Williams / Tyson Bagent; secondary: Kyler Gordon, Coby Bryant, Dallis Flowers, Beanie Bishop Jr.",
    "QB1 Caleb Williams rested by plan; Bagent started roughly one half",
    "Kyler Gordon on PUP with a calf injury, no firm return timeline; Coby Bryant expected out 4-6 months after "
    "knee surgery; Dallis Flowers on Reserve/Injured, reported out for the season; Beanie Bishop Jr. suspended for "
    "the first three regular-season games. WR Luther Burden III sidelined by a leg injury, no diagnosis reported.",
    NFL10,"2026-08-12","OFFICIAL","HIGH","NONE",
    "Monitor-layer record only: four secondary availability statuses. No points, rating, formula or model change proposed.",
    "Burden III diagnosis and timeline not reported.","MONITOR","N")
row("2026-08-15","COMPLETE","MIN","NYG","Away","LIMITED","Kyler Murray / J.J. McCarthy",
    "Head Coach Kevin O'Connell named Murray the starter, and Murray played the first series in his Vikings "
    "preseason debut; J.J. McCarthy played most of the first half.",
    "WR Justin Jefferson sat out (reason not reported)",
    VIKG+" ; "+VIKSTART,"2026-08-15","OFFICIAL","HIGH","QB VALUES",
    "QB VALUES: MIN Confidence Low->High, Source citation and Last-update applied in v1.1_AUTHORITATIVE "
    "(I25/J25/K25). C25/E25 unchanged at 3.0; no model output changed.",
    "Reason for Jefferson sitting out not reported","UPDATE","Y")
row("2026-08-15","COMPLETE","NYG","MIN","Home","LIMITED","Jaxson Dart",
    "Dart started; starters were out by the second quarter",
    "None reported for NYG. RECORD CORRECTION 2026-08-24: the earlier entry attributed a carted-off Jamal Adams "
    "to New York; Adams is a Minnesota Vikings player who was injured during this game, not a Giants player.",
    STRIB,"2026-08-15","BEAT REPORT","MEDIUM","NONE",
    "Monitor-layer record correction only. No points, rating, formula or model change proposed.",
    "")
row("2026-08-15","COMPLETE","LA","KC","Away","RESTED","Matthew Stafford / Ty Simpson",
    "QB1 Stafford sat out by plan; rookie Ty Simpson took his first NFL action","None reported",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","KC","LA","Home","RESTED","Patrick Mahomes / Justin Fields",
    "Mahomes held out for ACL/LCL rehab as the HC signalled pre-game; Fields, Nussmeier and Oladokun handled the snaps",
    "Mahomes withheld for rehab management; previously cleared for camp",SBD15,"2026-08-15","MULTI-SOURCE","HIGH","NONE",
    "PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","JAX","NO","Away","RESTED","Trevor Lawrence + all starters",
    "HC held all starters out as stated pre-game; Mullens and Bradley took the snaps","None reported",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","NO","JAX","Home","MIXED","Spencer Rattler / Tyler Shough",
    "Rattler started; workbook baseline QB Tyler Shough did not play. Preseason usage is not a Week 1 declaration, "
    "but the baseline-vs-usage divergence needs verification",
    "DT Bryan Bresee and OL Dillon Radunz were placed on Injured Reserve.",
    SAINTS1+" ; "+SAINTS2,"2026-08-12","OFFICIAL","HIGH","QB VALUES",
    "QB VALUES: NO Source/Notes/Last-update fields; flag baseline-vs-usage divergence for verification. "
    "IR placements recorded in monitor layer only; duration not characterised by the cited sources.",
    "No official statement located on whether NO has changed its Week 1 starter","MONITOR","N")
row("2026-08-15","COMPLETE","PHI","BAL","Away","RESTED","Jalen Hurts",
    "QB1 Hurts rested; Dalton, McKee and Payton handled snaps",
    "Absent: Quinyon Mitchell, Cooper DeJean, Jalen Carter, Jordan Davis, Zack Baun - reasons not reported",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only",
    "Reasons for the five defensive absences UNVERIFIED (rest vs injury not distinguished)")
row("2026-08-15","COMPLETE","BAL","PHI","Home","RESTED","Lamar Jackson / Tyler Huntley",
    "QB1 Lamar Jackson rested; Huntley led the quarterback group","None reported",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","DAL","SEA","Away","RESTED","Dak Prescott",
    "QB1 Prescott rested as the HC signalled pre-game; Howell and Milton III split reps","None reported",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")
row("2026-08-15","COMPLETE","SEA","DAL","Home","LIMITED","Sam Darnold",
    "QB1 Darnold saw limited work; Lock and Milroe took extended snaps","None reported",
    SBD15,"2026-08-15","BEAT REPORT","MEDIUM","NONE","PRESEASON MONITOR log only")

os.makedirs("preseason",exist_ok=True)
with open("preseason/PRESEASON_MONITOR.csv","w",newline="") as f:
    w=csv.writer(f,lineterminator="\n"); w.writerow(HDR); w.writerows(R)
with open("preseason/intake_template.csv","w",newline="") as f:
    csv.writer(f,lineterminator="\n").writerow(HDR)
print(f"rows={len(R)} teams={len(set(r[3] for r in R))}")
