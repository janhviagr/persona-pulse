from fastapi.testclient import TestClient

from backend.app.main import app

PRODUCT = {
    "name": "Fitness Smartwatch", "description": "Tracks workouts", "category": "wearables",
    "price": 4999, "currency": "INR", "features": ["heart rate", "GPS"],
}


async def fake_eval(product, audience_config, count, on_progress=None):
    personas = [
        {"persona_id": f"P{i:03d}", "age": 20 + i * 5, "occupation": "student", "interests": ["fitness"],
         "personality_traits": {"openness": 0.5}, "price_sensitivity": 0.6, "technical_literacy": 0.7}
        for i in range(count)
    ]
    responses = [
        {"persona_id": p["persona_id"], "interest_score": 80, "purchase_intent": 60, "price_acceptance": 50,
         "perceived_usefulness": 70, "design_appeal": 75, "reasoning": "ok", "would_recommend": True,
         "positive_factors": ["GPS"], "negative_factors": ["price"]}
        for p in personas
    ]
    responses.append({**responses[0], "interest_score": 150})  # invalid: out of range
    if on_progress:
        for i in range(1, count + 1):
            on_progress(i, 0, count)
    return {"personas": personas, "responses": responses, "total": len(responses), "failed": 0}


def test_full_flow(monkeypatch):
    monkeypatch.setattr("backend.app.services.simulation_service.evaluate_with_personas", fake_eval)
    with TestClient(app) as c:
        pid = c.post("/api/v1/products", json=PRODUCT).json()["product_id"]
        assert c.get(f"/api/v1/products/{pid}").status_code == 200

        r = c.post("/api/v1/simulations", json={"product_id": pid, "persona_count": 3})
        assert r.status_code == 202
        sid = r.json()["simulation_id"]

        st = c.get(f"/api/v1/simulations/{sid}").json()
        assert st["status"] == "completed"
        assert st["progress"]["failed_personas"] == 1  # the invalid response

        res = c.get(f"/api/v1/simulations/{sid}/results").json()
        assert len(res["responses"]) == 3

        rep = c.get(f"/api/v1/reports/{sid}").json()
        assert "overall_score" in rep, rep
        assert rep["overall_score"] > 0
        assert "age_group" in rep["segment_analysis"]

        assert c.get(f"/api/v1/personas/P000?simulation_id={sid}").status_code == 200


def test_unknown_product():
    with TestClient(app) as c:
        assert c.post("/api/v1/simulations", json={"product_id": "NOPE"}).status_code == 404
