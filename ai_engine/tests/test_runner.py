import asyncio
import json

import pytest
from pydantic import ValidationError

from ai_engine.agents import AgentFactory, run_agents
from ai_engine.llm import LLMProvider, MockLLMProvider
from ai_engine.personas import generate_personas

PRODUCT = {
    "product_id": "PROD001",
    "name": "FitTrack Smartwatch",
    "description": "Affordable smartwatch with fitness tracking",
    "category": "Wearable Technology",
    "price": 4999,
    "currency": "INR",
    "features": ["Heart rate monitoring"],
}

GOOD_JSON = json.dumps({
    "interest_score": 80, "purchase_intent": 60, "price_acceptance": 40,
    "perceived_usefulness": 85, "design_appeal": 70, "would_recommend": True,
    "positive_factors": ["Good battery"], "negative_factors": ["Pricey"],
    "reasoning": "Useful, but I would wait for a discount.",
})


class TrackingLLM(LLMProvider):
    """Fake LLM that records how many calls are running at the same moment."""

    def __init__(self):
        self.running = 0
        self.max_running = 0

    async def generate(self, prompt: str) -> str:
        self.running += 1
        self.max_running = max(self.max_running, self.running)
        await asyncio.sleep(0.02)
        self.running -= 1
        return GOOD_JSON


def test_factory_creates_one_agent_per_persona():
    personas = generate_personas({}, 10, seed=1)
    agents = AgentFactory.create_agents(personas, MockLLMProvider([GOOD_JSON]))
    assert len(agents) == 10


def test_factory_rejects_invalid_persona():
    with pytest.raises(ValidationError):
        AgentFactory.create_agents([{"persona_id": "P1", "age": 15}], MockLLMProvider([GOOD_JSON]))


def test_runner_returns_all_results_in_order():
    personas = generate_personas({}, 12, seed=2)
    agents = AgentFactory.create_agents(personas, MockLLMProvider([GOOD_JSON]))
    results = asyncio.run(run_agents(agents, PRODUCT, max_concurrent=5))
    assert len(results) == 12
    assert [r["persona_id"] for r in results] == [p["persona_id"] for p in personas]
    assert all(r["status"] == "ok" for r in results)


def test_runner_respects_concurrency_limit():
    llm = TrackingLLM()
    agents = AgentFactory.create_agents(generate_personas({}, 20, seed=3), llm)
    asyncio.run(run_agents(agents, PRODUCT, max_concurrent=4))
    assert 1 < llm.max_running <= 4


def test_failed_agents_do_not_stop_the_others():
    personas = generate_personas({}, 5, seed=4)
    good = AgentFactory.create_agents(personas[:3], MockLLMProvider([GOOD_JSON]))
    bad = AgentFactory.create_agents(personas[3:], MockLLMProvider(["garbage"]))
    results = asyncio.run(run_agents(good + bad, PRODUCT, max_concurrent=2))
    assert [r["status"] for r in results] == ["ok", "ok", "ok", "invalid", "invalid"]


def test_progress_callback_reports_counts():
    personas = generate_personas({}, 5, seed=5)
    good = AgentFactory.create_agents(personas[:3], MockLLMProvider([GOOD_JSON]))
    bad = AgentFactory.create_agents(personas[3:], MockLLMProvider(["garbage"]))
    calls = []
    asyncio.run(run_agents(good + bad, PRODUCT, max_concurrent=2,
                           on_progress=lambda done, failed, total: calls.append((done, failed, total))))
    assert [c[0] for c in calls] == [1, 2, 3, 4, 5]
    assert calls[-1] == (5, 2, 5)
