import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.database.session import get_session
from backend.app.models.orm import ProductORM, SimulationORM
from backend.app.schemas.simulation import (
    Progress, SimulationRequest, SimulationResults, SimulationStatus,
)
from backend.app.services.simulation_service import load_responses, run_simulation_job

router = APIRouter(prefix="/simulations", tags=["simulations"])


def _status(sim: SimulationORM) -> SimulationStatus:
    return SimulationStatus(
        simulation_id=sim.simulation_id,
        status=sim.status,
        progress=Progress(
            total_personas=sim.total_personas,
            completed_personas=sim.completed_personas,
            failed_personas=sim.failed_personas,
        ),
        error=sim.error,
        created_at=sim.created_at,
        updated_at=sim.updated_at,
    )


@router.post("", response_model=SimulationStatus, status_code=202)
async def start_simulation(
    body: SimulationRequest, bg: BackgroundTasks, s: AsyncSession = Depends(get_session)
):
    if body.persona_count > settings.MAX_PERSONA_COUNT:
        raise HTTPException(422, f"persona_count must be <= {settings.MAX_PERSONA_COUNT}")
    p = await s.get(ProductORM, body.product_id)
    if p is None:
        raise HTTPException(404, "Product not found")

    sim = SimulationORM(
        simulation_id=f"SIM{uuid.uuid4().hex[:8].upper()}",
        product_id=p.product_id,
        status="queued",
        config=body.model_dump(),
        total_personas=body.persona_count,
    )
    s.add(sim)
    await s.commit()

    product = {
        "product_id": p.product_id, "name": p.name, "description": p.description,
        "category": p.category, "price": p.price, "currency": p.currency,
        "features": p.features or [], "target_audience": p.target_audience,
    }
    bg.add_task(run_simulation_job, sim.simulation_id, product, body.audience_config, body.persona_count)
    return _status(sim)


@router.get("/{simulation_id}", response_model=SimulationStatus)
async def get_simulation(simulation_id: str, s: AsyncSession = Depends(get_session)):
    sim = await s.get(SimulationORM, simulation_id)
    if sim is None:
        raise HTTPException(404, "Simulation not found")
    return _status(sim)


@router.get("/{simulation_id}/results", response_model=SimulationResults)
async def get_results(simulation_id: str, s: AsyncSession = Depends(get_session)):
    sim = await s.get(SimulationORM, simulation_id)
    if sim is None:
        raise HTTPException(404, "Simulation not found")
    if sim.status not in ("completed", "failed"):
        raise HTTPException(409, f"Simulation is {sim.status}; results not ready")
    return SimulationResults(
        simulation_id=sim.simulation_id,
        status=sim.status,
        total=sim.total_personas,
        failed=sim.failed_personas,
        responses=await load_responses(s, simulation_id),
    )
