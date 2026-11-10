import pytest
from pydantic import ValidationError

from ai_engine.personas import Persona
from ai_engine.agents import AgentResponse


def make_persona(**overrides):
    data = dict(
        persona_id="P001", age=21, occupation="Student",
        interests=["technology"], personality_traits=["curious"],
        price_sensitivity=0.8, technical_literacy=0.9,
    )
    data.update(overrides)
    return Persona(**data)


def make_response(**overrides):
    data = dict(
        persona_id="P001", interest_score=80, purchase_intent=60,
        price_acceptance=50, perceived_usefulness=85, design_appeal=70,
        reasoning="Useful but slightly expensive.",
    )
    data.update(overrides)
    return AgentResponse(**data)


def test_valid_persona():
    assert make_persona().persona_id == "P001"


def test_persona_rejects_underage():
    with pytest.raises(ValidationError):
        make_persona(age=15)


def test_persona_rejects_trait_above_one():
    with pytest.raises(ValidationError):
        make_persona(price_sensitivity=1.5)


def test_persona_missing_required_field():
    with pytest.raises(ValidationError):
        Persona(persona_id="P001", age=21)


def test_valid_response():
    assert make_response().purchase_intent == 60


def test_response_rejects_score_above_100():
    with pytest.raises(ValidationError):
        make_response(interest_score=150)


def test_response_missing_reasoning():
    with pytest.raises(ValidationError):
        AgentResponse(
            persona_id="P001", interest_score=80, purchase_intent=60,
            price_acceptance=50, perceived_usefulness=85, design_appeal=70,
        )
