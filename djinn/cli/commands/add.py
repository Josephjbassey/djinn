import click
from djinn.core.config import Config
from djinn.core.registry import Registry
from djinn.core.installer import Installer

@click.command()
@click.argument("component")
@click.option("--force", is_flag=True, help="Overwrite existing files.")
def add(component, force):
    """Add a component to the project."""
    config = Config.load()
    if not config:
        raise click.ClickException("Djinn not initialized. Run 'djinn init' first.")

    registry = Registry(config.registry_url)
    installer = Installer(config, registry)

    try:
        installed_files = installer.install(component, force=force)
        click.echo(f"Successfully installed '{component}':")
        for _, path in installed_files:
            click.echo(f"  - {path}")
    except Exception as e:
        raise click.ClickException(str(e))
