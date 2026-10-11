from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService

import sqlite3


ticket_repository = TicketRepository('tickets.db')
ticket_service = TicketService(ticket_repository=ticket_repository)

try:
    ticket = ticket_service.create_ticket('T011', 'C002', 'it doesnot work', 'low')
except ValueError as e:
    print(f"Error creating ticket: {e}")

print(ticket)

