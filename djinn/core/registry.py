import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import importlib.resources
import urllib.request
import urllib.error

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
    def __init__(self, registry_url: str):
        self.registry_url = registry_url
        self.is_remote = registry_url.startswith(("http://", "https://"))
        self._bundled_path: Optional[Path] = None

        if not self.is_remote:
            path = Path(registry_url)
            # If registry_url is "__bundled__" or doesn't exist locally, try bundled
            if registry_url == "__bundled__" or not (path / "components").exists():
                self._bundled_path = self._resolve_bundled_path()
                if self._bundled_path:
                    self.registry_url = str(self._bundled_path)
            else:
                self.registry_url = str(path.absolute())

    def _resolve_bundled_path(self) -> Optional[Path]:
        try:
            bundled_res = importlib.resources.files('djinn') / 'registry'
            if bundled_res.joinpath('components').exists():
                # We need a physical path for some operations, as_file provides that
                # but it's a context manager. For simplicity in this CLI, we assume
                # it's installed as a regular package or we use the Traversable API.
                # Here we'll try to get a path.
                with importlib.resources.as_file(bundled_res) as p:
                    return Path(p)
        except (ImportError, TypeError, FileNotFoundError):
            pass
        return None

    def fetch_content(self, relative_path: str) -> bytes:
        """Fetch content from the registry (local or remote)."""
        if self.is_remote:
            url = f"{self.registry_url.rstrip('/')}/{relative_path}"
            try:
                with urllib.request.urlopen(url) as response:
                    return response.read()
            except urllib.error.URLError as e:
                raise RuntimeError(f"Failed to fetch from remote registry: {e}")
        else:
            full_path = Path(self.registry_url) / relative_path
            if not full_path.exists():
                raise FileNotFoundError(f"File not found in registry: {full_path}")
            return full_path.read_bytes()

    def load_component(self, component_name: str) -> Optional[ComponentMetadata]:
        try:
            content = self.fetch_content(f"components/{component_name}/registry.json")
            data = json.loads(content.decode('utf-8'))
            return ComponentMetadata.from_dict(data)
        except (Exception, json.JSONDecodeError):
            return None

    def get_component_file_path(self, component_name: str, file_name: str) -> str:
        """Returns the relative path for a component file in the registry."""
        return f"components/{component_name}/{file_name}"

    def list_components(self) -> List[ComponentMetadata]:
        if self.is_remote:
            # Listing remote components is hard without a specific API or index.json
            # For now, we'll try to fetch index.json if it exists, otherwise return empty
            try:
                content = self.fetch_content("index.json")
                data = json.loads(content.decode('utf-8'))
                return [ComponentMetadata.from_dict(c) for c in data.get("components", [])]
            except Exception:
                return []
        else:
            components_dir = Path(self.registry_url) / "components"
            if not components_dir.exists():
                return []

            components = []
            for item in components_dir.iterdir():
                if item.is_dir():
                    metadata = self.load_component(item.name)
                    if metadata:
                        components.append(metadata)
            return components
