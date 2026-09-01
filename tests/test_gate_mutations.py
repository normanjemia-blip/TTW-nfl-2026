#!/usr/bin/env python3
"""Mutation tests for the re-pinned v1.4 gate suite.

Each test corrupts a throwaway copy of the authoritative workbook back toward a v1.1-era
regression, points run_gates.py at it, and asserts the suite FAILS with a diagnostic
naming the specific regression. A gate that cannot fail is not a gate.

The real authoritative workbook is never modified: every mutation happens on a temp copy
and run_gates.py is invoked with its module-level target monkeypatched via a shim.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH = os.path.join(ROOT, "TTW_NFL_Power_Ratings_2026_v1.4_AUTHORITATIVE.xlsx")

PRESEASON = "xl/worksheets/sheet17.xml"
TEAM_RATINGS = "xl/worksheets/sheet8.xml"
SETTINGS = "xl/worksheets/sheet10.xml"
SHARED = "xl/sharedStrings.xml"

D_OLD = ('IFERROR(ROUND(INDEX(CalcGoverned,MATCH($A{r},CalcTeams,0)),2),&quot;&quot;)')
D_NEW = ('IFERROR(IF(ISNUMBER(INDEX(CalcGoverned,MATCH($A{r},CalcTeams,0))),'
         'ROUND(INDEX(CalcGoverned,MATCH($A{r},CalcTeams,0)),2),&quot;&quot;),&quot;&quot;)')


def mutate(dst, edits):
    """Copy AUTH to dst applying {part: fn(xml)->xml}."""
    zin = zipfile.ZipFile(AUTH)
    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename in edits:
            data = edits[info.filename](data.decode("utf-8")).encode("utf-8")
        zout.writestr(info, data)
    zout.close()
    zin.close()


def run_gates_on(path):
    """Run run_gates.py against `path` without touching the real workbook."""
    shim = ("import runpy,sys,os\n"
            "sys.path.insert(0,%r)\n"
            "import run_gates\n"
            "run_gates.A=%r\n"
            "sys.exit(run_gates.main())\n" % (os.path.join(ROOT, "scripts"), path))
    return subprocess.run([sys.executable, "-c", shim], cwd=ROOT,
                          capture_output=True, text=True)


class GateMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _assert_fails(self, path, needle):
        r = run_gates_on(path)
        self.assertEqual(r.returncode, 1, "gate suite should FAIL but passed:\n" + r.stdout)
        self.assertIn("GATE SUITE: FAIL", r.stdout)
        self.assertRegex(r.stdout, needle, "failure did not name the regression:\n" + r.stdout)

    def test_unmutated_workbook_passes(self):
        r = run_gates_on(AUTH)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("GATE SUITE: PASS", r.stdout)

    def test_v11_banner_fails(self):
        p = os.path.join(self.tmp, "banner.xlsx")
        mutate(p, {SHARED: lambda x: x.replace(
            "TO THE WINDOW — NFL POWER RATINGS 2026 (v1.4)",
            "TO THE WINDOW — NFL POWER RATINGS 2026 (v1.1)")})
        self._assert_fails(p, r"banner is not v1\.4")

    def test_blank_source_b_fails(self):
        """Clear PRESEASON I5:I36 -> Source B population gate must fail."""
        def strip(x):
            for r in range(5, 37):
                x = re.sub(r'<c r="I%d"[^>]*>.*?</c>' % r, '<c r="I%d" s="12"/>' % r, x,
                           count=1, flags=re.S)
            return x
        p = os.path.join(self.tmp, "blank_srcb.xlsx")
        mutate(p, {PRESEASON: strip})
        self._assert_fails(p, r"Source B populated 0/32")

    def test_old_coercing_formula_fails(self):
        """Restore the pre-fix D formula -> the fix gate must fail and say so."""
        def revert(x):
            for r in range(5, 37):
                x = x.replace(D_NEW.format(r=r), D_OLD.format(r=r))
            return x
        p = os.path.join(self.tmp, "old_formula.xlsx")
        mutate(p, {TEAM_RATINGS: revert})
        self._assert_fails(p, r"not the ISNUMBER-protected formula.*old coercing form")

    def test_stale_asof_date_fails(self):
        p = os.path.join(self.tmp, "asof.xlsx")
        mutate(p, {SETTINGS: lambda x: re.sub(
            r'(<c r="B7"[^>]*>)<v>[^<]*</v>', r'\g<1><v>46216</v>', x, count=1)})
        self._assert_fails(p, r"as-of date is .*expected 2026-09-01")

    def test_changed_ats_threshold_fails(self):
        p = os.path.join(self.tmp, "ats.xlsx")
        mutate(p, {SETTINGS: lambda x: re.sub(
            r'(<c r="B26"[^>]*>)<v>1\.5</v>', r'\g<1><v>3.0</v>', x, count=1)})
        self._assert_fails(p, r"ATS thresholds drifted")

    def test_changed_source_weight_fails(self):
        p = os.path.join(self.tmp, "weight.xlsx")
        mutate(p, {PRESEASON: lambda x: re.sub(
            r'(<c r="M5"[^>]*>)<v>0\.35</v>', r'\g<1><v>0.3</v>', x, count=1)})
        self._assert_fails(p, r"source weights drifted")

    def test_populated_source_c_fails(self):
        p = os.path.join(self.tmp, "srcc.xlsx")
        mutate(p, {PRESEASON: lambda x: re.sub(
            r'<c r="N5"[^>]*?/>', '<c r="N5" s="12"><v>9.5</v></c>', x, count=1)})
        self._assert_fails(p, r"Source C must remain blank")

    def test_bet_labels_off_fails(self):
        """SETTINGS B67 is a shared-string reference, so flip the cell to an inline
        string rather than editing the shared table (which other cells may share)."""
        p = os.path.join(self.tmp, "bet.xlsx")
        mutate(p, {SETTINGS: lambda x: re.sub(
            r'<c r="B67"[^>]*?t="s"><v>\d+</v></c>',
            '<c r="B67" s="32" t="inlineStr"><is><t>N</t></is></c>', x, count=1)})
        self._assert_fails(p, r"BET labels must be Y at v1\.4")

    def test_real_authoritative_workbook_untouched_by_mutations(self):
        r = run_gates_on(AUTH)
        self.assertEqual(r.returncode, 0, "mutations must never touch the real workbook")


if __name__ == "__main__":
    unittest.main(verbosity=2)
