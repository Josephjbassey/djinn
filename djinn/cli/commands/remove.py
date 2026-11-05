import click
from pathlib import Path
from djinn.core.config import Config
from djinn.core.registry import Registry


@click.command(name="remove")
@click.argument("component")
@click.option("--force", is_flag=True, help="Remove without prompting.")
def remove(component, force):
    """Remove a component and its installed files from the project."""
    config = Config.load()
    if not config:
        click.secho("Djinn not initialized. Run 'djinn init' first.", fg="red")
        return

    registry = Registry(config)
    metadata = registry.load_component(component)
    if not metadata:
        click.secho(f"Component '{component}' not found in registry.", fg="red")
        return

    # Collect all destination paths
    files_to_remove = []
    for file_obj in metadata.files:
        file_name = file_obj["name"]
        file_dir = file_obj.get("dir", "")

        if "templates" in file_dir:
            dest_base = Path(metadata.install.get("template_path", config.get_template_path()))
        elif "templatetags" in file_dir:
            dest_base = Path(metadata.install.get("python_path", config.get_python_path()))
        else:
            dest_base = Path(file_dir) if file_dir else Path("components")

        dest_path = dest_base / file_name
        files_to_remove.append(dest_path)

    click.echo(f"Would remove {len(files_to_remove)} file(s) for '{component}':")
    for path in files_to_remove:
        exists = "exists" if path.exists() else "missing"
        click.echo(f"  - {path} ({exists})")

    if not force:
        if not click.confirm(f"Remove '{component}' now?", default=True):
            click.echo("Removal cancelled.")
            return

    removed = 0
    for path in files_to_remove:
        if path.exists():
            try:
                path.unlink()
                removed += 1
                click.echo(f"  Removed: {path}")
            except OSError as e:
                click.secho(f"  Failed to remove {path}: {e}", fg="red")
        else:
            click.echo(f"  Skipped (missing): {path}")

    click.echo(f"Removed {removed} file(s) for '{component}'.")
