from ai_engine.personas import generate_personas
from ai_engine.personas.persona_templates import ARCHETYPES, RANGE_KEYS, combine_archetypes


def test_all_archetype_ranges_are_valid():
    for name, archetype in ARCHETYPES.items():
        for key in RANGE_KEYS:
            low, high = archetype[key]
            assert 0 <= low <= high <= 1, f"{name}.{key} is invalid"


def test_blend_keeps_traits_from_both():
    mixed = combine_archetypes(["budget_student", "tech_enthusiast"])
    assert "price_conscious" in mixed["traits"]
    assert "adventurous" in mixed["traits"]
    assert mixed["occupation"] == "Student"


def test_budget_students_are_price_sensitive():
    config = {"age_groups": ["18-24"], "archetypes": ["budget_student"]}
    for p in generate_personas(config, 50, seed=1):
        assert p["occupation"] == "Student"
        assert p["income_level"] == "Low"
        assert p["price_sensitivity"] >= 0.6


def test_traditional_consumers_have_low_tech_literacy():
    config = {"age_groups": ["55+"], "archetypes": ["traditional_consumer"]}
    for p in generate_personas(config, 50, seed=1):
        assert p["technical_literacy"] <= 0.6


def test_tech_enthusiasts_have_high_tech_literacy():
    config = {"age_groups": ["25-34"], "archetypes": ["tech_enthusiast"]}
    for p in generate_personas(config, 50, seed=1):
        assert p["technical_literacy"] >= 0.6


def test_every_persona_gets_a_motivation():
    for p in generate_personas({}, 100, seed=1):
        assert p["primary_motivation"] != ""
