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
        # Try to resolve registry path
        path = Path(registry_path)
        if not path.exists() or not (path / "components").exists():
            # Fallback to bundled registry if local one doesn't exist
            try:
                # Use importlib.resources to find the bundled registry
                # Assuming the registry folder is at the root of the package distribution
                # or we can move it inside djinn/
                bundled_path = Path(str(importlib.resources.files('djinn') / 'registry'))
                if bundled_path.exists():
                    path = bundled_path
            except (ImportError, TypeError):
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
