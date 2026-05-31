import click
from tabulate import tabulate
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry

@click.command()
def list_components():
    """List available components in the registry."""
    config = Config.load()
    if config:
        registry_url = config.registry_url
    else:
        registry_url = DEFAULT_CONFIG["registry_url"]
        click.echo("Djinn not initialized. Showing components from bundled registry.")

    try:
        registry = Registry(registry_url)
        components = registry.list_components()

        if not components:
            click.echo(f"No components found in registry: {registry_url}")
            return

        table_data = [[c.name, c.version] for c in components]
        click.echo(tabulate(table_data, headers=["Component", "Version"], tablefmt="simple"))
    except Exception as e:
        raise click.ClickException(f"Failed to list components: {e}")
