from app.repositories.ticket_repository import TicketRepository


class TicketService:

    def __init__(self, ticket_repository:TicketRepository) -> None:
        self.ticket_repository = ticket_repository

    def validate_priority(self, priority: str) -> None:
        if priority not in ("low", "medium", "high"):
            raise ValueError("Priority must be low, medium, or high.")

    def create_ticket(self, ticket_id:str, customer_id:str, description:str, priority:str) -> None:
        self.validate_priority(priority=priority)
        ticket = self.ticket_repository.create_ticket(
            ticket_id=ticket_id, customer_id=customer_id, description=description, priority=priority
            )
        return ticket
            