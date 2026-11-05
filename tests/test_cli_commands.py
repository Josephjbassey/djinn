"""Tests for the upgrade, remove, and doctor CLI commands."""

import os
import tempfile
from click.testing import CliRunner
from djinn.cli.commands.upgrade import upgrade
from djinn.cli.commands.remove import remove
from djinn.cli.commands.doctor import doctor
from djinn.cli.main import cli


class TestUpgradeCommand:
    def test_upgrade_up_to_date(self, tmp_path, monkeypatch):
        """upgrade should report component is up to date when files match."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        # Init and add button
        result = runner.invoke(cli, ["init", "--defaults", "--force"])
        assert result.exit_code == 0

        result = runner.invoke(cli, ["add", "button", "--force"])
        assert result.exit_code == 0

        # Upgrade should say up to date
        result = runner.invoke(cli, ["upgrade", "button"])
        assert result.exit_code == 0
        assert "already up to date" in result.output

    def test_upgrade_nonexistent(self, tmp_path, monkeypatch):
        """upgrade should error on nonexistent component."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(cli, ["init", "--defaults", "--force"])
        assert result.exit_code == 0

        result = runner.invoke(cli, ["upgrade", "does-not-exist"])
        assert result.exit_code == 0
        assert "not found" in result.output


class TestRemoveCommand:
    def test_remove_with_force(self, tmp_path, monkeypatch):
        """remove --force should delete installed files."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(cli, ["init", "--defaults", "--force"])
        assert result.exit_code == 0

        result = runner.invoke(cli, ["add", "modal", "--force"])
        assert result.exit_code == 0

        # Verify files exist
        template_dir = tmp_path / "templates" / "components"
        python_dir = tmp_path / "theme" / "templatetags"
        assert (template_dir / "modal.html").exists()
        assert (python_dir / "djinn_modal.py").exists()

        # Remove with --force
        result = runner.invoke(cli, ["remove", "modal", "--force"])
        assert result.exit_code == 0
        assert "Removed:" in result.output

        # Verify files are gone
        assert not (template_dir / "modal.html").exists()
        assert not (python_dir / "djinn_modal.py").exists()

    def test_remove_nonexistent(self, tmp_path, monkeypatch):
        """remove should error on nonexistent component."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(cli, ["init", "--defaults", "--force"])
        assert result.exit_code == 0

        result = runner.invoke(cli, ["remove", "does-not-exist"])
        assert result.exit_code == 0
        assert "not found" in result.output


class TestDoctorCommand:
    def test_doctor_not_initialized(self, tmp_path, monkeypatch):
        """doctor should error when not initialized."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(cli, ["doctor"])
        assert result.exit_code != 0
        assert "not initialized" in result.output

    def test_doctor_initialized(self, tmp_path, monkeypatch):
        """doctor should report status for initialized project."""
        monkeypatch.chdir(tmp_path)
        runner = CliRunner()

        result = runner.invoke(cli, ["init", "--defaults", "--force"])
        assert result.exit_code == 0

        result = runner.invoke(cli, ["doctor"])
        assert result.exit_code == 0
        assert "Djinn Project Health Check" in result.output
        assert "PASS" in result.output or "FAIL" in result.output
