import json

import pytest
from pydantic import ValidationError

from ai_engine.agents import AgentResponse
from ai_engine.evaluation import (
    analyze_factors,
    analyze_pricing,
    analyze_segments,
    calculate_scores,
    generate_recommendations,
    generate_report,
    validate_responses,
)
from ai_engine.personas import Persona


def persona(persona_id="P001", **overrides):
    values = {
        "persona_id": persona_id,
        "age": 22,
        "occupation": "Student",
        "interests": ["fitness", "technology"],
        "personality_traits": ["practical"],
        "price_sensitivity": 0.8,
        "technical_literacy": 0.7,
        "income_level": "Low",
        "location_type": "Urban",
    }
    values.update(overrides)
    return Persona(**values)


def response(persona_id="P001", **overrides):
    values = {
        "persona_id": persona_id,
        "interest_score": 80,
        "purchase_intent": 60,
        "price_acceptance": 40,
        "perceived_usefulness": 85,
        "design_appeal": 70,
        "reasoning": "Useful, but the submitted price is high for my budget.",
        "would_recommend": True,
        "positive_factors": ["Useful fitness tracking"],
        "negative_factors": ["Price is high"],
    }
    values.update(overrides)
    return AgentResponse(**values)


def valid_response(persona_id="P001", **overrides):
    values = response(persona_id, product_id="PROD001", **overrides).model_dump()
    return {**values, "status": "ok"}


def test_composite_scoring_uses_documented_weights_and_response_model():
    result = calculate_scores([valid_response()])
    assert result["overall_score"] == pytest.approx(66.25)
    assert result["interest_score"] == 80
    assert result["product_appeal"] == 80
    assert result["recommendation_rate"] == 100
    assert result["recommendation_intent"] == 100
    assert response().purchase_intent == 60


def test_invalid_responses_are_excluded_and_counted():
    valid, failed = validate_responses([
        valid_response(),
        {"persona_id": "P002", "status": "invalid", "error": "bad JSON"},
        {**valid_response("P003"), "interest_score": 101},
    ])
    assert len(valid) == 1
    assert failed == 2
    assert calculate_scores([
        valid_response(),
        {"persona_id": "P002", "status": "invalid"},
    ])["purchase_intent"] == 60
    with pytest.raises(ValidationError):
        AgentResponse(**{**response().model_dump(), "interest_score": 101})


def test_response_requires_ok_status_and_product_id():
    missing_status = valid_response()
    missing_status.pop("status")
    missing_product_id = valid_response()
    missing_product_id.pop("product_id")

    valid, failed = validate_responses([missing_status, missing_product_id])

    assert valid == []
    assert failed == 2


def test_segment_analysis_uses_available_persona_attributes():
    personas = [persona(), persona("P002", age=38, occupation="Nurse", interests=["health"])]
    responses = [valid_response(), valid_response("P002", purchase_intent=40, price_acceptance=30)]
    result = analyze_segments(responses, personas)
    assert result["age_group"]["18-24"]["sample_size"] == 1
    assert result["age_group"]["35-44"]["average_purchase_intent"] == 40
    assert result["interest"]["health"]["sample_size"] == 1
    assert "occupation" in result and "income_level" in result


def test_pricing_analysis_uses_product_and_persona_response_data_only():
    result = analyze_pricing(
        {"price": 4999, "currency": "INR"}, [valid_response()], [persona()]
    )
    assert result["product_price"] == 4999
    assert result["mean_price_acceptance"] == 40
    assert result["mean_purchase_intent"] == 60
    assert result["price_acceptance_by_price_sensitivity"] == {"high": 40}
    assert result["pricing_scenario_analysis_supported"] is False


def test_factor_analysis_counts_actual_factors_case_insensitively():
    result = analyze_factors([
        valid_response(), valid_response("P002", positive_factors=[" useful   FITNESS tracking "])
    ])
    assert result["positive_factors"] == [{"factor": "Useful fitness tracking", "count": 2}]
    assert result["negative_factors"] == [{"factor": "Price is high", "count": 2}]
    assert result["recurring_reasoning"] == [{
        "reasoning": "Useful, but the submitted price is high for my budget.", "count": 2
    }]


def test_factor_analysis_accepts_omitted_or_null_optional_factor_lists():
    data = response().model_dump(exclude={"positive_factors", "negative_factors"})
    result = analyze_factors([data, {**data, "positive_factors": None, "negative_factors": None}])
    assert result["positive_factors"] == []
    assert result["negative_factors"] == []


def test_recommendations_are_traceable_to_analytics():
    metrics = {
        "purchase_intent": 40,
        "perceived_usefulness": 80,
        "price_acceptance": 35,
        "recommendation_intent": 75,
    }
    recommendations = generate_recommendations(
        metrics,
        {"age_group": {}},
        {"negative_factors": [{"factor": "Price is high", "count": 2}]},
        3,
    )
    assert any("purchase intent" in item for item in recommendations)
    assert any("price acceptance" in item for item in recommendations)
    assert any("Price is high" in item for item in recommendations)
    assert all("simulation" in item.lower() or "simulated" in item.lower() for item in recommendations)


def test_report_shape_counts_failed_responses_and_is_json_serializable():
    report = generate_report(
        "SIM001",
        {"price": 4999, "currency": "INR"},
        [persona(), persona("P002", age=36, occupation="Nurse")],
        [
            valid_response(),
            {"persona_id": "P002", "status": "invalid", "error": "bad JSON"},
        ],
    )
    serialized = json.dumps(report)
    assert report["overall_score"] == pytest.approx(66.25)
    assert report["sample_size"] == 1
    assert report["failed_responses"] == 1
    assert "sentiment_distribution" in report  # required by the existing report contract
    assert "factor_analysis" in report
    assert json.loads(serialized)["simulation_id"] == "SIM001"


def test_absent_recommendation_is_reported_unavailable():
    data = {**response(product_id="PROD001").model_dump(exclude={"would_recommend"}), "status": "ok"}
    metrics = calculate_scores([data])
    assert "recommendation_intent" not in metrics

    report = generate_report("SIM003", {"price": 20}, [persona()], [data])
    assert report["unavailable_metrics"] == ["recommendation_intent"]
    assert report["sentiment_distribution"]["recommendation_responses"]["not_reported"] == 1


def test_explicit_negative_recommendation_is_counted_as_negative():
    data = valid_response(would_recommend=False)
    report = generate_report("SIM004", {"price": 20}, [persona()], [data])

    assert report["metrics"]["recommendation_intent"] == 0
    assert report["sentiment_distribution"]["recommendation_responses"] == {
        "would_recommend": 0,
        "would_not_recommend": 1,
        "not_reported": 0,
    }


def test_report_rejects_responses_for_unknown_personas():
    report = generate_report(
        "SIM002", {"price": 20}, [persona()], [valid_response("UNKNOWN")]
    )
    assert report["sample_size"] == 0
    assert report["failed_responses"] == 1
    assert "No valid response data was available for analytics." in report["limitations"]
