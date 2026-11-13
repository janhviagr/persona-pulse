
import random


# --------------------------------------------------
# PRODUCT CONTEXT
# --------------------------------------------------

def get_product_context(product):
    """
    Builds product-specific benefits and buying concerns
    using the information submitted by the user.
    """

    name = product.get("name", "this product")
    description = product.get("description", "")
    category = product.get("category", "")

    raw_features = product.get("features", [])

    if isinstance(raw_features, str):
        features = [
            item.strip()
            for item in raw_features.replace("\n", ",").split(",")
            if item.strip()
        ]
    elif isinstance(raw_features, list):
        features = [str(item).strip() for item in raw_features if str(item).strip()]
    else:
        features = []

    product_text = (
        name + " " + description + " " + category + " " +
        " ".join(features)
    ).lower()

    # Category-specific considerations.
    # These are fallback assumptions, not claims about actual features.

    if any(word in product_text for word in [
        "sweater", "clothing", "apparel", "fashion",
        "garment", "jacket", "shirt", "dress"
    ]):
        benefits = [
            "comfort and fit",
            "fabric quality",
            "style and appearance",
            "warmth and everyday usability",
            "durability after repeated use",
            "ease of washing and maintenance"
        ]

        concerns = [
            "whether the fit and sizing will be right",
            "whether the fabric feels comfortable",
            "whether the product is easy to maintain",
            "whether the price matches the quality",
            "whether the design suits my personal style",
            "whether it will remain durable after repeated use"
        ]

    elif any(word in product_text for word in [
        "watch", "fitness", "tracker", "wearable"
    ]):
        benefits = [
            "ease of use",
            "useful product features",
            "reliable performance",
            "convenience in everyday life",
            "long-term durability",
            "value for money"
        ]

        concerns = [
            "battery life",
            "whether the features are genuinely useful",
            "ease of use",
            "long-term reliability",
            "compatibility with my devices",
            "whether the price is justified"
        ]

    elif any(word in product_text for word in [
        "phone", "laptop", "electronic", "gadget",
        "speaker", "headphone", "device"
    ]):
        benefits = [
            "performance and reliability",
            "ease of use",
            "useful features",
            "battery life and efficiency",
            "compatibility",
            "value for money"
        ]

        concerns = [
            "performance over time",
            "battery life",
            "compatibility with other devices",
            "product reliability",
            "ease of use",
            "whether the price is justified"
        ]

    elif any(word in product_text for word in [
        "food", "snack", "beverage", "drink", "coffee"
    ]):
        benefits = [
            "taste and overall experience",
            "ingredient quality",
            "convenience",
            "packaging and freshness",
            "value for money",
            "availability"
        ]

        concerns = [
            "taste and quality",
            "ingredient transparency",
            "freshness",
            "packaging",
            "price compared with alternatives",
            "whether I would buy it again"
        ]

    elif any(word in product_text for word in [
        "beauty", "skincare", "cosmetic", "makeup"
    ]):
        benefits = [
            "ease of application",
            "product quality",
            "texture and experience",
            "packaging and convenience",
            "value for money",
            "suitability for my preferences"
        ]

        concerns = [
            "whether the product suits my preferences",
            "product quality",
            "ease of application",
            "packaging",
            "price compared with alternatives",
            "whether the product delivers its stated benefits"
        ]

    else:
        benefits = [
            "quality and reliability",
            "convenience",
            "ease of use",
            "practical usefulness",
            "durability",
            "value for money"
        ]

        concerns = [
            "whether the product meets my expectations",
            "product quality",
            "ease of use",
            "long-term reliability",
            "availability of alternatives",
            "whether the price is justified"
        ]

    # Submitted product features take priority.
    # We only use features that the user actually supplied.

    if features:
        benefits = features + benefits

    return {
        "name": name,
        "description": description,
        "category": category,
        "features": features,
        "benefits": benefits,
        "concerns": concerns
    }


# --------------------------------------------------
# PERSONA-SPECIFIC FEEDBACK
# --------------------------------------------------

