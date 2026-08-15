#!/usr/bin/env python3
"""Repo-local regression suite (stdlib only). Run: python3 tests/run_tests.py"""
import unittest, subprocess, csv, hashlib, os, sys, glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
AUTH="TTW_NFL_Power_Ratings_2026_v1.1_AUTHORITATIVE.xlsx"
AUTH_SHA="674510507fa784f0926a348b81068cc731e082b992fa9a0fc42d3957e75b6b5f"

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
    def test_all_decisions_pending_and_unwritten(self):
        for r in self.rows:
            self.assertEqual(r["Decision"],"PENDING",r["Team"])
            self.assertEqual(r["Workbook Updated?"],"N",r["Team"])
    def test_unplayed_games_are_tbd(self):
        for r in self.rows:
            if r["Game Status"]=="NOT PLAYED": self.assertEqual(r["Starter Use"],"TBD",r["Team"])
    def test_no_point_values_in_proposals(self):
        import re
        for r in self.rows:
            self.assertIsNone(re.search(r"[+-]?\d+(\.\d+)?\s*(pt|point)",r["Proposed Change"],re.I),r["Team"])

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
