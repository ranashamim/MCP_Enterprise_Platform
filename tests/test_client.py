
from client import collect_arguments, helper

import pytest


class FakeTool:
    name = "add"
    description = "Add two numbers."
    input_schema = {
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"},
        }
    }


def test_collect_arguments_for_add_tool(monkeypatch):
    # Arrange: provide answers automatically.
    user_inputs = iter(["5", "3"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(user_inputs),
    )

    # Act: run the real function.
    arguments = collect_arguments(FakeTool())

    # Assert: verify the returned data.
    assert arguments == {"a": 5, "b": 3}

def test_collect_arguments_retries_invalid_integer(monkeypatch):
    user_inputs = iter(["hello", "5", "3"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(user_inputs),
    )

    arguments = collect_arguments(FakeTool())

    assert arguments == {"a": 5, "b": 3}

def test_collect_arguments_for_number(monkeypatch):
    class FakeNumberTool:
        name = "calculate"
        description = "Test number conversion."
        input_schema = {
            "properties": {
                "value": {"type": "number"},
            }
        }

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "3.5",
    )

    arguments = collect_arguments(FakeNumberTool())

    assert arguments == {"value": 3.5}

def test_collect_arguments_for_boolean(monkeypatch):
    class FakeBooleanTool:
        name = "toggle"
        description = "Test boolean conversion."
        input_schema = {
            "properties": {
                "enabled": {"type": "boolean"},
            }
        }

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "yes",
    )

    arguments = collect_arguments(FakeBooleanTool())

    assert arguments == {"enabled": True}
    assert arguments["enabled"] is True

@pytest.mark.asyncio
async def test_helper_for_add(monkeypatch):
    class FakeTool:
        name = "add"
        description = "Add two numbers."
        input_schema = {
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            }
        }
    class FakeSession:
        def __init__(self, response):
            self.response = response
            self.called_with = None

        async def call_tool(self, name, arguments):
            self.called_with = {
                "name": name,
                "arguments": arguments,
            }
            return self.response
    class FakeResponse:
        is_error = False
        structured_content = {"result": 8}

    fake_response = FakeResponse()
    fake_session = FakeSession(fake_response)
    arguments = {'a': 5, 'b': 3}
    helper_response = await helper(session=fake_session, tool_name=FakeTool.name,arguments=arguments)

    assert helper_response is fake_response
    assert fake_session.called_with == {"name": "add", "arguments": {"a": 5, "b": 3},}


@pytest.mark.asyncio
async def test_helper_handles_tool_error(capsys):
    class FakeTool:
        name = "get_tickets"
        description = "Gets tickets."
        input_schema = {
            "properties": {}
        }
    class FakeSession:
        def __init__(self, response):
            self.response = response
            self.called_with = None

        async def call_tool(self, name, arguments):
            self.called_with = {
                "name": name,
                "arguments": arguments,
            }
            return self.response
    class FakeResponse:
        is_error = True
        content = ["Ticket does not exist."]

    fake_response = FakeResponse()
    fake_session = FakeSession(fake_response)
    arguments = {}
    helper_response = await helper(session=fake_session, tool_name=FakeTool.name,arguments=arguments)

    captured = capsys.readouterr()

    assert helper_response is fake_response
    assert fake_session.called_with == { "name": "get_tickets", "arguments": {},}
   
    assert "Tool call failed:" in captured.out

@pytest.mark.asyncio
async def test_helper_default_arguments(capsys):
    class FakeTool:
        name = "get_tickets"
        description = "Gets tickets."
        input_schema = {
            "properties": {}
        }
    class FakeSession:
        def __init__(self, response):
            self.response = response
            self.called_with = None

        async def call_tool(self, name, arguments):
            self.called_with = {
                "name": name,
                "arguments": arguments,
            }
            return self.response
    class FakeResponse:
        is_error = True
        content = ["Ticket does not exist."]

    fake_response = FakeResponse()
    fake_session = FakeSession(fake_response)
    helper_response = await helper(session=fake_session, tool_name=FakeTool.name,arguments=None)

    captured = capsys.readouterr()

    assert helper_response is fake_response
    assert fake_session.called_with == { "name": "get_tickets", "arguments": {},}
    
    assert "Tool call failed:" in captured.out
