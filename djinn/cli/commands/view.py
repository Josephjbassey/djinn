import click
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry

@click.command()
@click.argument('components', nargs=-1, required=True)
def view(components):
    """View the raw source code of a component without installing it."""
    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())

    registry = Registry(config)
    
    for comp in components:
        click.secho(f"Fetching '{comp}'...", fg="yellow")
        try:
            metadata = registry.load_component(comp)
            if not metadata:
                click.secho(f"Error: Component '{comp}' not found in registry.", fg="red")
                continue
            
            click.secho(f"\nComponent: {metadata.name} (Type: {metadata.type})", bold=True, fg="green")
            click.echo("-" * 60)
            
            for file_obj in metadata.files:
                file_name = file_obj.get("name", "Unknown File")
                content = file_obj.get("content", "")
                click.secho(f"File: {file_name}", bold=True, fg="cyan")
                click.echo(content)
                click.echo("-" * 60)
                
        except Exception as e:
            click.secho(f"Failed to fetch '{comp}': {e}", fg="red")
