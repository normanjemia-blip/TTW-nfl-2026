#!/usr/bin/env python3
"""Repo-local regression suite (stdlib only). Run: python3 tests/run_tests.py"""
import unittest, subprocess, csv, hashlib, os, sys, glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
AUTH="TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx"
AUTH_SHA="79923992e9cfe156af47207b1756010af9a375592997be8e194bc75e4e9d313f"

def sh(cmd): return subprocess.run(cmd,shell=True,capture_output=True,text=True)

class Gates(unittest.TestCase):
    def test_gate_suite_passes(self):
        r=sh("python3 scripts/run_gates.py"); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
    def test_validator_passes(self):
        r=sh("python3 scripts/validate_preseason_monitor.py"); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
    def test_linkcheck_passes(self):
        r=sh("python3 scripts/linkcheck_preseason.py"); self.assertEqual(r.returncode,0,r.stdout+r.stderr)

class Authoritative(unittest.TestCase):
    def test_authoritative_workbook_unmodified(self):
        self.assertEqual(hashlib.sha256(open(AUTH,'rb').read()).hexdigest(),AUTH_SHA,
                         "AUTHORITATIVE workbook must not be modified")
    def test_no_new_spreadsheet_added(self):
        allowed={"TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx","TTW_NFL_v1_1_1 Version 2.xlsx",
                 "TTW_NFL_Power_Ratings_2026_v1.2_QB_WORKING.xlsx","TTW_NFL_Power_Ratings_2026_v1.2.1_QB_CANDIDATE.xlsx",
                 "TTW_NFL_Power_Ratings_2026_v1.2.2_QB_SWEEP_CANDIDATE.xlsx","TTW_NFL_Power_Ratings_2026_v1.3_MARKET_CANDIDATE.xlsx"}
        found={os.path.basename(p) for p in glob.glob("**/*.xls*",recursive=True)}
        self.assertEqual(found-allowed,set(),"no spreadsheet file may be added to the repository")

class Monitor(unittest.TestCase):
    def setUp(self): self.rows=list(csv.DictReader(open("preseason/PRESEASON_MONITOR.csv")))
    def test_32_team_game_rows(self):
        self.assertEqual(len(self.rows),32); self.assertEqual(len({r["Team"] for r in self.rows}),32)
    def test_current_tracking_state(self):
        expected={"MIN":("UPDATE","Y"),"CLE":("UPDATE","Y"),"NO":("UPDATE","Y"),"WAS":("MONITOR","N"),"CHI":("MONITOR","N")}
        for r in self.rows:
            got=(r["Decision"],r["Workbook Updated?"])
            self.assertEqual(got, expected.get(r["Team"],("PENDING","N")), r["Team"])
    def test_decision_updated_lifecycle_consistency(self):
        for r in self.rows:
            d,u=r["Decision"],r["Workbook Updated?"]
            self.assertIn(d,{"PENDING","MONITOR","UPDATE","IGNORE"},r["Team"])
            self.assertIn(u,{"Y","N"},r["Team"])
            if d in {"PENDING","MONITOR","IGNORE"}:
                self.assertEqual(u,"N",f"{r['Team']}: {d} must have N")
            self.assertFalse(d=="PENDING" and u=="Y",f"{r['Team']}: PENDING/Y forbidden")
    def test_unplayed_games_are_tbd(self):
        for r in self.rows:
            if r["Game Status"]=="NOT PLAYED": self.assertEqual(r["Starter Use"],"TBD",r["Team"])
    def test_complete_tbd_rows_have_blockers(self):
        for r in self.rows:
            if r["Game Status"]=="COMPLETE" and r["Starter Use"]=="TBD":
                self.assertTrue(r["Blocker"].strip(),f"{r['Team']}: COMPLETE+TBD needs a named blocker")
    def test_all_16_games_present(self):
        games={tuple(sorted([r["Team"],r["Opponent"]])) for r in self.rows}
        self.assertEqual(len(games),16,"expected 16 distinct games")
    def test_no_point_values_in_proposals(self):
        import re
        for r in self.rows:
            self.assertIsNone(re.search(r"[+-]?\d+(\.\d+)?\s*(pt|point)",r["Proposed Change"],re.I),r["Team"])

class LinkcheckMultiURL(unittest.TestCase):
    """Source URL may hold several URLs separated by ' ; '. Every one must be validated."""
    def setUp(self):
        sys.path.insert(0,os.path.join(ROOT,"scripts"))
        import linkcheck_preseason as L; self.L=L
    def test_multi_url_field_splits_into_both_urls(self):
        f="https://www.vikings.com/a ; https://www.neworleanssaints.com/b"
        self.assertEqual(self.L.split_source_urls(f),
                         ["https://www.vikings.com/a","https://www.neworleanssaints.com/b"])
    def test_both_urls_in_valid_multi_field_are_checked(self):
        for u in self.L.split_source_urls("https://www.vikings.com/a ; https://www.nfl.com/b"):
            self.assertTrue(self.L.check_url(u)[0], u)
    def test_non_allowlisted_second_url_is_detected(self):
        parts=self.L.split_source_urls("https://www.nfl.com/a ; https://evil.example.com/b")
        self.assertTrue(self.L.check_url(parts[0])[0])
        ok,host,reason=self.L.check_url(parts[1])
        self.assertFalse(ok); self.assertEqual(host,"evil.example.com"); self.assertIn("allowlist",reason)
    def test_invalid_second_url_is_detected(self):
        parts=self.L.split_source_urls("https://www.nfl.com/a ; http://www.nfl.com/b")
        ok,_h,reason=self.L.check_url(parts[1])
        self.assertFalse(ok); self.assertIn("non-HTTPS", reason)
    def test_single_url_behaviour_preserved(self):
        f="https://www.nfl.com/news/x"
        self.assertEqual(self.L.split_source_urls(f),[f])
        self.assertTrue(self.L.check_url(f)[0])
    def test_joined_field_is_never_treated_as_one_url(self):
        joined="https://www.nfl.com/a ; https://www.vikings.com/b"
        self.assertFalse(self.L.check_url(joined)[0])          # combined string is not a valid URL
        self.assertEqual(len(self.L.split_source_urls(joined)),2)

class DQGuardPatch(unittest.TestCase):
    """Proves the PROPOSED CALC guard semantics. No workbook is modified."""
    @staticmethod
    def guarded_mean(vals):
        nums=[v for v in vals if isinstance(v,(int,float))]
        return "" if len(nums)==0 else round(sum(nums)/len(nums),6)
    def test_empty_range_yields_blank_not_div0(self):
        self.assertEqual(self.guarded_mean(["","","" ]),"")
    def test_populated_range_matches_average(self):
        self.assertEqual(self.guarded_mean([1.0,2.0,3.0]),2.0)
    def test_mixed_ignores_text_blanks(self):
        self.assertEqual(self.guarded_mean(["",2.0,"",4.0]),3.0)
    def test_guard_preserves_nonzero_signal(self):
        self.assertNotEqual(self.guarded_mean([0.5,0.5]),"")

if __name__=="__main__":
    unittest.main(verbosity=2)
