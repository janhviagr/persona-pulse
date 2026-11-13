import asyncio
import json

from ai_engine.agents import AgentFactory
from ai_engine.evaluation import WEIGHTS
from ai_engine.llm import MockLLMProvider
from ai_engine.personas import generate_personas
from ai_engine.simulation import SimulationManager


PRODUCT = {
    "product_id": "PROD001",
    "name": "FitTrack Smartwatch",
    "description": "Smartwatch with fitness tracking",
    "category": "Wearable Technology",
    "price": 4999,
    "currency": "INR",
    "features": ["Heart rate monitoring"],
}
VALID_REPLY = json.dumps({
    "interest_score": 80,
    "purchase_intent": 60,
    "price_acceptance": 50,
    "perceived_usefulness": 90,
    "design_appeal": 70,
    "would_recommend": True,
    "positive_factors": ["Useful fitness tracking"],
    "negative_factors": ["Price is high"],
    "reasoning": "Useful features, but the price is high.",
})


def test_manager_reuses_runner_validates_results_and_forwards_progress():
    personas = generate_personas({}, 2, seed=11)
    llm = MockLLMProvider([VALID_REPLY, "not json"])
    agents = AgentFactory.create_agents(personas, llm)
    progress = []

    result = asyncio.run(SimulationManager(llm=llm, max_concurrent=2).run(
        PRODUCT,
        agents=agents,
        simulation_id="SIM-P4",
        on_progress=lambda completed, failed, total: progress.append((completed, failed, total)),
    ))

    assert result["simulation_id"] == "SIM-P4"
    assert result["total"] == 2
    assert result["sample_size"] == 1
    assert result["failed"] == 1
    assert result["report"]["overall_score"] == 69.0
    assert len(result["valid_responses"]) == 1
    assert len(result["failures"]) == 1
    assert sorted(row[0] for row in progress) == [1, 2]
    assert progress[-1] == (2, 1, 2)


def test_manager_reports_19_valid_and_one_invalid_without_scoring_failure():
    personas = generate_personas({}, 20, seed=12)
    valid_personas = personas[:19]
    valid_agents = AgentFactory.create_agents(valid_personas, MockLLMProvider([VALID_REPLY]))
    invalid_agents = AgentFactory.create_agents(personas[19:], MockLLMProvider(["not json"]))
    agents = valid_agents + invalid_agents

    result = asyncio.run(SimulationManager(max_concurrent=5).run(
        PRODUCT, agents=agents, simulation_id="SIM-20"
    ))

    expected = sum(WEIGHTS[field] * value for field, value in {
        "interest_score": 80,
        "purchase_intent": 60,
        "price_acceptance": 50,
        "perceived_usefulness": 90,
        "design_appeal": 70,
    }.items())
    assert result["sample_size"] == 19
    assert result["failed"] == 1
    assert result["report"]["failed_responses"] == 1
    assert result["report"]["overall_score"] == expected
    assert result["report"]["metrics"]["price_acceptance"] == 50
    assert result["report"]["metrics"]["purchase_intent"] == 60


def test_manager_requires_count_when_person3_entrypoint_is_used():
    try:
        asyncio.run(SimulationManager().run(PRODUCT))
    except ValueError as error:
        assert "count must be" in str(error)
    else:
        raise AssertionError("Missing count should be rejected")
