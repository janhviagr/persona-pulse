"""Deterministic analytics over Person 3's persona and response models."""

from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from statistics import mean
from typing import Any

from pydantic import ValidationError

from ai_engine.agents.response_model import AgentResponse
from ai_engine.personas.persona_model import Persona

WEIGHTS = {
    "interest_score": 0.25,
    "purchase_intent": 0.25,
    "price_acceptance": 0.20,
    "perceived_usefulness": 0.15,
    "design_appeal": 0.15,
}
SCORE_FIELDS = tuple(WEIGHTS)
LIMITATIONS = [
    "Results are simulated consumer insights, not real market research.",
    "The composite score is not a validated probability of commercial success.",
    "Scores depend on the LLM and prompts used and may reflect model bias.",
    "No calibration against real consumer data has been done.",
]


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="python")
    raise TypeError("Expected a mapping or a Pydantic model")


def _round(value: float) -> float:
    return round(float(value), 2)


def _average(values: Sequence[float]) -> float:
    return _round(mean(values)) if values else 0.0


def _age_group(age: int) -> str:
    if age < 18:
        return "<18"
    if age >= 55:
        return "55+"
    lower = 18 if age <= 24 else 25 + ((age - 25) // 10) * 10
    upper = 24 if lower == 18 else lower + 9
    return f"{lower}-{upper}"


def _trait_bucket(value: float) -> str:
    return "low" if value < 1 / 3 else "medium" if value < 2 / 3 else "high"


def validate_responses(
    responses: Sequence[Any], persona_ids: set[str] | None = None
) -> tuple[list[dict[str, Any]], int]:
    """Return only schema-valid successful responses and the rejected count.

    ``status`` and ``product_id`` are emitted by Person 3's runner but are not
    required fields on its public AgentResponse model, so this boundary checks
    them explicitly. Non-``ok`` statuses and responses without a matching
    supplied persona are rejected.
    """
    valid: list[dict[str, Any]] = []
    failed = 0
    for item in responses:
        try:
            raw = _as_dict(item)
            if raw.get("status") != "ok" or not raw.get("product_id"):
                failed += 1
                continue
            if hasattr(item, "model_fields_set"):
                recommendation_reported = "would_recommend" in item.model_fields_set
            else:
                recommendation_reported = "would_recommend" in raw
            response = AgentResponse.model_validate(
                {key: value for key, value in raw.items() if key != "status"}
            )
            if persona_ids is not None and response.persona_id not in persona_ids:
                failed += 1
                continue
        except (ValidationError, TypeError, ValueError):
            failed += 1
            continue
        normalized = response.model_dump(mode="python")
        if not recommendation_reported:
            # AgentResponse defaults this field to False; preserve omission for
            # analytics instead of treating the default as an explicit answer.
            normalized["would_recommend"] = None
        valid.append(normalized)
    return valid, failed


def _score(response: Mapping[str, Any]) -> float:
    return sum(WEIGHTS[field] * float(response[field]) for field in SCORE_FIELDS)


def calculate_scores(responses: Sequence[Any]) -> dict[str, float]:
    """Calculate the specified composite and component means from valid rows."""
    valid, _ = validate_responses(responses)
    metrics = {
        "overall_score": _average([_score(response) for response in valid]),
        "interest_score": _average([response["interest_score"] for response in valid]),
        # Keep the backend fallback's established alias while exposing the
        # Person 3 field name directly.
        "product_appeal": _average([response["interest_score"] for response in valid]),
        "purchase_intent": _average([response["purchase_intent"] for response in valid]),
        "price_acceptance": _average([response["price_acceptance"] for response in valid]),
        "perceived_usefulness": _average([response["perceived_usefulness"] for response in valid]),
        "design_appeal": _average([response["design_appeal"] for response in valid]),
    }
    recommendation_values = [
        100.0 if response["would_recommend"] else 0.0
        for response in valid
        if response["would_recommend"] is not None
    ]
    if recommendation_values:
        recommendation_intent = _average(recommendation_values)
        metrics["recommendation_intent"] = recommendation_intent
        metrics["recommendation_rate"] = recommendation_intent
    return metrics


def analyze_segments(
    responses: Sequence[Mapping[str, Any]], personas: Sequence[Mapping[str, Any]]
) -> dict[str, dict[str, dict[str, float | int]]]:
    """Aggregate valid responses by attributes that exist on Person 3's Persona."""
    persona_by_id: dict[str, dict[str, Any]] = {}
    for item in personas:
        try:
            persona = Persona.model_validate(_as_dict(item)).model_dump(mode="python")
        except (ValidationError, TypeError, ValueError):
            continue
        persona_by_id[persona["persona_id"]] = persona

    dimensions: dict[str, dict[str, list[Mapping[str, Any]]]] = {
        "age_group": defaultdict(list),
        "occupation": defaultdict(list),
        "income_level": defaultdict(list),
        "location_type": defaultdict(list),
        "interest": defaultdict(list),
        "price_sensitivity": defaultdict(list),
    }
    for response in responses:
        persona = persona_by_id.get(response["persona_id"])
        if persona is None:
            continue
        dimensions["age_group"][_age_group(persona["age"])].append(response)
        for key, field in (
            ("occupation", "occupation"),
            ("income_level", "income_level"),
            ("location_type", "location_type"),
        ):
            if persona[field]:
                dimensions[key][persona[field]].append(response)
        for interest in persona["interests"]:
            dimensions["interest"][interest].append(response)
        dimensions["price_sensitivity"][_trait_bucket(persona["price_sensitivity"])].append(response)

    analysis: dict[str, dict[str, dict[str, float | int]]] = {}
    for dimension, groups in dimensions.items():
        analysis[dimension] = {}
        for label, group in sorted(groups.items()):
            analysis[dimension][label] = {
                "sample_size": len(group),
                "average_overall_score": _average([_score(response) for response in group]),
                "average_purchase_intent": _average([response["purchase_intent"] for response in group]),
                "average_price_acceptance": _average([response["price_acceptance"] for response in group]),
            }
    return analysis


def analyze_pricing(
    product: Mapping[str, Any],
    responses: Sequence[Mapping[str, Any]],
    personas: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Summarize observed response against the submitted product price only."""
    persona_by_id: dict[str, dict[str, Any]] = {}
    for item in personas:
        try:
            persona = Persona.model_validate(_as_dict(item)).model_dump(mode="python")
        except (ValidationError, TypeError, ValueError):
            continue
        persona_by_id[persona["persona_id"]] = persona

    by_sensitivity: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for response in responses:
        persona = persona_by_id.get(response["persona_id"])
        if persona is not None:
            by_sensitivity[_trait_bucket(persona["price_sensitivity"])].append(response)

    product_price = product.get("price")
    try:
        numeric_price = float(product_price) if product_price is not None else None
        if numeric_price is not None and numeric_price < 0:
            numeric_price = None
    except (TypeError, ValueError):
        numeric_price = None

    return {
        "product_price": numeric_price,
        "currency": product.get("currency"),
        "mean_price_acceptance": _average([response["price_acceptance"] for response in responses]),
        "mean_purchase_intent": _average([response["purchase_intent"] for response in responses]),
        "price_acceptance_by_price_sensitivity": {
            label: _average([response["price_acceptance"] for response in group])
            for label, group in sorted(by_sensitivity.items())
        },
        "pricing_scenario_analysis_supported": False,
    }


def _factor_counts(responses: Sequence[Mapping[str, Any]], field: str) -> list[dict[str, Any]]:
    labels: dict[str, str] = {}
    counts: Counter[str] = Counter()
    for response in responses:
        for factor in response.get(field) or []:
            normalized = " ".join(factor.split()).casefold()
            if normalized:
                counts[normalized] += 1
                labels.setdefault(normalized, " ".join(factor.split()))
    return [
        {"factor": labels[key], "count": count}
        for key, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def analyze_factors(responses: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    reasoning_labels: dict[str, str] = {}
    reasoning_counts: Counter[str] = Counter()
    for response in responses:
        reasoning = " ".join(response["reasoning"].split())
        normalized = reasoning.casefold()
        if normalized:
            reasoning_counts[normalized] += 1
            reasoning_labels.setdefault(normalized, reasoning)
    return {
        "positive_factors": _factor_counts(responses, "positive_factors"),
        "negative_factors": _factor_counts(responses, "negative_factors"),
        "reasoning_responses": sum(bool(response["reasoning"].strip()) for response in responses),
        "recurring_reasoning": [
            {"reasoning": reasoning_labels[key], "count": count}
            for key, count in sorted(reasoning_counts.items(), key=lambda item: (-item[1], item[0]))
            if count > 1
        ],
    }


def generate_recommendations(
    metrics: Mapping[str, float],
    segments: Mapping[str, Mapping[str, Mapping[str, float | int]]],
    factors: Mapping[str, Any],
    sample_size: int,
) -> list[str]:
    """Generate cautious, deterministic next steps tied to calculated evidence."""
    if sample_size == 0:
        return ["The simulated sample has no valid responses; collect valid evaluations before drawing conclusions."]

    recommendations: list[str] = []
    if metrics["purchase_intent"] < 50:
        recommendations.append(
            f"Simulated consumers indicate weak purchase intent (average {metrics['purchase_intent']:.1f}/100); review the value proposition."
        )
    if metrics["perceived_usefulness"] >= 70 and metrics["price_acceptance"] < 50:
        recommendations.append(
            "Within this simulated sample, usefulness is strong while price acceptance is weak; test the stated price with a new simulation."
        )
    recommendation_intent = metrics.get("recommendation_intent")
    if recommendation_intent is not None and recommendation_intent >= 65:
        recommendations.append(
            f"Simulated consumers show a strong recommendation intent ({recommendation_intent:.1f}%)."
        )

    recurring = [entry["factor"] for entry in factors["negative_factors"] if entry["count"] >= 2]
    if recurring:
        recommendations.append("Investigate recurring simulated concerns: " + "; ".join(recurring[:3]) + ".")

    age_segments = segments.get("age_group", {})
    eligible = [(label, data) for label, data in age_segments.items() if data["sample_size"] >= 2]
    if len(eligible) >= 2:
        best_label, best = max(eligible, key=lambda item: item[1]["average_overall_score"])
        low_label, low = min(eligible, key=lambda item: item[1]["average_overall_score"])
        difference = best["average_overall_score"] - low["average_overall_score"]
        if difference >= 15:
            recommendations.append(
                f"The simulated {best_label} segment scores {difference:.1f} points above {low_label}; consider investigating this segment further."
            )

    if not recommendations:
        recommendations.append("The current simulated sample does not show a threshold-based action; review segment and factor results for context.")
    return recommendations


def generate_report(
    simulation_id: str,
    product: Mapping[str, Any],
    personas: Sequence[Any],
    responses: Sequence[Any],
) -> dict[str, Any]:
    """Build the report expected by backend.app.services.report_service.

    Invalid personas are ignored for matching and segmentation. Responses that
    fail the real Person 3 model, carry an invalid status, or refer to an
    unknown persona are excluded from every analytic and counted as failed.
    """
    normalized_personas: list[dict[str, Any]] = []
    for item in personas:
        try:
            normalized_personas.append(Persona.model_validate(_as_dict(item)).model_dump(mode="python"))
        except (ValidationError, TypeError, ValueError):
            continue
    known_ids = {persona["persona_id"] for persona in normalized_personas}
    valid, rejected = validate_responses(responses, known_ids)

    metrics = calculate_scores(valid)
    segments = analyze_segments(valid, normalized_personas)
    pricing = analyze_pricing(product, valid, normalized_personas)
    factors = analyze_factors(valid)
    recommendations = generate_recommendations(metrics, segments, factors, len(valid))

    rec_values = [response["would_recommend"] for response in valid]
    recommendation_distribution = {
        "would_recommend": sum(value is True for value in rec_values),
        "would_not_recommend": sum(value is False for value in rec_values),
        "not_reported": sum(value is None for value in rec_values),
    }
    failed = rejected + max(0, len(normalized_personas) - len(valid) - rejected)
    limitations = list(LIMITATIONS)
    limitations.append(
        "The required sentiment_distribution field summarizes recommendation responses; the response model provides no independent sentiment score."
    )
    if not valid:
        limitations.append("No valid response data was available for analytics.")
    limitations.append(
        "The product contains one submitted price; price sensitivity is descriptive and no alternate price scenarios were evaluated."
    )

    return {
        "simulation_id": simulation_id,
        "overall_score": metrics.pop("overall_score"),
        "metrics": metrics,
        "segment_analysis": segments,
        "pricing_analysis": pricing,
        # Retain the required contract field, but label its contents accurately:
        # recommendation answers do not establish textual sentiment.
        "sentiment_distribution": {"recommendation_responses": recommendation_distribution},
        "factor_analysis": factors,
        "recommendations": recommendations,
        "sample_size": len(valid),
        "failed_responses": failed,
        "unavailable_metrics": (
            [] if "recommendation_intent" in metrics else ["recommendation_intent"]
        ),
        "limitations": limitations,
    }
