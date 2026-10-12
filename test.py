from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService

import sqlite3


ticket_repository = TicketRepository('tickets.db')
ticket_service = TicketService(ticket_repository=ticket_repository)

try:
    connection = sqlite3.connect('tickets.db')
    
    cursor = connection.execute(
            "select * from tickets where status = 'open' "
    )
    tickets = cursor.fetchall()

except ValueError as e:
    print(f"Error creating ticket: {e}")
finally:
     connection.close()

print(tickets)

