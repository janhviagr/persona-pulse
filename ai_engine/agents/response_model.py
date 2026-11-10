from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """One persona's evaluation of a product. Matches contracts/simulation_result.schema.json."""

    # Required fields
    persona_id: str
    interest_score: float = Field(ge=0, le=100)
    purchase_intent: float = Field(ge=0, le=100)
    price_acceptance: float = Field(ge=0, le=100)
    perceived_usefulness: float = Field(ge=0, le=100)
    design_appeal: float = Field(ge=0, le=100)
    reasoning: str

    # Optional fields
    product_id: str = ""
    would_recommend: bool = False
    positive_factors: list[str] = []
    negative_factors: list[str] = []
