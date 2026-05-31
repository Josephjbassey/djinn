import click
from djinn.cli.commands.init import init
from djinn.cli.commands.add import add
from djinn.cli.commands.list import list_components
from djinn.cli.commands.diff import diff

@click.group()
@click.version_option()
def cli():
    """Djinn: A shadcn-style component installer for Django."""
    pass

cli.add_command(init)
cli.add_command(add)
cli.add_command(list_components, name="list")
cli.add_command(diff)

if __name__ == "__main__":
    cli()
