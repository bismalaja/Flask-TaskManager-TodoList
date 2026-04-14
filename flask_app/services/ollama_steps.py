import json
import os
import time
from urllib import error, request

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "").strip()
OLLAMA_MODEL_CANDIDATES = [
    name.strip()
    for name in os.getenv(
        "OLLAMA_MODEL_CANDIDATES",
        "qwen2.5:0.5b,qwen2.5:1.5b,llama3.2:1b,tinyllama:1.1b,phi3:mini,llama3.2",
    ).split(",")
    if name.strip()
]
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "20"))
OLLAMA_MODEL_CACHE_SECONDS = int(os.getenv("OLLAMA_MODEL_CACHE_SECONDS", "300"))

_MODEL_CACHE = {"model": None, "expires_at": 0.0}


def _normalize_model_name(name):
    normalized = (name or "").strip().lower()
    if ":" not in normalized:
        normalized += ":0.5b"
    return normalized


def _get_model_candidates():
    ordered = []
    if OLLAMA_MODEL:
        ordered.append(OLLAMA_MODEL)

    ordered.extend(OLLAMA_MODEL_CANDIDATES)

    deduped = []
    seen = set()
    for model in ordered:
        key = _normalize_model_name(model)
        if key and key not in seen:
            seen.add(key)
            deduped.append(model)
    return deduped


def _fetch_available_models():
    req = request.Request(f"{OLLAMA_BASE_URL}/api/tags", method="GET")
    with request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as response:
        decoded = json.loads(response.read().decode("utf-8"))

    model_names = []
    for model in decoded.get("models", []):
        name = model.get("name")
        if isinstance(name, str) and name.strip():
            model_names.append(name.strip())

    return model_names


def _resolve_model_name():
    now = time.time()
    if _MODEL_CACHE["model"] and now < _MODEL_CACHE["expires_at"]:
        return _MODEL_CACHE["model"]

    candidates = _get_model_candidates()
    fallback_model = candidates[0] if candidates else "llama3.2"

    try:
        available_models = _fetch_available_models()
    except (ValueError, json.JSONDecodeError, error.URLError, TimeoutError):
        _MODEL_CACHE["model"] = fallback_model
        _MODEL_CACHE["expires_at"] = now + OLLAMA_MODEL_CACHE_SECONDS
        return fallback_model

    available_by_key = {
        _normalize_model_name(model): model
        for model in available_models
    }

    for candidate in candidates:
        match = available_by_key.get(_normalize_model_name(candidate))
        if match:
            _MODEL_CACHE["model"] = match
            _MODEL_CACHE["expires_at"] = now + OLLAMA_MODEL_CACHE_SECONDS
            return match

    _MODEL_CACHE["model"] = fallback_model
    _MODEL_CACHE["expires_at"] = now + OLLAMA_MODEL_CACHE_SECONDS
    return fallback_model


def _extract_json_candidate(text):
    decoder = json.JSONDecoder()
    for idx, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            candidate, _ = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, (list, dict)):
            return candidate
    return None


def _extract_steps_from_text(text):
    steps = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        
        if line.startswith("```") or line in {"[", "]"}:
            continue

        
        if (line.startswith("{") and line.endswith("}")) or (line.startswith("[") and line.endswith("]")):
            continue

        prefixes = ("- ", "* ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "10. ")
        for prefix in prefixes:
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
                break

        
        lowered = line.lower()
        if lowered.startswith("great") or lowered.startswith("here"):
            continue

        
        
        if line.startswith('"') and line.endswith('",'):
            line = line[1:-2].strip()
        elif line.startswith('"') and line.endswith('"'):
            line = line[1:-1].strip()

        if line:
            steps.append(line)

    return steps[:10]


def _extract_list_from_parsed(parsed):
    if isinstance(parsed, list):
        return parsed

    if not isinstance(parsed, dict):
        return None

    if isinstance(parsed.get("steps"), list):
        return parsed["steps"]

    for key in ("instructions", "suggested_steps", "items", "tasks"):
        value = parsed.get(key)
        if isinstance(value, list):
            return value

    
    for value in parsed.values():
        if isinstance(value, list):
            return value

    return None


def _build_prompt(title, description, status):
    return (
        "You generate task suggestions for a productivity app.\n"
        "Return ONLY a valid JSON array of strings and nothing else.\n"
        "Do not return markdown, labels, explanations, or wrapper objects.\n"
        "For active tasks, return between 1 and 10 short actionable steps.\n"
        "If status is done, return [] exactly.\n"
        f"Task title: {title.strip()}\n"
        f"Task description: {description.strip()}\n"
        f"Task status: {status}\n"
        "Status guidance:\n"
        "- todo: suggest planning and first execution steps\n"
        "- in-progress: suggest immediate next actions and unblockers\n"
        "- done: return []\n"
        "Output format example: [\"Step 1\", \"Step 2\"]"
    )


def _build_repair_prompt(previous_response):
    return (
        "Your previous output was invalid.\n"
        "Return ONLY a valid JSON array of strings and nothing else.\n"
        "No wrapper object. No markdown. No explanation text.\n"
        "If you are unsure, return [].\n"
        f"Previous output: {previous_response}"
    )


def _call_ollama(prompt):
    model_name = _resolve_model_name()
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0},
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{OLLAMA_BASE_URL}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as response:
        raw = response.read().decode("utf-8")

    decoded = json.loads(raw)
    if "response" not in decoded:
        raise ValueError("Ollama response missing response field.")

    return decoded["response"]


def _parse_steps(response_text):
    
    parsed_steps = _extract_steps_from_text(response_text)
    if not parsed_steps:
        return []

    steps = []
    for item in parsed_steps:
        if not isinstance(item, str):
            item = str(item)
        cleaned = item.strip()
        if cleaned:
            steps.append(cleaned)

    return steps[:10]


def generate_suggested_steps(title, description, status):
    if status == "done":
        return [], None

    prompt = _build_prompt(title, description, status)

    try:
        first_response = _call_ollama(prompt)
        steps = _parse_steps(first_response)
        if steps:
            return steps, None

        repair_response = _call_ollama(_build_repair_prompt(first_response))
        repaired_steps = _parse_steps(repair_response)
        return repaired_steps, None
    except (ValueError, json.JSONDecodeError, error.URLError, TimeoutError) as exc:
        return [], str(exc)
    except Exception as exc:  
        return [], str(exc)
