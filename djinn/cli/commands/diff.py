import click
from pathlib import Path
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry
from djinn.core.utils import calculate_hash


@click.command()
@click.argument("component")
def diff(component):
    """Compare registry version vs local installed version."""
    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())
        click.echo("Djinn not initialized. Diffing against bundled registry defaults.")

    registry = Registry(config)
    metadata = registry.load_component(component)

    if not metadata:
        raise click.ClickException(f"Component '{component}' not found in registry.")

    click.echo(f"Diffing '{component}':")

    any_diff = False
    for file_obj in metadata.files:
        file_name = file_obj["name"]
        file_dir = file_obj.get("dir", "")
        registry_content = file_obj.get("content", "")

        if "templates" in file_dir:
            dest_base = Path(
                metadata.install.get("template_path", config.get_template_path())
            )
        elif "templatetags" in file_dir:
            dest_base = Path(
                metadata.install.get("python_path", config.get_python_path())
            )
        else:
            dest_base = Path(file_dir) if file_dir else Path("components")

        dest_path = dest_base / file_name

        src_hash = calculate_hash(registry_content.encode("utf-8"))

        if not dest_path.exists():
            click.echo(f"  [MISSING_LOCAL]    {dest_path}")
            any_diff = True
            continue

        try:
            dest_hash = calculate_hash(dest_path)
            if src_hash != dest_hash:
                click.echo(f"  [CHANGED] {dest_path}")
                any_diff = True
            else:
                click.echo(f"  [MATCH]   {dest_path}")
        except Exception as e:
            click.echo(f"  [ERROR]   Could not diff {dest_path}: {e}")
            any_diff = True

    if not any_diff:
        click.echo("Local version matches registry version.")
