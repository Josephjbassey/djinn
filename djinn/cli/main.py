import click
from djinn.cli.commands.init import init
from djinn.cli.commands.add import add
from djinn.cli.commands.list import list_components
from djinn.cli.commands.diff import diff
from djinn.cli.commands.build import build
from djinn.cli.commands.mcp import mcp
from djinn.cli.commands.info import info
from djinn.cli.commands.view import view
from djinn.cli.commands.docs import docs

@click.group()
@click.version_option()
def cli():
    """Djinn: A shadcn-style component installer for Django."""
    pass

cli.add_command(init)
cli.add_command(add)
cli.add_command(list_components, name="list")
cli.add_command(list_components, name="search")
cli.add_command(diff)
cli.add_command(build)
cli.add_command(mcp)
cli.add_command(info)
cli.add_command(view)
cli.add_command(docs)

if __name__ == "__main__":
    cli()
