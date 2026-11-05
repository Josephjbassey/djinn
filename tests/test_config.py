"""Tests for djinn.core.config"""

import json
import os
import tempfile
from djinn.core.config import Config, DEFAULT_CONFIG, CONFIG_FILE


class TestConfigDefaults:
    def test_default_config_values(self):
        config = Config(**DEFAULT_CONFIG.copy())
        assert config.registry_url == "__bundled__"
        assert config.style == "default"
        assert config.tailwind["config"] == "tailwind.config.js"
        assert config.tailwind["css"] == "static/css/base.css"
        assert config.tailwind["cssVariables"] is True
        assert config.aliases["components"] == "templates/components"
        assert config.aliases["utils"] == "theme/templatetags"

    def test_get_template_path_returns_path(self):
        config = Config(**DEFAULT_CONFIG.copy())
        path = config.get_template_path()
        assert isinstance(path, __import__("pathlib").Path)
        assert str(path) == "templates/components"

    def test_get_python_path_returns_path(self):
        config = Config(**DEFAULT_CONFIG.copy())
        path = config.get_python_path()
        assert isinstance(path, __import__("pathlib").Path)
        assert str(path) == "theme/templatetags"


class TestConfigLoadSave:
    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = Config(
            registry_url="https://example.com/registry",
            style="dark",
            tailwind={"config": "tailwind.config.js", "css": "static/css/base.css", "cssVariables": False},
            aliases={"components": "my_components", "utils": "my_templatetags"},
            registries={},
        )
        config.save()
        assert os.path.exists(CONFIG_FILE)

        loaded = Config.load()
        assert loaded is not None
        assert loaded.registry_url == "https://example.com/registry"
        assert loaded.style == "dark"
        assert loaded.tailwind["cssVariables"] is False
        assert loaded.aliases["components"] == "my_components"

    def test_load_returns_none_when_missing(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert Config.load() is None

    def test_load_returns_none_on_corrupt_json(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        with open(CONFIG_FILE, "w") as f:
            f.write("{not valid json")
        assert Config.load() is None

    def test_init_creates_config_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = Config.init()
        assert os.path.exists(CONFIG_FILE)
        loaded = Config.load()
        assert loaded.registry_url == "__bundled__"

