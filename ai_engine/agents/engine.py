from ai_engine.personas import generate_personas

from .agent_factory import AgentFactory
from .agent_runner import run_agents


async def evaluate_with_personas(
    product: dict,
    audience_config: dict,
    count: int,
    llm=None,
    seed: int | None = None,
    max_concurrent: int | None = None,
    on_progress=None,
) -> dict:
    """Generate `count` personas, have each one evaluate the product, return everything.

    Returns:
        {
          "personas":  list of persona dicts,
          "responses": list of result dicts, same order as personas
                       (each has "status": "ok" or "invalid"),
          "total":     number of personas,
          "failed":    number of responses that are not "ok",
        }
    If `llm` is None, a GeminiProvider is created (needs GEMINI_API_KEY in .env).
    """
    if llm is None:
        from ai_engine.llm import GeminiProvider  # imported here so tests never need a key

        llm = GeminiProvider()

    personas = generate_personas(audience_config, count, seed=seed)
    agents = AgentFactory.create_agents(personas, llm)
    responses = await run_agents(
        agents, product, max_concurrent=max_concurrent, on_progress=on_progress
    )
    failed = sum(1 for r in responses if r.get("status") != "ok")
    return {
        "personas": personas,
        "responses": responses,
        "total": len(responses),
        "failed": failed,
    }


async def evaluate_price_scenarios(
    product: dict,
    audience_config: dict,
    count: int,
    prices: list[float],
    llm=None,
    seed: int | None = None,
    max_concurrent: int | None = None,
    on_progress=None,
) -> dict:
    """Show the SAME personas the product at several prices.

    Returns:
        {
          "personas":  list of persona dicts (identical for every price),
          "scenarios": [
              {"price": 2999, "currency": "INR", "responses": [...], "total": 50, "failed": 1},
              ...one entry per price, in the order given...
          ],
        }
    Calls to the LLM = count x number of prices, so start with a small count.
    on_progress(completed, failed, total) restarts at 0 for each price.
    """
    if llm is None:
        from ai_engine.llm import GeminiProvider

        llm = GeminiProvider()

    personas = generate_personas(audience_config, count, seed=seed)
    agents = AgentFactory.create_agents(personas, llm)

    scenarios = []
    for price in prices:
        scenario_product = {**product, "price": price}
        responses = await run_agents(
            agents, scenario_product, max_concurrent=max_concurrent, on_progress=on_progress
        )
        failed = sum(1 for r in responses if r.get("status") != "ok")
        scenarios.append({
            "price": price,
            "currency": product.get("currency", ""),
            "responses": responses,
            "total": len(responses),
            "failed": failed,
        })
    return {"personas": personas, "scenarios": scenarios}
