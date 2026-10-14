import asyncio
from pathlib import Path
import sys

from mcp.client import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


server_params = StdioServerParameters(
    command=sys.executable,
    args=["server.py"],
    cwd=Path.cwd(),
)

async def main():
# Start the server and establish stdio communication
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()
            print("\nAvailable MCP tools:\n")

            for tool in result.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call the add tool on the MCP server
            result = await session.call_tool(
                "add",
                arguments={"a": 5, "b": 3},
            )

            print("\nTool call result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())