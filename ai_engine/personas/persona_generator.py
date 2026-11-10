import random

from .persona_model import Persona
from .persona_templates import ARCHETYPES, combine_archetypes

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

BLEND_CHANCE = 0.3  # chance that a persona mixes two archetypes


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


def _pick_archetypes(group: str, allowed: list[str] | None, rng: random.Random) -> list[str]:
    """Choose 1 archetype (sometimes 2) that fit this age group."""
    candidates = [
        name for name, a in ARCHETYPES.items()
        if (a["age_groups"] is None or group in a["age_groups"])
        and (allowed is None or name in allowed)
    ]
    if not candidates:
        return []
    chosen = [rng.choice(candidates)]
    others = [c for c in candidates if c != chosen[0]]
    if others and rng.random() < BLEND_CHANCE:
        chosen.append(rng.choice(others))
    return chosen


def _mix(base: tuple[float, float], extra: tuple[float, float]) -> tuple[float, float]:
    """Average two (low, high) ranges."""
    return (base[0] + extra[0]) / 2, (base[1] + extra[1]) / 2


def _draw(rng: random.Random, value_range: tuple[float, float]) -> float:
    low, high = value_range
    return round(rng.uniform(low, high), 2)


def _pick_interests(wanted: list[str], archetype_interests: list[str], rng: random.Random) -> list[str]:
    """One audience interest, one archetype interest, then fill up to 3."""
    chosen = []
    if wanted:
        chosen.append(rng.choice(wanted))
    options = [i for i in archetype_interests if i not in chosen]
    if options:
        chosen.append(rng.choice(options))
    others = [i for i in INTEREST_POOL if i not in chosen]
    chosen += rng.sample(others, max(0, 3 - len(chosen)))
    return chosen


def _pick_traits(archetype_traits: list[str], rng: random.Random) -> list[str]:
    traits = list(archetype_traits)
    others = [t for t in TRAIT_POOL if t not in traits]
    traits += rng.sample(others, max(0, 3 - len(traits)))
    return traits


def generate_personas(
    audience_config: dict, count: int, seed: int | None = None
) -> list[dict]:
    """Make `count` personas that fit the audience. Same seed = same result."""
    rng = random.Random(seed)
    age_groups = audience_config.get("age_groups") or ALL_AGE_GROUPS
    wanted_interests = audience_config.get("interests") or []
    allowed_archetypes = audience_config.get("archetypes")  # optional list of names

    personas = []
    for i in range(1, count + 1):
        group = rng.choice(age_groups)
        low, high = parse_age_group(group)
        age = rng.randint(low, high)

        names = _pick_archetypes(group, allowed_archetypes, rng)
        arch = combine_archetypes(names) if names else None

        occupation = (arch and arch["occupation"]) or rng.choice(
            OCCUPATIONS.get(group, OCCUPATIONS["25-34"])
        )
        income = (arch and arch["income"]) or _pick_income(occupation, rng)

        price_range = PRICE_SENSITIVITY[income]
        tech_range = TECH_LITERACY.get(group, (0.3, 0.8))
        if arch:
            price_range = _mix(price_range, arch["price_sensitivity"])
            tech_range = _mix(tech_range, arch["technical_literacy"])

        full_range = (0.0, 1.0)
        persona = Persona(
            persona_id=f"P{i:03d}",
            name=rng.choice(NAMES),
            age=age,
            occupation=occupation,
            income_level=income,
            location_type=rng.choice(["Urban", "Urban", "Semi-urban", "Rural"]),
            interests=_pick_interests(wanted_interests, arch["interests"] if arch else [], rng),
            personality_traits=_pick_traits(arch["traits"] if arch else [], rng),
            price_sensitivity=_draw(rng, price_range),
            technical_literacy=_draw(rng, tech_range),
            brand_loyalty=_draw(rng, arch["brand_loyalty"] if arch else full_range),
            innovation_preference=_draw(rng, arch["innovation_preference"] if arch else full_range),
            purchase_impulsiveness=_draw(rng, arch["purchase_impulsiveness"] if arch else full_range),
            primary_motivation=arch["motivation"] if arch else "",
            purchase_constraints=arch["constraints"] if arch else [],
        )
        personas.append(persona.model_dump())
    return personas