def generate_feedback(
    rng,
    persona,
    product_context
):

    product_name = product_context["name"]

    benefit = persona["purchase_motivation"]
    concern = persona["purchase_barrier"]

    likelihood = persona["purchase_likelihood"]
    price_sensitivity = persona["price_sensitivity"]

    if likelihood >= 75:

        opinion = rng.choice([
            f"I would seriously consider buying {product_name}.",
            f"{product_name} looks like something I could see myself purchasing.",
            f"I am quite interested in {product_name}.",
            f"I think {product_name} could be a good fit for my needs."
        ])

    elif likelihood >= 50:

        opinion = rng.choice([
            f"I might consider buying {product_name} after comparing alternatives.",
            f"{product_name} seems promising, but I need more information.",
            f"I am somewhat interested in {product_name}, but not fully convinced.",
            f"I would like to understand the product better before purchasing."
        ])

    else:

        opinion = rng.choice([
            f"I am not currently convinced that I need {product_name}.",
            f"I would probably explore alternatives before buying {product_name}.",
            f"{product_name} would need to offer more value to interest me.",
            f"I am unlikely to purchase {product_name} without stronger reasons."
        ])

    templates = [
        (
            f"As a {persona['occupation'].lower()}, I value {benefit}. "
            f"{opinion} My main concern is {concern}."
        ),

        (
            f"Looking at {product_name}, {opinion} "
            f"I would particularly care about {benefit}. "
            f"However, {concern} could affect my decision."
        ),

        (
            f"My shopping decisions are influenced by {benefit}. "
            f"{opinion} I would want reassurance about {concern}."
        ),

        (
            f"I usually discover products through "
            f"{persona['preferred_channel'].lower()}. "
            f"{opinion} Before buying, I would consider {concern}."
        ),

        (
            f"At my age of {persona['age']}, I would look for "
            f"{benefit}. {opinion} "
            f"I would also compare its price with alternatives."
        ),

        (
            f"Since I am {price_sensitivity.lower()} price-sensitive, "
            f"I would evaluate whether {product_name} offers good value. "
            f"{opinion} My main consideration would be {benefit}."
        )
    ]

    return rng.choice(templates)


# --------------------------------------------------
# GENERATE SAMPLE PERSONAS
# --------------------------------------------------

def get_sample_personas(count=50, product=None):

    rng = random.Random(42)

    if product is None:
        product = {}

    product_context = get_product_context(product)

    names = [
        "Aarav", "Priya", "Rahul", "Sneha", "Karan",
        "Meera", "Arjun", "Ananya", "Rohan", "Ishita",
        "Dev", "Aditi", "Kabir", "Neha", "Varun",
        "Diya", "Aditya", "Kavya", "Ishan", "Nisha",
        "Vihaan", "Riya", "Reyansh", "Tara", "Sahil"
    ]

    occupations = [
        "Student",
        "Software Engineer",
        "Marketing Executive",
        "Business Owner",
        "Designer",
        "Teacher",
        "Fitness Trainer",
        "Consultant",
        "Data Analyst",
        "Researcher",
        "Content Creator"
    ]

    locations = [
        "Bengaluru",
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Kochi",
        "Jaipur"
    ]

    # Use the target interests selected in the product form
    # when available.

    target_interests = product.get("interests", [])

    if isinstance(target_interests, str):
        target_interests = [
            x.strip()
            for x in target_interests.split(",")
            if x.strip()
        ]

    if not isinstance(target_interests, list):
        target_interests = []

    if not target_interests:
        target_interests = [
            "Technology",
            "Lifestyle",
            "Shopping",
            "Product Quality",
            "Convenience",
            "Value for Money"
        ]

    # Use product-specific benefits and concerns.

    benefits = product_context["benefits"]
    concerns = product_context["concerns"]

    frequencies = [
        "Weekly",
        "Monthly",
        "Occasionally",
        "Rarely"
    ]

    personas = []

    for i in range(count):

        age = rng.randint(18, 55)
        likelihood = rng.randint(25, 98)

        if likelihood >= 75:
            sentiment = "Positive"
        elif likelihood >= 50:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"

        occupation = rng.choice(occupations)
        location = rng.choice(locations)

        persona_interests = rng.sample(
            target_interests,
            k=min(2, len(target_interests))
        )

        motivation = rng.choice(benefits)
        barrier = rng.choice(concerns)

        sensitivity = rng.choice([
            "High",
            "Medium",
            "Low"
        ])

        channel = rng.choice([
            "Online Stores",
            "Social Media",
            "Brand Website",
            "Retail Stores",
            "Recommendations",
            "E-commerce Apps"
        ])

        frequency = rng.choice(frequencies)

        name = rng.choice(names) + f" {i + 1}"

        persona = {
            "id": i + 1,
            "name": name,
            "age": age,
            "occupation": occupation,
            "location": location,
            "income": rng.randint(15000, 120000),
            "interests": persona_interests,
            "budget": rng.randint(2000, 10000),
            "sentiment": sentiment,
            "purchase_likelihood": likelihood,
            "purchase_frequency": frequency,
            "preferred_channel": channel,
            "price_sensitivity": sensitivity,
            "purchase_motivation": motivation,
            "purchase_barrier": barrier
        }

        persona["feedback"] = generate_feedback(
            rng,
            persona,
            product_context
        )

        personas.append(persona)

    return personas
