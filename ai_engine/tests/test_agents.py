import asyncio
import json
import re

from ai_engine.agents import ConsumerAgent
from ai_engine.agents.prompt_builder import build_prompt
from ai_engine.llm import MockLLMProvider
from ai_engine.personas import generate_personas

PRODUCT = {
    "product_id": "PROD001",
    "name": "FitTrack Smartwatch",
    "description": "Affordable smartwatch with fitness tracking",
    "category": "Wearable Technology",
    "price": 4999,
    "currency": "INR",
    "features": ["Heart rate monitoring", "Seven-day battery life"],
}

PERSONA = generate_personas({"age_groups": ["18-24"]}, 1, seed=1)[0]

GOOD = {
    "interest_score": 80, "purchase_intent": 60, "price_acceptance": 40,
    "perceived_usefulness": 85, "design_appeal": 70, "would_recommend": True,
    "positive_factors": ["Good battery"], "negative_factors": ["Pricey"],
    "reasoning": "Useful, but I would wait for a discount.",
}
GOOD_JSON = json.dumps(GOOD)


def run(llm):
    return asyncio.run(ConsumerAgent(PERSONA, llm).evaluate_product(PRODUCT))


def test_good_reply_is_accepted():
    result = run(MockLLMProvider([GOOD_JSON]))
    assert result["status"] == "ok"
    assert result["purchase_intent"] == 60


def test_reply_inside_code_fences_is_accepted():
    fenced = "Sure! Here you go:\n```json\n" + GOOD_JSON + "\n```"
    assert run(MockLLMProvider([fenced]))["status"] == "ok"


def test_agent_sets_its_own_ids():
    wrong_ids = json.dumps({**GOOD, "persona_id": "P999"})
    result = run(MockLLMProvider([wrong_ids]))
    assert result["persona_id"] == PERSONA["persona_id"]
    assert result["product_id"] == "PROD001"


def test_broken_reply_is_retried():
    llm = MockLLMProvider(["this is not json", GOOD_JSON])
    result = run(llm)
    assert result["status"] == "ok"
    assert llm.calls == 2


def test_hopeless_reply_is_marked_invalid_not_raised():
    llm = MockLLMProvider(["garbage"])
    result = run(llm)
    assert result["status"] == "invalid"
    assert result["persona_id"] == PERSONA["persona_id"]
    assert llm.calls == 3


def test_out_of_range_score_is_rejected():
    bad = json.dumps({**GOOD, "interest_score": 150})
    assert run(MockLLMProvider([bad]))["status"] == "invalid"


def test_missing_field_is_rejected():
    incomplete = {k: v for k, v in GOOD.items() if k != "reasoning"}
    assert run(MockLLMProvider([json.dumps(incomplete)]))["status"] == "invalid"


def test_prompt_contains_persona_and_product_and_no_leftover_placeholders():
    prompt = build_prompt(PERSONA, PRODUCT)
    assert str(PERSONA["age"]) in prompt
    assert "FitTrack Smartwatch" in prompt
    assert "4999" in prompt
    assert re.search(r"\{[a-z_]+\}", prompt) is None
