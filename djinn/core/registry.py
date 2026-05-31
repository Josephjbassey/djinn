import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import importlib.resources

class ComponentMetadata:
    def __init__(self, name: str, version: str, files: Dict[str, str], install: Dict[str, str]):
        self.name = name
        self.version = version
        self.files = files
        self.install = install

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComponentMetadata':
        return cls(
            name=data["name"],
            version=data["version"],
            files=data["files"],
            install=data.get("install", {})
        )

class Registry:
    def __init__(self, registry_path: str):
        path = Path(registry_path)

        # If registry_path is "__bundled__" or doesn't exist locally, try bundled
        if registry_path == "__bundled__" or not (path / "components").exists():
            try:
                # Resolve bundled registry path
                bundled_res = importlib.resources.files('djinn') / 'registry'
                # Check if it actually exists in the package
                if bundled_res.joinpath('components').exists():
                    # In some environments, we need to convert to a concrete Path
                    # importlib.resources.as_file can handle zip-extracted files
                    with importlib.resources.as_file(bundled_res) as p:
                        # Note: 'as_file' is a context manager, but if it's already a physical path,
                        # it just returns it. For CLI tools, we usually have physical paths.
                        path = Path(p)
            except (ImportError, TypeError, FileNotFoundError):
                pass

        self.registry_path = path

    def get_component_path(self, component_name: str) -> Path:
        return self.registry_path / "components" / component_name

    def load_component(self, component_name: str) -> Optional[ComponentMetadata]:
        component_dir = self.get_component_path(component_name)
        registry_json_path = component_dir / "registry.json"

        if not registry_json_path.exists():
            return None

        try:
            with open(registry_json_path, 'r') as f:
                data = json.load(f)
                return ComponentMetadata.from_dict(data)
        except (json.JSONDecodeError, IOError, KeyError):
            return None

    def list_components(self) -> List[ComponentMetadata]:
        components_dir = self.registry_path / "components"
        if not components_dir.exists():
            return []

        components = []
        for item in components_dir.iterdir():
            if item.is_dir():
                metadata = self.load_component(item.name)
                if metadata:
                    components.append(metadata)
        return components
