import click
from pathlib import Path
from djinn.core.config import Config
from djinn.core.registry import Registry
from djinn.core.utils import calculate_hash

@click.command()
@click.argument("component")
def diff(component):
    """Compare registry version vs local installed version."""
    config = Config.load()
    if not config:
        click.echo("Error: Djinn not initialized. Run 'djinn init' first.")
        return

    registry = Registry(config.registry_url)
    metadata = registry.load_component(component)

    if not metadata:
        click.echo(f"Error: Component '{component}' not found in registry.")
        return

    click.echo(f"Diffing '{component}' (Registry Version: {metadata.version}):")

    component_src_dir = registry.get_component_path(component)

    any_diff = False
    for file_type, file_name in metadata.files.items():
        if file_type == "template":
            dest_base = Path(metadata.install.get("template_path", config.get_template_path()))
        elif file_type == "python":
            dest_base = Path(metadata.install.get("python_path", config.get_python_path()))
        else:
            dest_base = Path("components")

        dest_path = dest_base / file_name
        src_path = component_src_dir / file_name

        if not dest_path.exists():
            click.echo(f"  [MISSING] {dest_path}")
            any_diff = True
            continue

        src_hash = calculate_hash(src_path)
        dest_hash = calculate_hash(dest_path)

        if src_hash != dest_hash:
            click.echo(f"  [CHANGED] {dest_path}")
            any_diff = True
        else:
            click.echo(f"  [MATCH]   {dest_path}")

    if not any_diff:
        click.echo("Local version matches registry version.")
