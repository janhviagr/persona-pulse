"""Mirrors Person 3's persona fields. Required/optional split and 0-1 ranges match their models."""
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PersonaProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    # required
    persona_id: str
    age: int = Field(ge=0, le=120)
    occupation: str
    interests: list[str]
    personality_traits: Any  # shape owned by Person 3 (values 0-1)
    price_sensitivity: float = Field(ge=0, le=1)
    technical_literacy: float = Field(ge=0, le=1)
    # optional
    name: str | None = None
    income_level: str | None = None
    location_type: str | None = None
    brand_loyalty: float | None = Field(default=None, ge=0, le=1)
    innovation_preference: float | None = Field(default=None, ge=0, le=1)
    purchase_impulsiveness: float | None = Field(default=None, ge=0, le=1)
    primary_motivation: str | None = None
    purchase_constraints: Any | None = None


class PersonaGenerateRequest(BaseModel):
    audience_config: dict[str, Any] = Field(default_factory=dict)
    count: int = Field(default=20, ge=1)
