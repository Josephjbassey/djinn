import click
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry
from djinn.core.installer import Installer

@click.command()
@click.argument("components", nargs=-1)
@click.option("--force", is_flag=True, help="Overwrite existing files.")
def add(components, force):
    """Add components to the project."""
    if not components:
        click.echo("Please specify at least one component to add.")
        return

    config = Config.load()
    if not config:
        # Fallback to bundled registry if not initialized
        config = Config(**DEFAULT_CONFIG.copy())
        click.echo("Djinn not initialized. Using bundled registry defaults.")

    registry = Registry(config)
    installer = Installer(config, registry)

    for component in components:
        try:
            installed_files = installer.install(component, force=force)
            click.echo(f"Successfully installed '{component}':")
            for _, path in installed_files:
                click.echo(f"  - {path}")
        except FileExistsError as e:
            click.secho(f"Error installing '{component}': {e} Use --force to overwrite.", fg="red")
        except (ValueError, FileNotFoundError) as e:
            click.secho(f"Error installing '{component}': {e}", fg="red")
        except Exception as e:
            click.secho(f"An unexpected error occurred while installing '{component}': {e}", fg="red")

