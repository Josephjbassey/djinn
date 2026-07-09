import os
import json
import argparse
from pathlib import Path

def build_registry(components_dir: str, output_file: str):
    """
    Takes a directory of components and generates a registry.json schema.
    Expects each component to be in its own directory, containing .html and .py files.
    Optionally, a metadata.json file can define dependencies.
    """
    components_path = Path(components_dir)
    registry = {
        "name": "djinn-ui",
        "components": []
    }

    if not components_path.exists():
        print(f"Error: Directory {components_dir} does not exist.")
        return

    for item in components_path.iterdir():
        if item.is_dir():
            component_name = item.name
            component_data = {
                "name": component_name,
                "dependencies": [],
                "registryDependencies": [],
                "files": [],
                "type": "components:ui"
            }

            # Optional metadata
            metadata_file = item / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    meta = json.load(f)
                    component_data["dependencies"] = meta.get("dependencies", [])
                    component_data["registryDependencies"] = meta.get("registryDependencies", [])
                    component_data["type"] = meta.get("type", "components:ui")

            for file_path in item.iterdir():
                if file_path.is_file() and file_path.name not in ("metadata.json", "preview.md", "registry.json"):
                    content = file_path.read_text(encoding="utf-8")
                    
                    if file_path.suffix == ".html":
                        dir_path = "templates/components"
                    elif file_path.suffix == ".py":
                        dir_path = "templatetags"
                    else:
                        dir_path = "components"

                    component_data["files"].append({
                        "name": file_path.name,
                        "dir": dir_path,
                        "content": content
                    })

            registry["components"].append(component_data)

            # Also save a standalone registry.json for each component
            with open(item / "registry.json", "w") as f:
                json.dump(component_data, f, indent=2)

    with open(output_file, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"Registry generated successfully at {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Djinn registry JSON.")
    parser.add_argument("components_dir", type=str, help="Directory containing component folders.")
    parser.add_argument("output_file", type=str, help="Output registry JSON file path.")
    args = parser.parse_args()
    build_registry(args.components_dir, args.output_file)
