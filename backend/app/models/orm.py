from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.session import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ProductORM(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]
    currency: Mapped[str] = mapped_column(String(8), default="INR")
    features: Mapped[list[Any]] = mapped_column(JSON, default=list)
    target_audience: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class SimulationORM(Base):
    __tablename__ = "simulations"

    simulation_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.product_id"))
    status: Mapped[str] = mapped_column(String(30), default="queued")
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)  # full request, for reproducibility
    total_personas: Mapped[int] = mapped_column(Integer, default=0)
    completed_personas: Mapped[int] = mapped_column(Integer, default=0)
    failed_personas: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    report: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)


class PersonaORM(Base):
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    simulation_id: Mapped[str] = mapped_column(ForeignKey("simulations.simulation_id"), index=True)
    persona_id: Mapped[str] = mapped_column(String(60), index=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSON)


class ResponseORM(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    simulation_id: Mapped[str] = mapped_column(ForeignKey("simulations.simulation_id"), index=True)
    persona_id: Mapped[str] = mapped_column(String(60), index=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
