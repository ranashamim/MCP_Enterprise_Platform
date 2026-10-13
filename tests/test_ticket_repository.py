from app.repositories.ticket_repository import TicketRepository


def test_get_existing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_rep.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    
    # check existed data
    ticket = ticket_rep.get_ticket(ticket_id="T001")
    assert ticket["ticket_id"] == "T001"
    assert ticket["customer_id"] == "C001"

def test_get_missing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    
    # check not exist data
    ticket1 = ticket_rep.get_ticket(ticket_id="T999")
    assert ticket1 is None

def test_create_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket = ticket_rep.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")

    assert ticket["ticket_id"] == "T001"
    assert ticket["customer_id"] == "C001"
    assert ticket["priority"] == "high"

def test_update_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_rep.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    ticket = ticket_rep.update_ticket(ticket_id="T001", priority="low")

    assert ticket["ticket_id"] == "T001"
    assert ticket["priority"] == "low"

def test_update_missing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket = ticket_rep.update_ticket(ticket_id="T001", priority="low")

    assert ticket is None

def test_close_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket_rep.create_ticket(ticket_id="T001", customer_id="C001", description="Test", priority="high")
    ticket = ticket_rep.close_ticket(ticket_id="T001")

    assert ticket["ticket_id"] == "T001"
    assert ticket["status"] == "closed"

def test_close_missing_ticket(tmp_path):
    ticket_rep = TicketRepository(tmp_path / "test_tickets.db")
    ticket_rep.initialize()
    ticket = ticket_rep.close_ticket(ticket_id="T001")

    assert ticket is None