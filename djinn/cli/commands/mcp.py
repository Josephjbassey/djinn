import click
import asyncio
import json
from djinn.core.registry import Registry
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.installer import Installer

# Try to import MCP. If not installed, provide a graceful fallback.
try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    from mcp.server.models import InitializationOptions
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# Tool implementations shared between stdio and HTTP transports.
def _handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_project_info",
            description="Get information about the current Djinn UI project setup.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="search_components",
            description="List or search available components in the registry.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Optional search query to filter components."
                    }
                }
            },
        ),
        Tool(
            name="add_component",
            description="Add a component to the project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "description": "Name of the component to add (e.g. 'button' or '@internal/card')."
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Whether to force overwrite existing files."
                    }
                },
                "required": ["component"]
            },
        ),
    ]


def _handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    arguments = arguments or {}

    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())

    registry = Registry(config)

    if name == "get_project_info":
        info = {
            "style": config.style,
            "registry_url": config.registry_url,
            "tailwind_css": config.tailwind.get("css", "N/A"),
            "tailwind_config": config.tailwind.get("config", "N/A"),
            "aliases": config.aliases,
            "namespaces": list(config.registries.keys()) if hasattr(config, "registries") else []
        }
        return [TextContent(type="text", text=json.dumps(info, indent=2))]

    elif name == "search_components":
        query = arguments.get("query", "").lower()
        try:
            components = registry.list_components()
            if query:
                components = [c for c in components if query in c.name.lower()]

            res = [f"{c.name} ({c.type})" for c in components]
            if not res:
                return [TextContent(type="text", text="No components found.")]
            return [TextContent(type="text", text="\n".join(res))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching components: {str(e)}")]

    elif name == "add_component":
        component = arguments.get("component")
        force = arguments.get("force", False)
        if not component:
            return [TextContent(type="text", text="Error: Missing component name.")]

        installer = Installer(config, registry)
        try:
            installed = installer.install(component, force=force)
            output = f"Successfully installed '{component}':\n"
            for _, path in installed:
                output += f"  - {path}\n"
            return [TextContent(type="text", text=output)]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to install component: {str(e)}")]

    raise ValueError(f"Unknown tool: {name}")


if MCP_AVAILABLE:
    server = Server("djinn")

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return _handle_list_tools()

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
        return _handle_call_tool(name, arguments)


@click.command(name="mcp")
@click.option("--http", "use_http", is_flag=True, help="Serve over HTTP/SSE instead of stdio.")
@click.option("--host", default="127.0.0.1", help="Host to bind to (HTTP mode only).")
@click.option("--port", default=8000, help="Port to bind to (HTTP mode only).")
def mcp(use_http, host, port):
    """Start the Model Context Protocol (MCP) server.

    By default runs over stdio. Use --http to serve over HTTP/SSE for
    remote agent connections (e.g. via Tailscale Funnel).
    """
    if not MCP_AVAILABLE:
        click.secho("The MCP server is not available. Install 'mcp' package to enable it.", fg="red")
        return

    if use_http:
        _run_http_server(host, port)
    else:
        _run_stdio_server()


def _run_stdio_server():
    """Run the MCP server over stdio."""
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="djinn",
                    server_version="0.1.11",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass


def _run_http_server(host: str, port: int):
    """Run the MCP server over HTTP/SSE using FastMCP."""
    from mcp.server.fastmcp import FastMCP

    app = FastMCP(
        name="djinn",
        instructions="Djinn UI MCP server. Use get_project_info, search_components, and add_component to interact with your Djinn UI project.",
        host=host,
        port=port,
    )

    # Register the same tools as the stdio server.
    for tool in _handle_list_tools():
        app.add_tool(
            name=tool.name,
            fn=_make_tool_fn(tool.name),
            description=tool.description,
        )

    click.secho(f"Djinn MCP server running on http://{host}:{port}", fg="green")
    click.secho(f"SSE endpoint: http://{host}:{port}/sse", fg="green")
    click.secho(f"Message endpoint: http://{host}:{port}/messages/", fg="green")
    click.secho("Press Ctrl+C to stop.", fg="yellow")

    try:
        asyncio.run(app.run_sse_async())
    except KeyboardInterrupt:
        pass


def _make_tool_fn(tool_name: str):
    """Create an async function that wraps _handle_call_tool for FastMCP."""
    async def tool_fn(**kwargs):
        return _handle_call_tool(tool_name, kwargs)
    return tool_fn
