from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


def _load(filename: str) -> str:
    return (PROMPT_DIR / filename).read_text(encoding="utf-8")


def _render(template: str, values: dict) -> str:
    # Plain replace (not str.format) because the JSON example contains braces.
    for key, value in values.items():
        template = template.replace("{" + key + "}", str(value))
    return template


def _join(items, fallback="none"):
    return ", ".join(items) if items else fallback


def build_prompt(persona: dict, product: dict) -> str:
    """Combine one persona and one product into the full prompt text."""
    persona_values = {
        "name": persona.get("name") or "an anonymous customer",
        "age": persona["age"],
        "occupation": persona["occupation"],
        "location_type": persona.get("location_type") or "urban",
        "income_level": persona.get("income_level") or "medium",
        "interests": _join(persona.get("interests")),
        "personality_traits": _join(persona.get("personality_traits")),
        "primary_motivation": persona.get("primary_motivation") or "value for money",
        "purchase_constraints": _join(persona.get("purchase_constraints")),
        "price_sensitivity": persona["price_sensitivity"],
        "technical_literacy": persona["technical_literacy"],
        "brand_loyalty": persona.get("brand_loyalty", 0.5),
        "innovation_preference": persona.get("innovation_preference", 0.5),
        "purchase_impulsiveness": persona.get("purchase_impulsiveness", 0.5),
    }
    features = "\n".join(f"- {f}" for f in product.get("features", [])) or "- (none listed)"
    product_values = {
        "product_name": product.get("name", "Unnamed product"),
        "category": product.get("category", "General"),
        "description": product.get("description", ""),
        "price": product.get("price", "unknown"),
        "currency": product.get("currency", ""),
        "features": features,
    }
    system_part = _render(_load("system_persona.txt"), persona_values)
    task_part = _render(_load("product_evaluation.txt"), product_values)
    return system_part + "\n\n" + task_part
