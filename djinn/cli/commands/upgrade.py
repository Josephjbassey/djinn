import click
from pathlib import Path
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry
from djinn.core.installer import Installer
from djinn.core.utils import calculate_hash


@click.command(name="upgrade")
@click.argument("component")
@click.option("--force", is_flag=True, help="Upgrade without prompting.")
def upgrade(component, force):
    """Upgrade a component to the latest registry version."""
    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())
        click.echo("Djinn not initialized. Using bundled registry defaults.")

    registry = Registry(config)
    installer = Installer(config, registry)

    metadata = registry.load_component(component)
    if not metadata:
        click.secho(f"Component '{component}' not found in registry.", fg="red")
        return

    # Check what differs
    changed = []
    for file_obj in metadata.files:
        file_name = file_obj["name"]
        file_dir = file_obj.get("dir", "")
        registry_content = file_obj.get("content", "")

        if "templates" in file_dir:
            dest_base = Path(metadata.install.get("template_path", config.get_template_path()))
        elif "templatetags" in file_dir:
            dest_base = Path(metadata.install.get("python_path", config.get_python_path()))
        else:
            dest_base = Path(file_dir) if file_dir else Path("components")

        dest_path = dest_base / file_name

        src_hash = calculate_hash(registry_content.encode("utf-8"))

        if not dest_path.exists():
            changed.append((file_name, dest_path, "missing"))
        else:
            dest_hash = calculate_hash(dest_path)
            if src_hash != dest_hash:
                changed.append((file_name, dest_path, "changed"))

    if not changed:
        click.echo(f"'{component}' is already up to date.")
        return

    click.echo(f"Found {len(changed)} out-of-date file(s) for '{component}':")
    for file_name, dest_path, status in changed:
        click.echo(f"  - {dest_path} ({status})")

    if not force:
        if not click.confirm(f"Upgrade '{component}' now?", default=True):
            click.echo("Upgrade cancelled.")
            return

    installed = installer.install(component, force=True)
    click.echo(f"Successfully upgraded '{component}':")
    for _, path in installed:
        click.echo(f"  - {path}")
