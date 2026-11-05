import os
from pathlib import Path
from typing import List, Tuple
from djinn.core.config import Config
from djinn.core.registry import ComponentMetadata, Registry

class Installer:
    def __init__(self, config: Config, registry: Registry):
        self.config = config
        self.registry = registry

    def install(self, component_name: str, force: bool = False, installed_components: set = None) -> List[Tuple[str, Path]]:
        if installed_components is None:
            installed_components = set()

        if component_name in installed_components:
            return []

        metadata = self.registry.load_component(component_name)
        if not metadata:
            raise ValueError(f"Component '{component_name}' not found in registry.")

        installed_components.add(component_name)
        installed_files = []

        # Recursively install registry dependencies first
        for dep in metadata.registryDependencies:
            installed_files.extend(self.install(dep, force=force, installed_components=installed_components))

        # Phase 1: Validation
        files_to_install = []
        for file_obj in metadata.files:
            file_name = file_obj["name"]
            file_dir = file_obj.get("dir", "")
            content = file_obj.get("content", "")

            if "templates" in file_dir:
                dest_base = Path(metadata.install.get("template_path", self.config.get_template_path()))
            elif "templatetags" in file_dir:
                dest_base = Path(metadata.install.get("python_path", self.config.get_python_path()))
            else:
                dest_base = Path(file_dir) if file_dir else Path("components")

            dest_path = dest_base / file_name

            # Check if local file exists
            if dest_path.exists() and not force:
                raise FileExistsError(f"File '{dest_path}' already exists. Use --force to overwrite.")

            files_to_install.append((file_name, dest_path, content))

        # Phase 2: Installation
        for file_name, dest_path, content in files_to_install:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)

            installed_files.append((file_name, dest_path))

        return installed_files

