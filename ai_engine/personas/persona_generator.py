import random

from .persona_model import Persona

ALL_AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]

OCCUPATIONS = {
    "18-24": ["Student", "Student", "Student", "Intern", "Freelancer", "Junior Executive"],
    "25-34": ["Software Engineer", "Teacher", "Marketing Executive", "Nurse", "Shopkeeper", "Designer"],
    "35-44": ["Manager", "Doctor", "Accountant", "Business Owner", "Engineer", "Homemaker"],
    "45-54": ["Senior Manager", "Business Owner", "Teacher", "Government Employee", "Doctor"],
    "55+": ["Retired", "Retired", "Business Owner", "Government Employee", "Consultant"],
}

# (low, high) range of technical literacy by age group
TECH_LITERACY = {
    "18-24": (0.6, 1.0),
    "25-34": (0.5, 0.95),
    "35-44": (0.4, 0.85),
    "45-54": (0.25, 0.7),
    "55+": (0.1, 0.55),
}

# (low, high) range of price sensitivity by income level
PRICE_SENSITIVITY = {
    "Low": (0.6, 0.95),
    "Medium": (0.35, 0.75),
    "High": (0.1, 0.5),
}

INTEREST_POOL = [
    "technology", "fitness", "gaming", "travel", "fashion", "music",
    "cooking", "photography", "reading", "sports", "finance", "movies",
]
TRAIT_POOL = [
    "curious", "skeptical", "price_conscious", "impulsive", "careful",
    "trend_aware", "practical", "brand_loyal", "adventurous", "cautious",
]
NAMES = [
    "Arjun", "Priya", "Rohan", "Ananya", "Vikram", "Meera", "Karan", "Sneha",
    "Aditya", "Divya", "Rahul", "Neha", "Siddharth", "Pooja", "Amit", "Kavya",
    "Nikhil", "Ishita", "Varun", "Riya", "Manish", "Tanvi", "Deepak", "Shreya",
]


def parse_age_group(group: str) -> tuple[int, int]:
    """'18-24' -> (18, 24).  '55+' -> (55, 75)."""
    if group.endswith("+"):
        return int(group[:-1]), 75
    low, high = group.split("-")
    return int(low), int(high)


def _pick_income(occupation: str, rng: random.Random) -> str:
    if occupation in ("Student", "Intern"):
        return "Low"
    if occupation == "Retired":
        return rng.choices(["Low", "Medium"], weights=[0.5, 0.5])[0]
    return rng.choices(["Low", "Medium", "High"], weights=[0.25, 0.5, 0.25])[0]


def _pick_interests(wanted: list[str], rng: random.Random) -> list[str]:
    """Always include 1 audience interest if given, then fill up to 3."""
    chosen = []
    if wanted:
        chosen.append(rng.choice(wanted))
    others = [i for i in INTEREST_POOL if i not in chosen]
    chosen += rng.sample(others, 3 - len(chosen))
    return chosen


def generate_personas(
    audience_config: dict, count: int, seed: int | None = None
) -> list[dict]:
    """Make `count` personas that fit the audience. Same seed = same result."""
    rng = random.Random(seed)
    age_groups = audience_config.get("age_groups") or ALL_AGE_GROUPS
    wanted_interests = audience_config.get("interests") or []

    personas = []
    for i in range(1, count + 1):
        group = rng.choice(age_groups)
        low, high = parse_age_group(group)
        age = rng.randint(low, high)

        occupation = rng.choice(OCCUPATIONS.get(group, OCCUPATIONS["25-34"]))
        income = _pick_income(occupation, rng)

        ps_low, ps_high = PRICE_SENSITIVITY[income]
        tl_low, tl_high = TECH_LITERACY.get(group, (0.3, 0.8))

        persona = Persona(
            persona_id=f"P{i:03d}",
            name=rng.choice(NAMES),
            age=age,
            occupation=occupation,
            income_level=income,
            location_type=rng.choice(["Urban", "Urban", "Semi-urban", "Rural"]),
            interests=_pick_interests(wanted_interests, rng),
            personality_traits=rng.sample(TRAIT_POOL, 3),
            price_sensitivity=round(rng.uniform(ps_low, ps_high), 2),
            technical_literacy=round(rng.uniform(tl_low, tl_high), 2),
            brand_loyalty=round(rng.random(), 2),
            innovation_preference=round(rng.random(), 2),
            purchase_impulsiveness=round(rng.random(), 2),
        )
        personas.append(persona.model_dump())
    return personas
