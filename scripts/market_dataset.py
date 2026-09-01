#!/usr/bin/env python3
"""Week 1 2026 market lines — DraftKings OPENING lines (schedule release), as of 2026-05-15.
Source: FOX Sports "2026 NFL Odds Week 1" (explicitly 'as of May 15, DraftKings'), corroborated by
ESPN schedule-release odds, DK Network (2026-05-14), RotoWire.
NOT current lines. Recorded with true source + line date so the workbook's STALE rule fires.
Sign convention per sheet instructions: Favorite team code + spread as a POSITIVE number."""

LINE_DATE="2026-05-15"
SOURCE="DraftKings OPENING (schedule release) via FOX Sports, as of 2026-05-15"
NOTE=("OPENING line, NOT current — refresh with Novig before any live use. "
      "Stale by workbook rule (AsOfDate 2026-07-13 vs line date 2026-05-15).")

# row, away, home, favorite, spread(+), total
WEEK1=[
 (5, "NE","SEA","SEA",3.5,44.5),
 (6, "SF","LA", "LA", 2.5,48.5),
 (7, "CHI","CAR","CHI",2.5,44.5),
 (8, "TB","CIN","CIN",3.5,50.5),
 (9, "NO","DET","DET",7.0,48.5),
 (10,"BUF","HOU","BUF",1.5,45.5),
 (11,"BAL","IND","BAL",3.5,49.5),
 (12,"CLE","JAX","JAX",7.0,40.5),
 (13,"ATL","PIT","PIT",3.0,42.5),
 (14,"NYJ","TEN","TEN",3.0,39.5),
 (15,"ARI","LAC","LAC",11.5,45.5),
 (16,"MIA","LV", "LV", 3.0,41.5),
 (17,"GB","MIN","GB", 1.5,44.5),
 (18,"WAS","PHI","PHI",5.5,46.5),
 (19,"DAL","NYG","DAL",2.5,48.5),
 (20,"DEN","KC", "KC", 2.5,42.5),
]

# Cross-source divergence recorded for the audit (FanDuel undated lookahead set)
FANDUEL_DIVERGENCE={
 "SF@LA":  ("LA -3.5 / 48.5",  "DK LA -2.5 / 48.5"),
 "NO@DET": ("DET -6.5 / 49.5", "DK DET -7 / 48.5"),
 "NYJ@TEN":("TEN -2.5 / 38.5", "DK TEN -3 / 39.5"),
 "ATL@PIT":("PIT -2.5 / 41.5", "DK PIT -3 / 42.5"),
 "CLE@JAX":("JAX -7.5 / 40.5", "DK JAX -7 / 40.5"),
 "BAL@IND":("BAL -3.5 / 48.5", "DK BAL -3.5 / 49.5"),
 "BUF@HOU":("BUF -1.5 / 44.5", "DK BUF -1.5 / 45.5"),
 "CHI@CAR":("CHI -2.5 / 45.5", "DK CHI -2.5 / 44.5"),
 "TB@CIN": ("CIN -3.5 / 51.5", "DK CIN -3.5 / 50.5"),
 "ARI@LAC":("LAC -10.5 / 46.5","DK LAC -11.5 / 45.5"),
 "MIA@LV": ("MIA -3.5 / 40.5 (SIDE FLIP)", "DK LV -3 / 41.5"),
 "WAS@PHI":("PHI -4.5 / 47.5", "DK PHI -5.5 / 46.5"),
 "DEN@KC": ("KC -2.5 / 43.5",  "DK KC -2.5 / 42.5"),
}
AGREE=["NE@SEA","GB@MIN","DAL@NYG"]

if __name__=="__main__":
    assert len(WEEK1)==16
    for (r,a,h,f,s,t) in WEEK1:
        assert f in (a,h), f"favorite {f} not in game {a}@{h}"
        assert s>0 and t>0
    print("16 games validated; favorite always in game; spreads positive.")
