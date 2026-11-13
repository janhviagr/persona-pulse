import asyncio
import os

from dotenv import load_dotenv


def default_concurrency() -> int:
    """Reads MAX_CONCURRENT_AGENTS from .env (default 10)."""
    load_dotenv()
    try:
        return max(1, int(os.getenv("MAX_CONCURRENT_AGENTS", "10")))
    except ValueError:
        return 10


async def run_agents(
    agents: list,
    product: dict,
    max_concurrent: int | None = None,
    on_progress=None,
) -> list[dict]:
    """Run every agent on the product, at most `max_concurrent` at a time.

    Returns one result dict per agent, in the same order as `agents`.
    Never raises: a failed agent shows up as {"status": "invalid", ...}.

    on_progress (optional) is called after each agent finishes:
        on_progress(completed, failed, total)
    where `completed` counts every finished agent, including failed ones.
    """
    limit = max_concurrent or default_concurrency()
    gate = asyncio.Semaphore(limit)  # only `limit` agents may be inside at once
    total = len(agents)
    counts = {"completed": 0, "failed": 0}

    async def run_one(agent) -> dict:
        async with gate:
            try:
                result = await agent.evaluate_product(product)
            except Exception as error:  # safety net; agents should never raise
                result = {
                    "persona_id": agent.persona.get("persona_id", "unknown"),
                    "status": "invalid",
                    "error": f"{type(error).__name__}: {error}",
                }
        counts["completed"] += 1
        if result.get("status") != "ok":
            counts["failed"] += 1
        if on_progress:
            on_progress(counts["completed"], counts["failed"], total)
        return result

    return list(await asyncio.gather(*(run_one(agent) for agent in agents)))
