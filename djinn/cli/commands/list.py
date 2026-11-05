import click
from tabulate import tabulate
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry

@click.command()
@click.argument('query', required=False)
def list_components(query):
    """List or search available components in the registry."""
    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())
        click.echo("Djinn not initialized. Showing components from bundled registry.")

    try:
        registry = Registry(config)
        components = registry.list_components()

        if query:
            query_lower = query.lower()
            components = [c for c in components if query_lower in c.name.lower()]

        if not components:
            if query:
                click.echo(f"No components found matching '{query}'.")
            else:
                click.echo(f"No components found in registry: {registry_url}")
            return

        table_data = [[c.name, c.type] for c in components]
        click.echo(tabulate(table_data, headers=["Component", "Type"], tablefmt="simple"))
    except Exception as e:
        raise click.ClickException(f"Failed to list components: {e}")
