"""Coordinate Person 3 evaluations and pass validated results to analytics."""

from collections.abc import Mapping, Sequence
from typing import Any
from uuid import uuid4

from ai_engine.agents import run_agents
from ai_engine.evaluation import generate_report, validate_responses
from ai_engine.personas.persona_model import Persona
from pydantic import ValidationError


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="python")
    raise TypeError("Expected a mapping or a Pydantic model")


def _get(value: Any, field: str, default: Any = None) -> Any:
    return value.get(field, default) if isinstance(value, Mapping) else getattr(value, field, default)


class SimulationManager:
    """Run the existing agents or delegate generation and execution to Person 3.

    Pass ``agents`` to use Person 3's ``run_agents`` interface directly. If
    omitted, this manager calls Person 3's ``evaluate_with_personas`` entry
    point, which is available on ``feature/persona-engine``.
    """

    def __init__(self, llm: Any = None, max_concurrent: int | None = None):
        if max_concurrent is not None and max_concurrent < 1:
            raise ValueError("max_concurrent must be at least 1")
        self.llm = llm
        self.max_concurrent = max_concurrent

    async def run(
        self,
        product: Mapping[str, Any],
        agents: Sequence[Any] | None = None,
        simulation_id: str | None = None,
        audience_config: Mapping[str, Any] | None = None,
        count: int | None = None,
        on_progress=None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """Run, collect, validate, and report one simulation.

        The returned ``responses`` keeps Person 3's raw result shape for
        compatibility. ``valid_responses`` contains only schema-valid,
        persona-matched results and is the only input to analytics.
        """
        simulation_id = simulation_id or str(uuid4())
        product_data = dict(product)

        if agents is not None:
            agent_list = list(agents)
            personas = [getattr(agent, "persona", None) for agent in agent_list]
            raw_responses = await run_agents(
                agent_list,
                product_data,
                max_concurrent=self.max_concurrent,
                on_progress=on_progress,
            )
            total = len(agent_list)
            reported_failed = sum(1 for response in raw_responses if _get(response, "status") != "ok")
        else:
            if count is None or count < 1:
                raise ValueError("count must be a positive integer when agents are not supplied")
            try:
                from ai_engine.agents import evaluate_with_personas
            except ImportError as error:
                raise RuntimeError(
                    "Person 3's evaluate_with_personas interface is unavailable; integrate feature/persona-engine."
                ) from error
            output = await evaluate_with_personas(
                product_data,
                dict(audience_config or {}),
                count,
                llm=self.llm,
                seed=seed,
                max_concurrent=self.max_concurrent,
                on_progress=on_progress,
            )
            personas = list(_get(output, "personas", []))
            raw_responses = list(_get(output, "responses", []))
            total = int(_get(output, "total", max(count, len(raw_responses))))
            reported_failed = int(_get(output, "failed", 0))

        normalized_personas: list[dict[str, Any]] = []
        for persona in personas:
            try:
                normalized_personas.append(
                    Persona.model_validate(_as_dict(persona)).model_dump(mode="python")
                )
            except (ValidationError, TypeError, ValueError):
                # Invalid profiles cannot be used to match or segment responses.
                continue

        known_persona_ids = {persona["persona_id"] for persona in normalized_personas}
        raw_dicts: list[dict[str, Any]] = []
        valid_responses: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        accepted_ids: set[str] = set()

        for raw_response in raw_responses:
            try:
                response_data = _as_dict(raw_response)
            except (TypeError, ValueError) as error:
                failures.append({"status": "invalid", "error": str(error)})
                continue
            raw_dicts.append(response_data)
            persona_id = response_data.get("persona_id")

            # The agent runner's raw contract requires an explicit successful
            # status. AgentResponse itself has no status field.
            if response_data.get("status") != "ok":
                failures.append({
                    "persona_id": persona_id,
                    "status": "invalid",
                    "error": response_data.get("error", "Response status was not 'ok'."),
                })
                continue

            checked, rejected = validate_responses([response_data], known_persona_ids)
            if rejected or not checked:
                failures.append({
                    "persona_id": persona_id,
                    "status": "invalid",
                    "error": "Response failed AgentResponse validation or persona matching.",
                })
                continue
            if persona_id in accepted_ids:
                failures.append({
                    "persona_id": persona_id,
                    "status": "invalid",
                    "error": "Duplicate response for persona.",
                })
                continue

            accepted_ids.add(persona_id)
            valid_responses.append({**checked[0], "status": "ok"})

        total = max(int(total), len(raw_dicts), len(normalized_personas), reported_failed + len(valid_responses))
        failed = total - len(valid_responses)

        # A runner should return one result per attempted agent. Preserve the
        # reported count and make missing result records explicit if it did not.
        while len(failures) < failed:
            failures.append({
                "persona_id": None,
                "status": "invalid",
                "error": "No response was returned for an attempted persona.",
            })

        report = generate_report(
            simulation_id,
            product_data,
            normalized_personas,
            valid_responses,
        )
        report_failed = report.get("failed_responses", 0)
        report["failed_responses"] = failed
        if failed != report_failed:
            report["limitations"].append(
                f"The simulation runner reported {failed} failed or excluded evaluations."
            )

        return {
            "simulation_id": simulation_id,
            "personas": normalized_personas,
            "responses": raw_dicts,
            "valid_responses": valid_responses,
            "failures": failures,
            "total": total,
            "failed": failed,
            "sample_size": len(valid_responses),
            "report": report,
        }
