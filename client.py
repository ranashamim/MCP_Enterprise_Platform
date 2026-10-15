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

async def helper( session: ClientSession, tool_name: str, arguments: dict | None = None):
    response = await session.call_tool(
                    name=tool_name,
                    arguments=arguments or {}
                )
    if response.is_error:
        print("Tool call failed:")
        print(response.content)
    else:
        print(response.structured_content)

    return response
        

async def main():
# Start the server and establish stdio communication
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()

            # Call the add tool on the MCP server
            available_tools = [tool.name for tool in result.tools]

            print("Available tools:")
            for i,tool in enumerate(available_tools):
                print(str(i)+"-"+tool)

            tool_name=input("Please enter your tool: ")
            arguments={input("Please enter its arguments if it has.Enter key: "): input("Enter value: ")}
            
            if tool_name not in available_tools:
                print("the tool isn't available.")
            else:
                await helper(
                    session=session,
                    tool_name=tool_name,
                    arguments=arguments
                )

            


if __name__ == "__main__":
    asyncio.run(main())