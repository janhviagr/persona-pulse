import asyncio
import json

from ai_engine.agents import evaluate_with_personas
from ai_engine.llm import MockLLMProvider

PRODUCT = {
    "product_id": "PROD001", "name": "FitTrack Smartwatch",
    "description": "Smartwatch with fitness tracking", "category": "Wearable Technology",
    "price": 4999, "currency": "INR", "features": ["Heart rate monitoring"],
}
GOOD_JSON = json.dumps({
    "reasoning": "Useful, but I would wait for a discount.",
    "interest_score": 80, "purchase_intent": 60, "price_acceptance": 40,
    "perceived_usefulness": 85, "design_appeal": 70, "would_recommend": True,
    "positive_factors": ["Good battery"], "negative_factors": ["Pricey"],
})
CONFIG = {"age_groups": ["18-24", "25-34"], "interests": ["fitness"]}


def test_returns_personas_and_matching_responses():
    out = asyncio.run(evaluate_with_personas(
        PRODUCT, CONFIG, 8, llm=MockLLMProvider([GOOD_JSON]), seed=1))
    assert out["total"] == 8 and out["failed"] == 0
    assert len(out["personas"]) == len(out["responses"]) == 8
    ids = [p["persona_id"] for p in out["personas"]]
    assert [r["persona_id"] for r in out["responses"]] == ids


def test_failed_agents_are_counted():
    out = asyncio.run(evaluate_with_personas(
        PRODUCT, CONFIG, 5, llm=MockLLMProvider(["garbage"]), seed=1))
    assert out["total"] == 5 and out["failed"] == 5
    assert all(r["status"] == "invalid" for r in out["responses"])
