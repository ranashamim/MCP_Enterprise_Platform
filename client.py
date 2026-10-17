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
        print("Tool call successful:")
        print(response.structured_content)

    return response
        
def collect_arguments(tool) -> dict:
    print(f"\nTool: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Input schema: {tool.input_schema['properties'].keys()}")

    arguments_num = tool.input_schema['properties'].keys()
    arguments = {}
    for arg in arguments_num:
        value=input(f"Please enter {arg}: ")
        arg_type = tool.input_schema["properties"][arg]["type"]

        while(True):
            try:
                if arg_type == "integer":
                    arguments[arg] = int(value)
                    break
                elif arg_type == "number":
                    arguments[arg] = float(value)
                    break
                elif arg_type == "boolean":
                    arguments[arg] = value.strip().lower() in ("true", "yes", "1")
                    break
                else:
                    arguments[arg] = value
                    break
            except ValueError:
                print(f"Please enter a valid {arg_type}.")
                value = input(f"Please enter {arg}: ")

    return arguments


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
                print(str(i+1)+"-"+tool)

            while(True):
                tool_name=input("Please enter your tool or 0 to exit: ")
                if tool_name == "0":
                    break
                
                tool = next((item for item in result.tools if item.name == tool_name),None,)
                if(tool):
                    arguments = collect_arguments(tool=tool)
                    print(f"Arguments: {arguments}")
                    
                    response = await helper(
                        session=session,
                        tool_name=tool_name,
                        arguments=arguments
                    )
                else:
                    print("the tool isn't available.")

                print("result: ")
                print(response.structured_content['result'])
                return response
            
           
            

        

if __name__ == "__main__":
    asyncio.run(main())