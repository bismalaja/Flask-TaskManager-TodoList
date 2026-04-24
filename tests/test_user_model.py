from flask_app.models.user import User


def test_validate_user_valid_payload(monkeypatch):
    captured = []

    def fake_flash(message, category):
        captured.append((message, category))

    monkeypatch.setattr("flask_app.models.user.flash", fake_flash)
    monkeypatch.setattr(User, "get_by_email", lambda *_args, **_kwargs: None)

    is_valid = User.validate_user(
        {
            "first_name": "Sam",
            "last_name": "Ridge",
            "email": "sam@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
    )

    assert is_valid is True
    assert captured == []


def test_validate_user_invalid_payload_reports_errors(monkeypatch):
    captured = []

    def fake_flash(message, category):
        captured.append((message, category))

    monkeypatch.setattr("flask_app.models.user.flash", fake_flash)
    monkeypatch.setattr(User, "get_by_email", lambda *_args, **_kwargs: {"id": 1})

    is_valid = User.validate_user(
        {
            "first_name": "A",
            "last_name": "B",
            "email": "bad-email",
            "password": "short",
            "confirm_password": "different",
        }
    )

    assert is_valid is False
    assert len(captured) == 6
    assert all(category == "register" for _, category in captured)
