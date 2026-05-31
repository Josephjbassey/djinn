import shutil
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

        component_src_dir = self.registry.get_component_path(component_name)
        installed_files = []

        for file_type, file_name in metadata.files.items():
            # Determine destination path based on file type and registry/config settings
            if file_type == "template":
                dest_base = Path(metadata.install.get("template_path", self.config.get_template_path()))
            elif file_type == "python":
                dest_base = Path(metadata.install.get("python_path", self.config.get_python_path()))
            else:
                # Fallback or generic handling if more types are added
                dest_base = Path("components")

            dest_path = dest_base / file_name
            src_path = component_src_dir / file_name

            if not src_path.exists():
                raise FileNotFoundError(f"Source file '{file_name}' not found in registry for component '{component_name}'.")

            if dest_path.exists() and not force:
                raise FileExistsError(f"File '{dest_path}' already exists. Use --force to overwrite.")

            # Create directories if missing
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(src_path, dest_path)
            installed_files.append((file_type, dest_path))

        return installed_files
