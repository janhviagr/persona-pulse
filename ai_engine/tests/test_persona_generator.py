from ai_engine.personas import generate_personas

CONFIG = {"age_groups": ["18-24", "25-34"], "interests": ["fitness"]}


def test_generates_requested_count():
    assert len(generate_personas(CONFIG, 50, seed=1)) == 50


def test_ids_are_unique():
    ids = [p["persona_id"] for p in generate_personas(CONFIG, 100, seed=1)]
    assert len(set(ids)) == 100


def test_respects_age_groups():
    for p in generate_personas(CONFIG, 100, seed=1):
        assert 18 <= p["age"] <= 34


def test_traits_within_range():
    for p in generate_personas(CONFIG, 100, seed=1):
        assert 0 <= p["price_sensitivity"] <= 1
        assert 0 <= p["technical_literacy"] <= 1


def test_every_persona_has_audience_interest_or_pool_interest():
    for p in generate_personas(CONFIG, 50, seed=1):
        assert "fitness" in p["interests"]


def test_same_seed_same_result():
    assert generate_personas(CONFIG, 10, seed=7) == generate_personas(CONFIG, 10, seed=7)


def test_students_are_low_income():
    for p in generate_personas(CONFIG, 100, seed=1):
        if p["occupation"] == "Student":
            assert p["income_level"] == "Low"
