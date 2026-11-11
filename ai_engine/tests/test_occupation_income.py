from ai_engine.personas import generate_personas
from ai_engine.personas.persona_generator import OCCUPATIONS, OCCUPATION_INCOMES


def test_every_occupation_has_an_income_list():
    for jobs in OCCUPATIONS.values():
        for job in jobs:
            assert job in OCCUPATION_INCOMES, f"{job} missing from OCCUPATION_INCOMES"


def test_income_is_believable_for_the_job():
    for p in generate_personas({}, 400, seed=1):
        allowed = OCCUPATION_INCOMES[p["occupation"]]
        assert p["income_level"] in allowed, (
            f"{p['persona_id']}: {p['occupation']} with {p['income_level']} income"
        )


def test_premium_consumers_are_high_income():
    config = {"age_groups": ["35-44"], "archetypes": ["premium_consumer"]}
    for p in generate_personas(config, 60, seed=2):
        assert p["income_level"] == "High"
        assert "High" in OCCUPATION_INCOMES[p["occupation"]]
