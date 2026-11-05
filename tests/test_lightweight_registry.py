"""Tests for the lightweight registry index."""

import json
import os
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry


class TestLightweightIndex:
    def test_index_json_is_lightweight(self):
        """index.json should not contain full component content, just name/path references."""
        index_path = os.path.join(
            os.path.dirname(__file__),
            "..", "djinn", "registry", "index.json",
        )
        with open(index_path, "r") as f:
            data = json.load(f)

        assert "components" in data
        components = data["components"]
        assert len(components) > 0

        # Each entry should be lightweight (no embedded file content)
        for entry in components:
            assert "name" in entry
            assert "path" in entry
            # Should NOT have full file content embedded
            assert "content" not in entry
            assert "files" not in entry

    def test_list_components_lazy_loads(self):
        """list_components should lazy-load from individual registry.json files."""
        config = Config(**DEFAULT_CONFIG.copy())
        registry = Registry(config)
        components = registry.list_components()

        assert len(components) > 0
        names = [c.name for c in components]
        assert "button" in names
        assert "footer" in names
        assert "hero-section" in names

        # Each loaded component should have full data (files with content)
        button = next(c for c in components if c.name == "button")
        assert len(button.files) > 0
        assert button.files[0].get("content", "") != ""

    def test_load_component_from_lightweight_index(self):
        """load_component should work for components listed in lightweight index."""
        config = Config(**DEFAULT_CONFIG.copy())
        registry = Registry(config)

        metadata = registry.load_component("button")
        assert metadata is not None
        assert metadata.name == "button"
        assert len(metadata.files) > 0

        metadata = registry.load_component("footer")
        assert metadata is not None
        assert metadata.name == "footer"

    def test_nonexistent_component_returns_none(self):
        config = Config(**DEFAULT_CONFIG.copy())
        registry = Registry(config)
        assert registry.load_component("does-not-exist") is None
