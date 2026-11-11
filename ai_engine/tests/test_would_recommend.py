import asyncio
import json

from ai_engine.agents import ConsumerAgent
from ai_engine.llm import MockLLMProvider
from ai_engine.personas import generate_personas

PRODUCT = {
    "product_id": "PROD001", "name": "FitTrack Smartwatch",
    "description": "Smartwatch with fitness tracking", "category": "Wearable Technology",
    "price": 4999, "currency": "INR", "features": ["Heart rate monitoring"],
}
PERSONA = generate_personas({"age_groups": ["18-24"]}, 1, seed=1)[0]

BASE = {
    "reasoning": "Useful, but I would wait for a discount.",
    "interest_score": 80, "purchase_intent": 60, "price_acceptance": 40,
    "perceived_usefulness": 85, "design_appeal": 70,
    "positive_factors": ["Good battery"], "negative_factors": ["Pricey"],
}


def run(reply: dict) -> dict:
    llm = MockLLMProvider([json.dumps(reply)])
    return asyncio.run(ConsumerAgent(PERSONA, llm).evaluate_product(PRODUCT))


def test_true_is_kept():
    result = run({**BASE, "would_recommend": True})
    assert result["status"] == "ok"
    assert result["would_recommend"] is True


def test_false_is_kept():
    result = run({**BASE, "would_recommend": False})
    assert result["status"] == "ok"
    assert "would_recommend" in result
    assert result["would_recommend"] is False


def test_missing_is_left_out():
    result = run(BASE)
    assert result["status"] == "ok"
    assert "would_recommend" not in result


def test_ids_and_status_still_present_when_field_missing():
    result = run(BASE)
    assert result["persona_id"] == PERSONA["persona_id"]
    assert result["product_id"] == "PROD001"
    assert result["status"] == "ok"
