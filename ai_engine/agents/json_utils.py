import json


def extract_json(text: str) -> dict:
    """Find the JSON object inside an LLM reply and return it as a dict."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in the reply")
    data = json.loads(text[start : end + 1])
    if not isinstance(data, dict):
        raise ValueError("Reply JSON is not an object")
    return data
