#!/usr/bin/env python3
"""Link check for preseason/PRESEASON_MONITOR.csv source URLs.
Format/host validation always enforced; network reachability is best-effort (proxy-tolerant)."""
import csv, re, sys, urllib.request, urllib.error, collections
PATH="preseason/PRESEASON_MONITOR.csv"
ALLOW={"www.nfl.com","www.vikings.com","www.covers.com","sports.yahoo.com","www.sportsbettingdime.com",
       "www.joxfm.com","www.cbssports.com","www.si.com","www.foxsports.com","www.espn.com","www.startribune.com"}
def main():
    rows=list(csv.DictReader(open(PATH)))
    errs=[]; urls=collections.Counter()
    for i,r in enumerate(rows,2):
        u=r["Source URL"]; urls[u]+=1
        m=re.match(r"^https://([^/]+)/", u+"/")
        if not m: errs.append(f"r{i}: malformed URL {u}"); continue
        if m.group(1) not in ALLOW: errs.append(f"r{i}: host not in source-priority allowlist: {m.group(1)}")
    if errs:
        print("LINKCHECK: FAIL"); [print("  -",e) for e in errs]; return 1
    print(f"LINKCHECK: PASS (format+host) — {len(rows)} rows, {len(urls)} distinct URLs, all hosts in allowlist")
    # best-effort reachability
    unreachable=[]
    for u in urls:
        try:
            req=urllib.request.Request(u, method="HEAD", headers={"User-Agent":"ttw-linkcheck"})
            urllib.request.urlopen(req, timeout=6)
        except Exception as e:
            unreachable.append((u, type(e).__name__))
    if unreachable:
        print(f"LINKCHECK NETWORK: {len(unreachable)}/{len(urls)} not confirmed reachable (WARN, non-blocking):")
        for u,e in unreachable[:12]: print(f"  ~ {e}: {u}")
    else:
        print("LINKCHECK NETWORK: all URLs reachable")
    return 0
if __name__=="__main__": sys.exit(main())
