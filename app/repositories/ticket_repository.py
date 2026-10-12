
import sqlite3

class TicketRepository:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS tickets(ticket_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL, description TEXT NOT NULL, priority TEXT NOT NULL, status TEXT DEFAULT 'open')"
            )
        finally:
            connection.close()

    def create_ticket(self, ticket_id:str, customer_id:str, description:str, priority:str) -> dict | None:
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "INSERT INTO tickets(ticket_id, customer_id, description, priority) VALUES (?, ?, ?, ?)",
                (ticket_id, customer_id, description, priority)
            )
            connection.commit()
        finally:
            connection.close()

        ticket = self.get_ticket(ticket_id= ticket_id)
        if ticket is None:
            return None
        return dict(ticket)

    def get_ticket(self, ticket_id: str) -> sqlite3.Row | None:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            cursor = connection.execute(
                "select * from tickets where ticket_id = ?", (ticket_id,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def list_tickets(self) -> list[dict] :
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            cursor = connection.execute(
                "select * from tickets"
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            connection.close()

    def update_ticket(self, ticket_id: str, priority: str) -> dict | None:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute(
                "UPDATE tickets SET priority = ? WHERE ticket_id = ?", (priority, ticket_id)
            )
            connection.commit()
        finally:
            connection.close()

        ticket = self.get_ticket(ticket_id= ticket_id)
        if ticket is None:
            return None
        return dict(ticket)

    def close_ticket(self, ticket_id: str) -> dict | None:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute(
                "update tickets set status = 'closed' where ticket_id = ?", (ticket_id,)
            )
            connection.commit()
        finally:
            connection.close()
        
        ticket = self.get_ticket(ticket_id= ticket_id)
        if ticket is None:
            return None
        return dict(ticket)


