"""Report building.

Person 4 owns ai_engine/evaluation. If `generate_report` exists there, we call it.
Otherwise a minimal built-in aggregator runs so the pipeline works end to end.
The built-in report is computed from REAL agent responses only (never mock data)
and says so in `limitations`.
"""
from collections import Counter, defaultdict
from statistics import mean
from typing import Any

try:  # Person 4's engine
    from ai_engine.evaluation import generate_report as _p4_generate_report
except ImportError:
    _p4_generate_report = None

LIMITATIONS = [
    "Results are simulated consumer insights, not real market research.",
    "The composite score is simulated product readiness, not a validated probability of commercial success.",
    "Scores depend on the LLM and prompts used and may reflect model bias.",
]

W = {"A": 0.25, "P": 0.25, "C": 0.20, "U": 0.15, "D": 0.15}


def composite(r: dict[str, Any]) -> float:
    return (
        W["A"] * r["interest_score"]
        + W["P"] * r["purchase_intent"]
        + W["C"] * r["price_acceptance"]
        + W["U"] * r["perceived_usefulness"]
        + W["D"] * r["design_appeal"]
    )


def _age_group(age: int) -> str:
    for lo, hi in [(18, 24), (25, 34), (35, 44), (45, 54)]:
        if lo <= age <= hi:
            return f"{lo}-{hi}"
    return "55+" if age >= 55 else "<18"


def _avg(xs: list[float]) -> float:
    return round(mean(xs), 2) if xs else 0.0


def build_report(
    simulation_id: str,
    product: dict[str, Any],
    personas: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    failed: int,
    total: int,
) -> dict[str, Any]:
    if _p4_generate_report is not None:
        # ASSUMPTION: confirm exact signature with Person 4 and adjust here.
        report = _p4_generate_report(simulation_id, product, personas, responses)
        report = dict(report)
        report.setdefault("simulation_id", simulation_id)
        return report
    return _fallback_report(simulation_id, product, personas, responses, failed, total)


def _fallback_report(simulation_id, product, personas, responses, failed, total):
    by_pid = {p["persona_id"]: p for p in personas}
    scores = [composite(r) for r in responses]
    metrics = {
        "product_appeal": _avg([r["interest_score"] for r in responses]),
        "purchase_intent": _avg([r["purchase_intent"] for r in responses]),
        "price_acceptance": _avg([r["price_acceptance"] for r in responses]),
        "perceived_usefulness": _avg([r["perceived_usefulness"] for r in responses]),
        "design_appeal": _avg([r["design_appeal"] for r in responses]),
        "recommendation_intent": _avg(
            [100.0 if r.get("would_recommend") else 0.0 for r in responses if r.get("would_recommend") is not None]
        ),
    }

    seg_age: dict[str, list[float]] = defaultdict(list)
    seg_interest: dict[str, list[float]] = defaultdict(list)
    seg_occ: dict[str, list[float]] = defaultdict(list)
    price_sens: dict[str, list[float]] = defaultdict(list)
    for r, s in zip(responses, scores):
        p = by_pid.get(r["persona_id"])
        if not p:
            continue
        seg_age[_age_group(p["age"])].append(s)
        seg_occ[p["occupation"]].append(s)
        for i in p["interests"]:
            seg_interest[i].append(s)
        ps = p["price_sensitivity"]
        bucket = "low" if ps < 0.34 else "medium" if ps < 0.67 else "high"
        price_sens[bucket].append(r["price_acceptance"])

    def seg(d):
        return {k: {"score": _avg(v), "n": len(v)} for k, v in sorted(d.items())}

    pos = [s for s in scores if s >= 67]
    neg = [s for s in scores if s <= 33]
    sentiment = {
        "positive": len(pos),
        "neutral": len(scores) - len(pos) - len(neg),
        "negative": len(neg),
    }

    neg_counts = Counter(f for r in responses for f in r.get("negative_factors", []))
    pos_counts = Counter(f for r in responses for f in r.get("positive_factors", []))
    recs = []
    if neg_counts:
        recs.append("Address the most common concerns: " + "; ".join(f for f, _ in neg_counts.most_common(3)))
    if pos_counts:
        recs.append("Lead marketing with: " + "; ".join(f for f, _ in pos_counts.most_common(3)))
    if seg_age:
        best = max(seg_age.items(), key=lambda kv: mean(kv[1]))
        recs.append(f"Strongest simulated response from age group {best[0]}.")
    if metrics["price_acceptance"] < 50:
        recs.append("Price acceptance is low; consider testing lower price points.")

    return {
        "simulation_id": simulation_id,
        "overall_score": _avg(scores),
        "metrics": metrics,
        "segment_analysis": {
            "age_group": seg(seg_age),
            "interest": seg(seg_interest),
            "occupation": seg(seg_occ),
        },
        "pricing_analysis": {
            "product_price": product.get("price"),
            "currency": product.get("currency"),
            "mean_price_acceptance": metrics["price_acceptance"],
            "price_acceptance_by_price_sensitivity": {k: _avg(v) for k, v in price_sens.items()},
        },
        "sentiment_distribution": sentiment,
        "recommendations": recs,
        "limitations": LIMITATIONS
        + [f"{len(responses)} valid responses used; {failed} of {total} evaluations failed or were rejected."],
    }
