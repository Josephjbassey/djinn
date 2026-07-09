import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

if sys.version_info >= (3, 9):
    import importlib.resources as pkg_resources
else:
    import importlib_resources as pkg_resources

import urllib.request
import urllib.error

class ComponentMetadata:
    def __init__(
        self, 
        name: str, 
        files: List[Dict[str, str]], 
        dependencies: Optional[List[str]] = None,
        registryDependencies: Optional[List[str]] = None,
        type: str = "components:ui",
        install: Optional[Dict[str, str]] = None
    ):
        self.name = name
        self.files = files
        self.dependencies = dependencies or []
        self.registryDependencies = registryDependencies or []
        self.type = type
        self.install = install or {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComponentMetadata':
        return cls(
            name=data["name"],
            files=data.get("files", []),
            dependencies=data.get("dependencies", []),
            registryDependencies=data.get("registryDependencies", []),
            type=data.get("type", "components:ui"),
            install=data.get("install", {})
        )

class Registry:
    def __init__(self, config: 'Config'):
        self.config = config

    def _resolve_bundled_path(self) -> Optional[Path]:
        try:
            bundled_res = pkg_resources.files('djinn') / 'registry'
            if bundled_res.joinpath('components').exists():
                with pkg_resources.as_file(bundled_res) as p:
                    return Path(p)
        except (ImportError, TypeError, FileNotFoundError):
            pass
        return None

    def _resolve_component_url(self, component_name: str) -> dict:
        import os
        import re

        for namespace, reg_config in self.config.registries.items():
            if component_name.startswith(namespace + "/"):
                clean_name = component_name[len(namespace) + 1:]
                if isinstance(reg_config, str):
                    url_template = reg_config
                    headers = {}
                else:
                    url_template = reg_config.get("url", "")
                    raw_headers = reg_config.get("headers", {})
                    headers = {}
                    for k, v in raw_headers.items():
                        def repl(match):
                            return os.environ.get(match.group(1), "")
                        headers[k] = re.sub(r'\$\{([^}]+)\}', repl, v)
                
                if "{name}" in url_template:
                    resolved_url = url_template.replace("{name}", clean_name)
                else:
                    resolved_url = f"{url_template.rstrip('/')}/components/{clean_name}/registry.json"
                
                return {"url": resolved_url, "headers": headers, "clean_name": clean_name}

        url = self.config.registry_url
        if url == "__bundled__":
            path = self._resolve_bundled_path()
            if path:
                url = str(path)
        else:
            if not url.startswith(("http://", "https://")):
                url = str(Path(url).absolute())

        if url.startswith(("http://", "https://")):
            if "{name}" in url:
                resolved_url = url.replace("{name}", component_name)
            else:
                resolved_url = f"{url.rstrip('/')}/components/{component_name}/registry.json"
        else:
            resolved_url = f"{url}/components/{component_name}/registry.json"

        return {"url": resolved_url, "headers": {}, "clean_name": component_name}

    def fetch_url(self, url: str, headers: dict) -> bytes:
        if not url.startswith(("http://", "https://")):
            path = Path(url)
            if not path.exists():
                raise FileNotFoundError(f"File not found in registry: {path}")
            return path.read_bytes()

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                return response.read()
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to fetch from registry {url}: {e}")

    def load_component(self, component_name: str) -> Optional[ComponentMetadata]:
        try:
            info = self._resolve_component_url(component_name)
            content = self.fetch_url(info["url"], info["headers"])
            data = json.loads(content.decode('utf-8'))
            
            # Strict schema validation
            required_keys = {"name", "type", "files"}
            if not required_keys.issubset(data.keys()):
                raise ValueError(f"Invalid component schema: Missing required keys {required_keys - data.keys()}")
            
            if not isinstance(data.get("files", []), list):
                raise ValueError("Invalid component schema: 'files' must be a list")
                
            return ComponentMetadata.from_dict(data)
        except Exception as e:
            print(f"Error loading {component_name}: {e}")
            return None

    def list_components(self) -> List[ComponentMetadata]:
        # Simple implementation for default registry
        url = self.config.registry_url
        if url == "__bundled__":
            path = self._resolve_bundled_path()
            if path:
                url = str(path)
        
        if url.startswith(("http://", "https://")):
            index_url = f"{url.rstrip('/')}/index.json"
            try:
                content = self.fetch_url(index_url, {})
                data = json.loads(content.decode('utf-8'))
                return [ComponentMetadata.from_dict(c) for c in data.get("components", [])]
            except Exception:
                return []
        else:
            components_dir = Path(url) / "components"
            if not components_dir.exists():
                return []

            components = []
            for item in components_dir.iterdir():
                if item.is_dir():
                    metadata = self.load_component(item.name)
                    if metadata:
                        components.append(metadata)
            return components
