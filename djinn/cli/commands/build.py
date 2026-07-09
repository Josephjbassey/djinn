import click
import sys
from djinn.scripts.build_registry import build_registry

@click.command()
@click.argument('components_dir', default="djinn/registry/components", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('output_file', default="djinn/registry/index.json", type=click.Path(dir_okay=False))
def build(components_dir, output_file):
    """Build the registry.json payload from local component files."""
    try:
        build_registry(components_dir, output_file)
        click.secho(f"Registry successfully built at {output_file}", fg="green")
    except Exception as e:
        raise click.ClickException(f"Failed to build registry: {e}")
