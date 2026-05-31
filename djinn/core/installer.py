import os
from pathlib import Path
from typing import List, Tuple
from djinn.core.config import Config
from djinn.core.registry import ComponentMetadata, Registry

class Installer:
    def __init__(self, config: Config, registry: Registry):
        self.config = config
        self.registry = registry

    def install(self, component_name: str, force: bool = False) -> List[Tuple[str, Path]]:
        metadata = self.registry.load_component(component_name)
        if not metadata:
            raise ValueError(f"Component '{component_name}' not found in registry.")

        # Phase 1: Validation
        files_to_install = []
        for file_type, file_name in metadata.files.items():
            if file_type == "template":
                dest_base = Path(metadata.install.get("template_path", self.config.get_template_path()))
            elif file_type == "python":
                dest_base = Path(metadata.install.get("python_path", self.config.get_python_path()))
            else:
                dest_base = Path("components")

            dest_path = dest_base / file_name

            # Check if local file exists
            if dest_path.exists() and not force:
                raise FileExistsError(f"File '{dest_path}' already exists. Use --force to overwrite.")

            # Relative path in registry
            registry_file_path = self.registry.get_component_file_path(component_name, file_name)

            files_to_install.append((file_type, registry_file_path, dest_path))

        # Phase 2: Installation
        installed_files = []
        for file_type, registry_file_path, dest_path in files_to_install:
            try:
                content = self.registry.fetch_content(registry_file_path)
            except FileNotFoundError:
                 raise FileNotFoundError(f"Source file '{registry_file_path}' not found in registry.")

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as f:
                f.write(content)

            installed_files.append((file_type, dest_path))

        return installed_files
