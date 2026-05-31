import click
from tabulate import tabulate
from djinn.core.config import Config
from djinn.core.registry import Registry

@click.command()
def list_components():
    """List available components in the registry."""
    config = Config.load()
    registry_url = config.registry_url if config else "registry"

    registry = Registry(registry_url)
    components = registry.list_components()

    if not components:
        click.echo("No components found in registry.")
        return

    table_data = [[c.name, c.version] for c in components]
    click.echo(tabulate(table_data, headers=["Component", "Version"], tablefmt="simple"))
