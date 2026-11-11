import asyncio
import json

from ai_engine.agents import evaluate_price_scenarios
from ai_engine.llm import MockLLMProvider

PRODUCT = {
    "product_id": "PROD001", "name": "FitTrack Smartwatch",
    "description": "Smartwatch with fitness tracking", "category": "Wearable Technology",
    "price": 4999, "currency": "INR", "features": ["Heart rate monitoring"],
}
GOOD_JSON = json.dumps({
    "reasoning": "Fine.", "interest_score": 70, "purchase_intent": 50,
    "price_acceptance": 50, "perceived_usefulness": 70, "design_appeal": 60,
    "would_recommend": True, "positive_factors": [], "negative_factors": [],
})
CONFIG = {"age_groups": ["18-24"]}
PRICES = [1999, 3999, 5999]


def run(llm):
    return asyncio.run(evaluate_price_scenarios(PRODUCT, CONFIG, 4, PRICES, llm=llm, seed=1))


def test_one_scenario_per_price_in_order():
    out = run(MockLLMProvider([GOOD_JSON]))
    assert [s["price"] for s in out["scenarios"]] == PRICES
    assert all(s["total"] == 4 and s["failed"] == 0 for s in out["scenarios"])


def test_same_personas_in_every_scenario():
    out = run(MockLLMProvider([GOOD_JSON]))
    ids = [p["persona_id"] for p in out["personas"]]
    for scenario in out["scenarios"]:
        assert [r["persona_id"] for r in scenario["responses"]] == ids


def test_each_price_reaches_the_prompt():
    llm = MockLLMProvider([GOOD_JSON])
    run(llm)
    assert len(llm.prompts) == 12  # 4 personas x 3 prices
    for price in PRICES:
        assert any(f"Price: {price} INR" in prompt for prompt in llm.prompts)
    assert not any("Price: 4999 INR" in prompt for prompt in llm.prompts)


def test_original_product_is_not_modified():
    run(MockLLMProvider([GOOD_JSON]))
    assert PRODUCT["price"] == 4999
