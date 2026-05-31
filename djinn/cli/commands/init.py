import click
from djinn.core.config import Config

@click.command()
def init():
    """Initialize Djinn in the current project."""
    if Config.load():
        click.echo("Djinn is already initialized in this project.")
        return

    Config.init()
    click.echo("Initialized djinn.config.json")
