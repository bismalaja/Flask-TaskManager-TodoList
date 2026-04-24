import json

from flask_app.models.task import Task


def test_normalize_steps_cleans_and_limits_to_ten():
    raw = ["  Step 1  ", "", None, "Step 2", 7] + [f"x{i}" for i in range(20)]

    normalized = Task._normalize_steps(raw)

    assert normalized[0] == "Step 1"
    assert normalized[1] == "Step 2"
    assert len(normalized) == 10


def test_serialize_steps_returns_json_array_of_cleaned_values():
    payload = ["  one  ", "two", "", "   "]

    serialized = Task._serialize_steps(payload)

    assert json.loads(serialized) == ["one", "two"]


def test_validate_task_valid_payload(monkeypatch):
    captured = []

    def fake_flash(message, category):
        captured.append((message, category))

    monkeypatch.setattr("flask_app.models.task.flash", fake_flash)

    is_valid = Task.validate_task(
        {
            "title": "Write tests",
            "description": "Create a minimal unit test suite",
            "due_date": "2026-04-30",
            "priority": "medium",
            "status": "todo",
        }
    )

    assert is_valid is True
    assert captured == []


def test_validate_task_invalid_payload_collects_flash_errors(monkeypatch):
    captured = []

    def fake_flash(message, category):
        captured.append((message, category))

    monkeypatch.setattr("flask_app.models.task.flash", fake_flash)

    is_valid = Task.validate_task(
        {
            "title": "x",
            "description": "bad",
            "due_date": "",
            "priority": "urgent",
            "status": "started",
        }
    )

    assert is_valid is False
    assert len(captured) == 5
    assert all(category == "task_error" for _, category in captured)
