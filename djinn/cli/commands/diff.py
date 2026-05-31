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
        registry_url = DEFAULT_CONFIG["registry_url"]
        config = Config(registry_url=registry_url, output=DEFAULT_CONFIG["output"])
        click.echo("Djinn not initialized. Diffing against bundled registry.")
    else:
        registry_url = config.registry_url

    registry = Registry(registry_url)
    metadata = registry.load_component(component)

    if not metadata:
        raise click.ClickException(f"Component '{component}' not found in registry.")

    click.echo(f"Diffing '{component}' (Registry Version: {metadata.version}):")

    any_diff = False
    for file_type, file_name in metadata.files.items():
        if file_type == "template":
            dest_base = Path(metadata.install.get("template_path", config.get_template_path()))
        elif file_type == "python":
            dest_base = Path(metadata.install.get("python_path", config.get_python_path()))
        else:
            click.echo(f"  [WARNING] Unknown file type '{file_type}' for {file_name}. Skipping.")
            continue

        dest_path = dest_base / file_name
        registry_file_path = registry.get_component_file_path(component, file_name)

        try:
            # Fetch registry content
            src_content = registry.fetch_content(registry_file_path)
            src_hash = calculate_hash(src_content)
        except Exception:
            click.echo(f"  [MISSING_REGISTRY] {registry_file_path}")
            any_diff = True
            continue

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
