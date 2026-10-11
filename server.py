from mcp.server import MCPServer

mcp = MCPServer("Enterprise Platform")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """Multiply two numbers."""
    return a * b