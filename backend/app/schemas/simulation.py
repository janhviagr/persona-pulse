from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SimStatus = Literal["queued", "generating_personas", "running", "aggregating", "completed", "failed"]


class SimulationRequest(BaseModel):
    product_id: str
    persona_count: int = Field(default=20, ge=1)
    audience_config: dict[str, Any] = Field(default_factory=dict)
    evaluation_categories: list[str] = Field(
        default_factory=lambda: ["appeal", "purchase_intent", "price_acceptance"]
    )
    pricing_scenarios: list[float] = Field(default_factory=list)


class Progress(BaseModel):
    total_personas: int
    completed_personas: int
    failed_personas: int


class SimulationStatus(BaseModel):
    simulation_id: str
    status: SimStatus
    progress: Progress
    error: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AgentResponse(BaseModel):
    """Mirrors Person 3's agent response fields. Scores are 0-100."""
    model_config = ConfigDict(extra="allow")

    # required
    persona_id: str
    interest_score: float = Field(ge=0, le=100)
    purchase_intent: float = Field(ge=0, le=100)
    price_acceptance: float = Field(ge=0, le=100)
    perceived_usefulness: float = Field(ge=0, le=100)
    design_appeal: float = Field(ge=0, le=100)
    reasoning: str
    # optional
    product_id: str | None = None
    would_recommend: bool | None = None
    positive_factors: list[str] = Field(default_factory=list)
    negative_factors: list[str] = Field(default_factory=list)


class SimulationResults(BaseModel):
    simulation_id: str
    status: SimStatus
    total: int
    failed: int
    responses: list[AgentResponse]


class Report(BaseModel):
    model_config = ConfigDict(extra="allow")

    simulation_id: str
    overall_score: float
    segment_analysis: dict[str, Any]
    pricing_analysis: dict[str, Any]
    sentiment_distribution: dict[str, Any]
    metrics: dict[str, Any]
    recommendations: list[Any]
    limitations: list[Any]