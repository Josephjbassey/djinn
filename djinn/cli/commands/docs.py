import click
import webbrowser
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry

@click.command()
@click.argument('component')
def docs(component):
    """Open the documentation for a specific component."""
    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())

    registry = Registry(config)
    
    click.echo(f"Looking up documentation for '{component}'...")
    try:
        metadata = registry.load_component(component)
        if not metadata:
            click.secho(f"Error: Component '{component}' not found in registry.", fg="red")
            return
            
        # In a real scenario, the documentation URL might be provided in the registry metadata.
        # Alternatively, we can derive it from the base registry URL.
        # For now, we will assume the web UI is hosted at the base URL of the registry without the /registry path.
        
        info = registry._resolve_component_url(component)
        base_url = info["url"].split("/registry")[0]
        
        if base_url.startswith(("http://", "https://")):
            docs_url = f"{base_url}/docs/components/{metadata.name}"
            click.secho(f"Opening {docs_url} in your browser...", fg="green")
            webbrowser.open(docs_url)
        else:
            click.secho("Error: Cannot open docs for a local/bundled registry.", fg="yellow")
            
    except Exception as e:
        click.secho(f"Failed to fetch component info: {e}", fg="red")
