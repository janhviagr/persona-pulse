from pydantic import BaseModel, Field


class Persona(BaseModel):
    """One synthetic customer. Matches contracts/persona.schema.json."""

    # Required fields
    persona_id: str
    age: int = Field(ge=18, le=100)
    occupation: str
    interests: list[str]
    personality_traits: list[str]
    price_sensitivity: float = Field(ge=0, le=1)
    technical_literacy: float = Field(ge=0, le=1)

    # Optional fields (have defaults)
    name: str = ""
    income_level: str = ""
    location_type: str = ""
    brand_loyalty: float = Field(default=0.5, ge=0, le=1)
    innovation_preference: float = Field(default=0.5, ge=0, le=1)
    purchase_impulsiveness: float = Field(default=0.5, ge=0, le=1)
    primary_motivation: str = ""
    purchase_constraints: list[str] = []
