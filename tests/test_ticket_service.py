import pytest

from app.services.ticket_service import TicketService
from app.repositories.ticket_repository import TicketRepository


def test_validate_priority(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket_ser.validate_priority(priority="high")

   
def test_invalid_priority(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    with pytest.raises(ValueError):
        ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="urgent")


def test_create_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket = ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="low")

    assert ticket["ticket_id"] == "T001"
    assert ticket["customer_id"] == "C001"
    assert ticket["priority"] == "low"

def test_invalid_create_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    with pytest.raises(ValueError):
        ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="urgent")


def test_get_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    ticket = ticket_ser.get_ticket(ticket_id="T001")

    assert ticket["ticket_id"] == "T001"
    assert ticket["customer_id"] == "C001"
    assert ticket["priority"] == "high"


def test_get_missing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    with pytest.raises(ValueError):
        ticket_ser.get_ticket(ticket_id="T001")


def test_list_tickets(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    ticket = ticket_ser.list_tickets()

    assert ticket[0]["ticket_id"] == "T001"
    assert ticket[0]["customer_id"] == "C001"
    assert ticket[0]["priority"] == "high"


def test_list_no_tickets(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket = ticket_ser.list_tickets()

    assert ticket == []


def test_update_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    ticket = ticket_ser.update_ticket(ticket_id="T001", priority="low")

    assert ticket["ticket_id"] == "T001"
    assert ticket["customer_id"] == "C001"
    assert ticket["priority"] == "low"


def test_update_missing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    with pytest.raises(ValueError):
        ticket_ser.update_ticket(ticket_id="T001", priority="low")
  

def test_close_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    ticket = ticket_ser.close_ticket(ticket_id="T001")

    assert ticket["ticket_id"] == "T001"
    assert ticket["customer_id"] == "C001"
    assert ticket["status"] == "closed"


def test_close_missing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    with pytest.raises(ValueError):
        ticket_ser.close_ticket(ticket_id="T001")


def test_duplicate_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_ser = TicketService(ticket_rep)
    ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    with pytest.raises(ValueError):
        ticket_ser.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
               

   
    

