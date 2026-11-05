import click
import json
from djinn.core.config import Config

@click.command()
def info():
    """Display information about your project and Djinn configuration."""
    config = Config.load()
    if not config:
        click.secho("No djinn.json found. Run 'djinn init' first.", fg="red")
        return

    click.secho("Project Configuration", bold=True)
    click.echo("-" * 40)
    click.echo(f"Style:       {click.style(config.style, fg='cyan')}")
    click.echo(f"Registry:    {click.style(config.registry_url, fg='cyan')}")
    
    click.secho("\nTailwind", bold=True)
    click.echo("-" * 40)
    click.echo(f"Config File: {click.style(config.tailwind.get('config', 'N/A'), fg='cyan')}")
    click.echo(f"CSS File:    {click.style(config.tailwind.get('css', 'N/A'), fg='cyan')}")
    click.echo(f"Variables:   {click.style(str(config.tailwind.get('cssVariables', False)), fg='cyan')}")

    click.secho("\nAliases / Paths", bold=True)
    click.echo("-" * 40)
    for alias, path in config.aliases.items():
        click.echo(f"{alias.ljust(12)} {click.style(path, fg='cyan')}")
        
    if config.registries:
        click.secho("\nRegistries", bold=True)
        click.echo("-" * 40)
        for namespace, reg_config in config.registries.items():
            if isinstance(reg_config, str):
                url = reg_config
            else:
                url = reg_config.get("url", "")
            click.echo(f"{namespace.ljust(12)} {click.style(url, fg='cyan')}")

