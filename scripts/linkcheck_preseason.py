#!/usr/bin/env python3
"""Link check for preseason/PRESEASON_MONITOR.csv source URLs.

Source URL may hold one or more URLs separated by ' ; '. Every individual URL is
validated for absolute-HTTPS syntax and permitted hostname; the combined field is
never passed to the network request function. Format/host validation is always
enforced; network reachability is best-effort (proxy-tolerant) and warns only.
"""
import csv, re, sys, urllib.request, urllib.error, collections
PATH="preseason/PRESEASON_MONITOR.csv"
ALLOW={"www.nfl.com","www.vikings.com","www.covers.com","sports.yahoo.com","www.sportsbettingdime.com",
       "www.joxfm.com","www.cbssports.com","www.si.com","www.foxsports.com","www.espn.com","www.startribune.com","www.neworleanssaints.com"}

def split_source_urls(field):
    """Split a Source URL field into individual URLs on ';', stripping whitespace."""
    return [u.strip() for u in (field or "").split(";") if u.strip()]

def check_url(u):
    """Return (ok, host_or_None, reason_or_None) for one individual URL."""
    m=re.match(r"^https://([^/\s;]+)(/[^\s;]*)?$", u)   # no whitespace/';' — a joined field can never match
    if not m: return (False, None, f"malformed or non-HTTPS absolute URL: {u}")
    host=m.group(1)
    if host not in ALLOW: return (False, host, f"host not in source-priority allowlist: {host} ({u})")
    return (True, host, None)

def main():
    rows=list(csv.DictReader(open(PATH)))
    errs=[]; urls=collections.Counter()
    for i,r in enumerate(rows,2):
        team=r.get("Team","?")
        parts=split_source_urls(r["Source URL"])
        if not parts:
            errs.append(f"r{i} {team}: empty Source URL"); continue
        for u in parts:
            urls[u]+=1
            ok,_host,reason=check_url(u)
            if not ok: errs.append(f"r{i} {team}: {reason}")
    if errs:
        print("LINKCHECK: FAIL"); [print("  -",e) for e in errs]; return 1
    print(f"LINKCHECK: PASS (format+host) — {len(rows)} rows, {len(urls)} distinct URLs, all hosts in allowlist")
    unreachable=[]
    for u in urls:                                  # individual URLs only, never a joined field
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
