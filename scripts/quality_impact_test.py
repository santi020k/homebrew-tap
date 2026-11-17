"""Exercise the committed policy using the installed, pinned Quality CLI."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from check_tap import ROOT


class ImpactPolicy(unittest.TestCase):
    def test_committed_selection_and_fallbacks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, env=env, stderr=subprocess.PIPE).decode().strip()
            def plan(base):
                command = [os.environ.get("QUALITY_BINARY", "quality"), "impact", "plan", "--base", base,
                           "--head", "HEAD", "--format", "json"]
                result = json.loads(subprocess.check_output(command, cwd=root, env=env))
                return sorted(node["id"] for node in result["selected"])
            git("init", "-q")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.test")
            shutil.copyfile(ROOT / "quality-impact.json", root / "quality-impact.json")
            git("add", ".")
            git("commit", "-qm", "policy")
            for path, expected in (("Formula/a.rb", ["formulae"]), ("Casks/a.rb", ["casks"]),
                                   ("scripts/change.py", ["casks", "formulae"]),
                                   ("unknown", ["casks", "formulae"])):
                base = git("rev-parse", "HEAD")
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("changed")
                git("add", ".")
                git("commit", "-qm", "change")
                self.assertEqual(plan(base), expected)
            self.assertEqual(plan("unavailable"), ["casks", "formulae"])


if __name__ == "__main__":
    unittest.main()
