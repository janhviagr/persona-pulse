"""Runs a simulation in the background and keeps the DB in sync.

Person 3's evaluate_with_personas generates personas AND evaluates them in one call,
so status goes generating_personas -> (first progress callback) running -> aggregating -> completed.
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from pydantic import ValidationError
from sqlalchemy import case, select, update

from backend.app.database.session import SessionLocal
from backend.app.models.orm import PersonaORM, ResponseORM, SimulationORM
from backend.app.schemas.persona import PersonaProfile
from backend.app.schemas.simulation import AgentResponse
from backend.app.services import report_service

try:
    from ai_engine.agents import evaluate_with_personas
except ImportError:  # branch not merged yet
    evaluate_with_personas = None

log = logging.getLogger(__name__)


def _to_dict(x: Any) -> dict[str, Any]:
    if hasattr(x, "model_dump"):
        return x.model_dump(mode="json")
    return dict(x)


def _get(obj: Any, key: str) -> Any:
    return obj[key] if isinstance(obj, dict) else getattr(obj, key)


async def _update(sim_id: str, **fields: Any) -> None:
    async with SessionLocal() as s:
        sim = await s.get(SimulationORM, sim_id)
        if sim is None:
            return
        for k, v in fields.items():
            setattr(sim, k, v)
        sim.updated_at = datetime.now(timezone.utc)
        await s.commit()


async def _update_progress(sim_id: str, completed: int, failed: int, total: int) -> None:
    # One atomic UPDATE guarded by status, so a late tick can never overwrite
    # aggregating/completed/failed. GREATEST-style monotonic counters via CASE.
    async with SessionLocal() as s:
        await s.execute(
            update(SimulationORM)
            .where(
                SimulationORM.simulation_id == sim_id,
                SimulationORM.status.in_(("generating_personas", "running")),
            )
            .values(
                status="running",
                total_personas=case((SimulationORM.total_personas < total, total), else_=SimulationORM.total_personas),
                completed_personas=case(
                    (SimulationORM.completed_personas < completed, completed), else_=SimulationORM.completed_personas
                ),
                failed_personas=case(
                    (SimulationORM.failed_personas < failed, failed), else_=SimulationORM.failed_personas
                ),
                updated_at=datetime.now(timezone.utc),
            )
        )
        await s.commit()


async def run_simulation_job(
    sim_id: str,
    product: dict[str, Any],
    audience_config: dict[str, Any],
    count: int,
) -> None:
    loop = asyncio.get_running_loop()
    await _update(sim_id, status="generating_personas", total_personas=count)

    pending: set[asyncio.Task] = set()

    def _spawn(c: int, f: int, t: int) -> None:
        task = loop.create_task(_update_progress(sim_id, c, f, t))
        pending.add(task)
        task.add_done_callback(pending.discard)

    def on_progress(completed: int, failed: int, total: int) -> None:
        # Works whether Person 3 calls this from the loop or a worker thread.
        loop.call_soon_threadsafe(_spawn, completed, failed, total)

    try:
        if evaluate_with_personas is None:
            raise RuntimeError("ai_engine.agents.evaluate_with_personas not found (merge feature/persona-engine)")

        out = await evaluate_with_personas(product, audience_config, count, on_progress=on_progress)
        await asyncio.sleep(0)  # let queued progress callbacks start
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        await _update(sim_id, status="aggregating")

        personas = [_to_dict(p) for p in _get(out, "personas")]
        total = int(_get(out, "total"))
        failed = int(_get(out, "failed"))

        valid_personas = []
        for p in personas:
            try:
                valid_personas.append(PersonaProfile.model_validate(p).model_dump(mode="json"))
            except ValidationError:
                valid_personas.append(p)  # keep as-is; analytics tolerates missing fields poorly, so log
                log.warning("persona %s failed schema validation", p.get("persona_id"))
        known_ids = {p["persona_id"] for p in valid_personas}

        valid: list[dict[str, Any]] = []
        for r in _get(out, "responses"):
            try:
                resp = AgentResponse.model_validate(_to_dict(r))
            except ValidationError:
                failed += 1
                continue
            if resp.persona_id not in known_ids:
                failed += 1
                continue
            valid.append(resp.model_dump(mode="json"))

        if not valid:
            raise RuntimeError("No valid agent responses were produced")

        report = report_service.build_report(sim_id, product, valid_personas, valid, failed, total)

        async with SessionLocal() as s:
            s.add_all([PersonaORM(simulation_id=sim_id, persona_id=p["persona_id"], data=p) for p in valid_personas])
            s.add_all([ResponseORM(simulation_id=sim_id, persona_id=r["persona_id"], data=r) for r in valid])
            await s.commit()

        await _update(
            sim_id,
            status="completed",
            total_personas=total,
            completed_personas=total,
            failed_personas=failed,
            report=report,
            error=None,
        )
    except Exception as exc:  # noqa: BLE001
        log.exception("simulation %s failed", sim_id)
        await _update(sim_id, status="failed", error=str(exc))


async def load_responses(s, sim_id: str) -> list[dict[str, Any]]:
    rows = (await s.execute(select(ResponseORM.data).where(ResponseORM.simulation_id == sim_id))).scalars().all()
    return list(rows)
