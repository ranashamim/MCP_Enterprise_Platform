
from client import collect_arguments


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
