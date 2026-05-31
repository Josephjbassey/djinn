import click
import os
from djinn.core.config import Config, DEFAULT_CONFIG

@click.command()
@click.option("--yes", "-y", is_flag=True, help="Skip interactive prompts and use defaults.")
@click.option("--defaults", is_flag=True, help="Skip interactive prompts and use defaults.")
def init(yes, defaults):
    """Initialize Djinn in the current project."""
    if Config.load():
        if not click.confirm("Djinn is already initialized. Overwrite existing configuration?", default=False):
            return

    if yes or defaults:
        config = Config.init()
        click.echo(f"Initialized djinn.config.json with defaults.")
        return

    # Interactive prompts
    registry_url = click.prompt(
        "Registry URL (or path)",
        default=DEFAULT_CONFIG["registry_url"]
    )

    template_path = click.prompt(
        "Where should Django templates be installed?",
        default=DEFAULT_CONFIG["output"]["templates"]
    )

    python_path = click.prompt(
        "Where should Python component files be installed?",
        default=DEFAULT_CONFIG["output"]["python"]
    )

    config_data = {
        "registry_url": registry_url,
        "output": {
            "templates": template_path,
            "python": python_path
        }
    }

    config = Config(
        registry_url=config_data["registry_url"],
        output=config_data["output"]
    )
    config.save()

    click.echo("\nDjinn initialized successfully!")
    click.echo(f"Config saved to djinn.config.json")
