"""Tests for djinn.core.registry using the bundled registry."""

from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry, ComponentMetadata


class TestRegistry:
    def setup_method(self):
        self.config = Config(**DEFAULT_CONFIG.copy())
        self.registry = Registry(self.config)

    def test_load_existing_component(self):
        metadata = self.registry.load_component("button")
        assert metadata is not None
        assert isinstance(metadata, ComponentMetadata)
        assert metadata.name == "button"
        assert metadata.type == "components:ui"
        assert len(metadata.files) > 0

    def test_load_nonexistent_component_returns_none(self):
        metadata = self.registry.load_component("does-not-exist")
        assert metadata is None

    def test_component_files_have_content(self):
        metadata = self.registry.load_component("button")
        for file_obj in metadata.files:
            assert "name" in file_obj
            assert "content" in file_obj
            assert "dir" in file_obj

    def test_list_components_returns_list(self):
        components = self.registry.list_components()
        assert isinstance(components, list)
        assert len(components) > 0
        names = [c.name for c in components]
        assert "button" in names

    def test_list_components_includes_types(self):
        components = self.registry.list_components()
        for c in components:
            assert c.type == "components:ui"

    def test_bundled_path_resolution(self):
        path = self.registry._resolve_bundled_path()
        assert path is not None
        assert path.exists()
