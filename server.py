from mcp.server import MCPServer
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("Enterprise Platform")

ticket_rep = TicketRepository("tickets.db")
ticket_rep.initialize()
ticket_ser = TicketService(ticket_repository=ticket_rep)

# MCP Tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def create_ticket(ticket_id: str, customer_id: str, description: str, priority: str) -> dict | None:
    """Create a support ticket."""
    try:
        ticket = ticket_ser.create_ticket(ticket_id=ticket_id, customer_id=customer_id, description=description, priority=priority)
        return ticket
    except ValueError as exc:
        raise ToolError(str(exc)) from exc

@mcp.tool()
def get_ticket(ticket_id:str) -> dict | None:
    """Get a ticket"""
    try:
        ticket = ticket_ser.get_ticket(ticket_id=ticket_id)
        return ticket
    except ValueError as exc:
                raise ToolError(str(exc)) from exc

@mcp.tool()
def list_tickets() -> list[dict]:
    """Get list of tickets"""
    tickets = ticket_ser.list_tickets()
    return tickets

@mcp.tool()
def update_ticket(ticket_id:str, priority:str) -> dict | None:
    """Update priority of ticket"""
    try:
        ticket = ticket_ser.update_ticket(ticket_id=ticket_id, priority=priority)
        return ticket
    except ValueError as exc:
            raise ToolError(str(exc)) from exc
    

@mcp.tool()
def close_ticket(ticket_id:str) -> dict | None:
    """Close a ticket"""
    try:
        ticket = ticket_ser.close_ticket(ticket_id=ticket_id)
        return ticket
    except ValueError as exc:
        raise ToolError(str(exc)) from exc

# MCP resources
@mcp.resource("ticket://{ticket_id}")
def get_ticket_resource(ticket_id: str):
    """Get a ticket with its ticket_id"""
    try:
        ticket = ticket_ser.get_ticket(ticket_id=ticket_id)
        return ticket
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


# MCP prompt
@mcp.prompt()
def summarize_ticket(ticket_id: str):
    return f"""
    Summarize support ticket {ticket_id}.
    Identify its priority, status, and key details.
    Recommend the next action.
    """



if __name__ == "__main__":
    mcp.run(transport="stdio")