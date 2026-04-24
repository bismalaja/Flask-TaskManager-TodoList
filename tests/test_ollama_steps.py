from flask_app.services.ollama_steps import (
    _extract_steps_from_text,
    _normalize_model_name,
    _parse_steps,
)


def test_normalize_model_name_adds_default_suffix_and_lowercases():
    assert _normalize_model_name(" QWEN2.5 ") == "qwen2.5:0.5b"
    assert _normalize_model_name("llama3.2:1b") == "llama3.2:1b"


def test_extract_steps_from_text_strips_bullets_and_noise():
    text = """
    Here are your steps:
    - First action
    * Second action
    1. Third action
    ```
    [
    ]
    "quoted step",
    """

    steps = _extract_steps_from_text(text)

    assert steps == ["First action", "Second action", "Third action", "quoted step"]


def test_parse_steps_returns_empty_for_non_actionable_text():
    assert _parse_steps("   ") == []


def test_parse_steps_limits_to_ten_items():
    lines = "\n".join(f"- item {i}" for i in range(15))

    steps = _parse_steps(lines)

    assert len(steps) == 10
    assert steps[0] == "item 0"
    assert steps[-1] == "item 9"
