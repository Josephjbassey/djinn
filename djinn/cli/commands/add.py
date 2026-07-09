import click
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry
from djinn.core.installer import Installer

@click.command()
@click.argument("component")
@click.option("--force", is_flag=True, help="Overwrite existing files.")
def add(component, force):
    """Add a component to the project."""
    config = Config.load()
    if not config:
        # Fallback to bundled registry if not initialized
        config = Config(**DEFAULT_CONFIG.copy())
        click.echo("Djinn not initialized. Using bundled registry defaults.")

    registry = Registry(config)
    installer = Installer(config, registry)

    try:
        installed_files = installer.install(component, force=force)
        click.echo(f"Successfully installed '{component}':")
        for _, path in installed_files:
            click.echo(f"  - {path}")
    except FileExistsError as e:
        raise click.ClickException(f"{e} Use --force to overwrite.")
    except (ValueError, FileNotFoundError) as e:
        raise click.ClickException(str(e))
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {e}")
