import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from check_tap import ROOT, check, select, validate_identity


class TapChecks(unittest.TestCase):
    def test_current_identities(self):
        for path in (ROOT / "Formula").glob("*.rb"):
            validate_identity(path.read_text())
        for path in (ROOT / "Casks").glob("*.rb"):
            validate_identity(path.read_text())

    def test_untrusted_identity(self):
        text = (ROOT / "Casks/coolstead.rb").read_text()
        for bad in (text.replace('sha256 "7', 'sha256 "x'),
                    text.replace("https://github.com", "http://github.com"),
                    text.replace("santi020k/", "untrusted/"),
                    text.replace("v#{version}", "latest"),
                    text.replace('version "1.2.0"', 'version "latest"'),
                    text.replace('Coolstead-#{version}.dmg', 'Coolstead-1.0.0.dmg')):
            with self.subTest(source=bad[:30]), self.assertRaises(ValueError):
                validate_identity(bad)

    def test_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, env=env, stderr=subprocess.PIPE).decode().strip()
            git("init", "-q")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.test")
            for path in ("Formula/a.rb", "Casks/b.rb", "README.md"):
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("initial")
            git("add", ".")
            git("commit", "-qm", "initial")
            base = git("rev-parse", "HEAD")
            (root / "README.md").write_text("documentation")
            git("add", ".")
            git("commit", "-qm", "docs")
            self.assertEqual(select(root, base), [])
            (root / "Formula/a.rb").write_text("updated")
            git("add", ".")
            git("commit", "-qm", "formula")
            self.assertEqual(select(root, base), ["Formula/a.rb"])
            self.assertEqual(select(root, "missing"), ["Casks/b.rb", "Formula/a.rb"])
            git("mv", "Formula/a.rb", "Formula/renamed.rb")
            git("commit", "-qm", "rename")
            self.assertEqual(select(root, base), ["Casks/b.rb", "Formula/renamed.rb"])
            base = git("rev-parse", "HEAD")
            (root / "unknown").write_text("unknown")
            git("add", ".")
            git("commit", "-qm", "unknown")
            self.assertEqual(select(root, base), ["Casks/b.rb", "Formula/renamed.rb"])

    def test_gate_rejects_selected_skips_and_failures(self):
        workflow = (ROOT / ".github/workflows/quality.yml").read_text()
        script = workflow.split("          for result in ")[-1]
        script = "for result in " + script
        for value in ("success", "failure", "cancelled", "skipped", ""):
            for name in ("PACKAGING", "IMPACT"):
                env = {**os.environ, "PACKAGING": "success", "IMPACT": "success", name: value}
                result = subprocess.run(["bash", "-e", "-c", script], env=env, capture_output=True)
                self.assertEqual(result.returncode == 0, value == "success")

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "link.rb").symlink_to(ROOT / "Casks/coolstead.rb")
            with self.assertRaises(ValueError):
                check(root, "link.rb")


if __name__ == "__main__":
    unittest.main()
