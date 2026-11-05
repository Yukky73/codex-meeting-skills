"""Isolated installer checks; no app connections or workspace credentials are used."""
import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("meeting_installer", Path(__file__).with_name("install.py"))
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)
SOURCE = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.workspace = self.root / "営業 チーム 日本語"
        self.workspace.mkdir()
        self.target = self.workspace / ".agents" / "skills"

    def run_install(self, *options):
        output = io.StringIO()
        with patch.object(sys, "argv", ["install.py", "--workspace", str(self.workspace), *options]):
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = INSTALLER.main()
        return result, output.getvalue()

    def test_dry_run_has_no_side_effects(self):
        result, output = self.run_install("--dry-run")
        self.assertEqual(result, 0)
        self.assertIn("Would copy", output)
        self.assertFalse((self.workspace / ".agents").exists())

    def test_default_copy_works_when_symlinks_are_forbidden(self):
        with patch.object(Path, "symlink_to", side_effect=OSError(1314, "Privilege not held")):
            self.assertEqual(self.run_install()[0], 0)
        self.assertEqual(len(list(self.target.iterdir())), 6)
        for name in INSTALLER.NAMES:
            self.assertFalse((self.target / name).is_symlink())
            self.assertEqual(INSTALLER.contents(self.target / name), INSTALLER.contents(SOURCE / "skills" / name))
        config = self.target / "meeting-run-followup/references/configuration.md"
        self.assertTrue((config.parent / "../../meeting-create-minutes/assets/meeting-minutes-template.md").resolve().is_file())

    def test_repeat_preserves_local_config_and_skills(self):
        config = self.workspace / ".meeting-skills.local.md"
        config.write_text("private local settings", encoding="utf-8")
        self.assertEqual(self.run_install()[0], 0)
        before = INSTALLER.contents(self.target)
        self.assertEqual(self.run_install()[0], 0)
        self.assertEqual(before, INSTALLER.contents(self.target))
        self.assertEqual(config.read_text(encoding="utf-8"), "private local settings")

    def test_conflict_preflight_does_not_install_or_overwrite(self):
        existing = self.target / INSTALLER.NAMES[-1]
        existing.mkdir(parents=True)
        (existing / "user.md").write_text("keep", encoding="utf-8")
        result, output = self.run_install()
        self.assertEqual(result, 1)
        self.assertIn("will not be replaced", output)
        self.assertEqual([p.name for p in self.target.iterdir()], [existing.name])
        self.assertEqual((existing / "user.md").read_text(encoding="utf-8"), "keep")

    def test_link_denial_is_actionable_and_installs_no_partial_skill(self):
        with patch.object(Path, "symlink_to", side_effect=OSError(1314, "Privilege not held")):
            result, output = self.run_install("--mode", "link")
        self.assertEqual(result, 1)
        self.assertIn("--mode copy", output)
        self.assertNotIn("Traceback", output)
        self.assertFalse(list(self.target.iterdir()))

    def test_source_can_move_after_copy(self):
        checkout = self.root / "配布 元"
        shutil.copytree(SOURCE, checkout)
        with patch.object(INSTALLER, "__file__", str(checkout / "scripts/install.py")):
            self.assertEqual(self.run_install()[0], 0)
        shutil.rmtree(checkout)
        for name in INSTALLER.NAMES:
            self.assertTrue((self.target / name / "SKILL.md").is_file())
        self.assertTrue((self.target / "meeting-create-minutes/assets/meeting-minutes-template.md").is_file())

    def test_optional_links_remain_compatible(self):
        try:
            probe = self.root / "probe"
            probe.symlink_to(self.workspace, target_is_directory=True)
            probe.unlink()
        except OSError:
            self.skipTest("Link privilege unavailable on this machine")
        self.assertEqual(self.run_install("--mode", "link")[0], 0)
        self.assertTrue(all((self.target / name).is_symlink() for name in INSTALLER.NAMES))
        self.assertEqual(self.run_install()[0], 0)


if __name__ == "__main__":
    unittest.main()
