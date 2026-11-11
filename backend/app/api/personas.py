import asyncio
import inspect
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.database.session import get_session
from backend.app.models.orm import PersonaORM
from backend.app.schemas.persona import PersonaGenerateRequest, PersonaProfile

try:
    from ai_engine.personas import PersonaGenerator
except ImportError:
    PersonaGenerator = None

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post("/generate", response_model=list[PersonaProfile])
async def generate_personas(body: PersonaGenerateRequest):
    if PersonaGenerator is None:
        raise HTTPException(501, "ai_engine.personas.PersonaGenerator not available (merge feature/persona-engine)")
    if body.count > settings.MAX_PERSONA_COUNT:
        raise HTTPException(422, f"count must be <= {settings.MAX_PERSONA_COUNT}")
    gen = PersonaGenerator()
    result = gen.generate_personas(body.audience_config, body.count)
    if inspect.isawaitable(result):
        result = await result
    out: list[dict[str, Any]] = []
    for p in result:
        d = p.model_dump(mode="json") if hasattr(p, "model_dump") else dict(p)
        try:
            out.append(PersonaProfile.model_validate(d))
        except ValidationError:
            continue  # reject invalid profiles
    return out


@router.get("/{persona_id}", response_model=PersonaProfile)
async def get_persona(persona_id: str, simulation_id: str | None = None, s: AsyncSession = Depends(get_session)):
    """persona_ids (e.g. P001) repeat across simulations; pass ?simulation_id= to disambiguate."""
    q = select(PersonaORM).where(PersonaORM.persona_id == persona_id)
    if simulation_id:
        q = q.where(PersonaORM.simulation_id == simulation_id)
    row = (await s.execute(q.order_by(PersonaORM.id.desc()))).scalars().first()
    if row is None:
        raise HTTPException(404, "Persona not found")
    return PersonaProfile.model_validate(row.data)
