"""Tests for djinn.core.installer using tmp directories."""

import os
import tempfile
from pathlib import Path
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry
from djinn.core.installer import Installer


class TestInstaller:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.config = Config(
            registry_url="__bundled__",
            style="default",
            tailwind={
                "config": "tailwind.config.js",
                "css": "static/css/base.css",
                "cssVariables": True,
            },
            aliases={
                "components": os.path.join(self.tmp, "templates/components"),
                "utils": os.path.join(self.tmp, "templatetags"),
            },
            registries={},
        )
        self.registry = Registry(self.config)
        self.installer = Installer(self.config, self.registry)

    def test_install_button_creates_files(self):
        installed = self.installer.install("button", force=True)
        assert len(installed) > 0

        template_dir = Path(self.config.get_template_path())
        python_dir = Path(self.config.get_python_path())

        assert (template_dir / "button.html").exists()
        assert (python_dir / "djinn_button.py").exists()

    def test_install_without_force_raises_on_existing(self):
        self.installer.install("button", force=True)
        try:
            self.installer.install("button", force=False)
            assert False, "Should have raised FileExistsError"
        except FileExistsError:
            pass

    def test_install_force_overwrites(self):
        self.installer.install("button", force=True)
        installed = self.installer.install("button", force=True)
        assert len(installed) > 0
        assert (Path(self.config.get_template_path()) / "button.html").exists()

    def test_install_nonexistent_raises(self):
        try:
            self.installer.install("does-not-exist", force=True)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_install_records_all_files(self):
        installed = self.installer.install("button", force=True)
        installed_paths = {p for _, p in installed}
        assert Path(self.config.get_template_path(), "button.html") in installed_paths
        assert Path(self.config.get_python_path(), "djinn_button.py") in installed_paths
