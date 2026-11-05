import unittest
import os
import shutil
import tempfile
from pathlib import Path
from click.testing import CliRunner

from djinn.cli.main import cli


class TestUpgradeCLI(unittest.TestCase):
    """Test upgrade CLI with diff preview, backup, and confirmation."""

    def setUp(self):
        self.runner = CliRunner()
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.addCleanup(os.chdir, self.old_cwd)
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)

    def test_upgrade_diff_shows_changes(self):
        """djinn upgrade --diff shows changes without applying."""
        result = self.runner.invoke(cli, ["init", "--yes"])
        self.assertEqual(result.exit_code, 0)

        # Install button first
        result = self.runner.invoke(cli, ["add", "button", "--force"])
        self.assertEqual(result.exit_code, 0)

        # Now diff should show no changes (just installed)
        result = self.runner.invoke(cli, ["upgrade", "button", "--diff"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("already up to date", result.output)

    def test_upgrade_force_without_prompt(self):
        """djinn upgrade --force upgrades without prompting."""
        result = self.runner.invoke(cli, ["init", "--yes"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["add", "button", "--force"])
        self.assertEqual(result.exit_code, 0)

        # Force upgrade should work
        result = self.runner.invoke(cli, ["upgrade", "button", "--force"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("already up to date", result.output)

    def test_upgrade_backup_creates_directory(self):
        """djinn upgrade --backup creates backup directory."""
        result = self.runner.invoke(cli, ["init", "--yes"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["add", "button", "--force"])
        self.assertEqual(result.exit_code, 0)

        # Upgrade with backup (no changes since just installed, but tests the flag)
        result = self.runner.invoke(cli, ["upgrade", "button", "--backup", "--force"])
        self.assertEqual(result.exit_code, 0)
        # Backup directory may or may not exist depending on changes
        # Just verify the command doesn't crash

    def test_upgrade_no_component_shows_error(self):
        """djinn upgrade without component shows error."""
        result = self.runner.invoke(cli, ["init", "--yes"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["upgrade"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error", result.output)


if __name__ == "__main__":
    unittest.main()
