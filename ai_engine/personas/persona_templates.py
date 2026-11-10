"""Customer archetypes. Each trait is a (low, high) range between 0 and 1."""

RANGE_KEYS = [
    "price_sensitivity",
    "technical_literacy",
    "brand_loyalty",
    "innovation_preference",
    "purchase_impulsiveness",
]

# age_groups = None means "fits any age group"
ARCHETYPES = {
    "budget_student": {
        "age_groups": ["18-24"],
        "occupation": "Student",
        "income": "Low",
        "price_sensitivity": (0.7, 0.95),
        "technical_literacy": (0.6, 0.95),
        "brand_loyalty": (0.1, 0.4),
        "innovation_preference": (0.5, 0.85),
        "purchase_impulsiveness": (0.3, 0.6),
        "traits": ["price_conscious", "curious"],
        "motivation": "Value for money",
        "constraints": ["Limited budget"],
        "interests": ["technology", "gaming"],
    },
    "tech_enthusiast": {
        "age_groups": None,
        "occupation": None,
        "income": None,
        "price_sensitivity": (0.2, 0.6),
        "technical_literacy": (0.8, 1.0),
        "brand_loyalty": (0.2, 0.6),
        "innovation_preference": (0.75, 1.0),
        "purchase_impulsiveness": (0.4, 0.8),
        "traits": ["curious", "adventurous"],
        "motivation": "Latest features and performance",
        "constraints": [],
        "interests": ["technology", "gaming"],
    },
    "working_professional": {
        "age_groups": ["25-34", "35-44", "45-54"],
        "occupation": None,
        "income": None,
        "price_sensitivity": (0.3, 0.65),
        "technical_literacy": (0.5, 0.85),
        "brand_loyalty": (0.3, 0.7),
        "innovation_preference": (0.3, 0.65),
        "purchase_impulsiveness": (0.2, 0.5),
        "traits": ["practical", "careful"],
        "motivation": "Convenience and saving time",
        "constraints": ["Limited free time"],
        "interests": ["finance", "travel"],
    },
    "family_consumer": {
        "age_groups": ["25-34", "35-44", "45-54"],
        "occupation": None,
        "income": None,
        "price_sensitivity": (0.5, 0.85),
        "technical_literacy": (0.3, 0.7),
        "brand_loyalty": (0.5, 0.85),
        "innovation_preference": (0.15, 0.5),
        "purchase_impulsiveness": (0.1, 0.4),
        "traits": ["cautious", "practical"],
        "motivation": "Safety and reliability for the family",
        "constraints": ["Household budget"],
        "interests": ["cooking", "travel"],
    },
    "traditional_consumer": {
        "age_groups": ["45-54", "55+"],
        "occupation": None,
        "income": None,
        "price_sensitivity": (0.5, 0.85),
        "technical_literacy": (0.1, 0.5),
        "brand_loyalty": (0.6, 0.95),
        "innovation_preference": (0.05, 0.35),
        "purchase_impulsiveness": (0.05, 0.3),
        "traits": ["cautious", "brand_loyal"],
        "motivation": "Familiarity and trust",
        "constraints": ["Distrusts unfamiliar technology"],
        "interests": ["reading", "cooking"],
    },
    "trend_follower": {
        "age_groups": ["18-24", "25-34"],
        "occupation": None,
        "income": None,
        "price_sensitivity": (0.3, 0.7),
        "technical_literacy": (0.5, 0.9),
        "brand_loyalty": (0.3, 0.7),
        "innovation_preference": (0.6, 0.95),
        "purchase_impulsiveness": (0.6, 0.95),
        "traits": ["trend_aware", "impulsive"],
        "motivation": "Style and social image",
        "constraints": ["Wants peer approval"],
        "interests": ["fashion", "music"],
    },
    "health_conscious": {
        "age_groups": None,
        "occupation": None,
        "income": None,
        "price_sensitivity": (0.35, 0.7),
        "technical_literacy": (0.3, 0.8),
        "brand_loyalty": (0.3, 0.7),
        "innovation_preference": (0.4, 0.75),
        "purchase_impulsiveness": (0.2, 0.5),
        "traits": ["practical", "careful"],
        "motivation": "Better health and wellbeing",
        "constraints": ["Wants proven accuracy"],
        "interests": ["fitness", "cooking"],
    },
    "premium_consumer": {
        "age_groups": ["25-34", "35-44", "45-54", "55+"],
        "occupation": None,
        "income": "High",
        "price_sensitivity": (0.0, 0.3),
        "technical_literacy": (0.4, 0.9),
        "brand_loyalty": (0.6, 1.0),
        "innovation_preference": (0.4, 0.8),
        "purchase_impulsiveness": (0.3, 0.7),
        "traits": ["brand_loyal", "trend_aware"],
        "motivation": "Quality and brand prestige",
        "constraints": ["Dislikes cheap-looking products"],
        "interests": ["travel", "fashion"],
    },
}


def _merge(lists):
    """Join lists, dropping repeats but keeping order."""
    out = []
    for items in lists:
        for item in items:
            if item not in out:
                out.append(item)
    return out


def combine_archetypes(names: list[str]) -> dict:
    """Blend one or more archetypes into a single profile (ranges are averaged)."""
    parts = [ARCHETYPES[n] for n in names]
    combined = {"names": list(names)}

    for key in RANGE_KEYS:
        lows = [p[key][0] for p in parts]
        highs = [p[key][1] for p in parts]
        combined[key] = (sum(lows) / len(parts), sum(highs) / len(parts))

    combined["traits"] = _merge(p["traits"] for p in parts)
    combined["constraints"] = _merge(p["constraints"] for p in parts)
    combined["interests"] = _merge(p["interests"] for p in parts)
    combined["motivation"] = " and ".join(p["motivation"] for p in parts)
    combined["occupation"] = next((p["occupation"] for p in parts if p["occupation"]), None)
    combined["income"] = next((p["income"] for p in parts if p["income"]), None)
    return combined
