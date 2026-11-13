from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.session import get_session
from backend.app.models.orm import SimulationORM
from backend.app.schemas.simulation import Report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{simulation_id}", response_model=Report)
async def get_report(simulation_id: str, s: AsyncSession = Depends(get_session)):
    """The report id is the simulation id."""
    sim = await s.get(SimulationORM, simulation_id)
    if sim is None:
        raise HTTPException(404, "Simulation not found")
    if sim.status != "completed" or not sim.report:
        raise HTTPException(409, f"Report not ready (status: {sim.status})")
    return sim.report
