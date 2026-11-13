# Persona and Agent Engine: Design Notes

Owner: Person 3. Code lives in `ai_engine/personas`, `ai_engine/agents`, `ai_engine/llm`, `ai_engine/prompts`.

## What it does

1. Generates a population of synthetic consumers (personas) that fits a chosen audience.
2. Makes each persona evaluate a product independently, using an LLM.
3. Returns one validated result per persona. Failed agents are marked, never hidden.

## How to call it

    from ai_engine.agents import evaluate_with_personas

    out = await evaluate_with_personas(product, audience_config, count=50)
    out["personas"]    # list of persona dicts
    out["responses"]   # list of result dicts, same order as personas
    out["failed"]      # number of responses whose status is not "ok"

`audience_config` keys (all optional): `age_groups` (for example "18-24", "55+"), `interests` (list), `archetypes` (list of archetype names).

## Price scenarios

    from ai_engine.agents import evaluate_price_scenarios

    out = await evaluate_price_scenarios(product, audience_config, count=20, prices=[2999, 4999, 7999])
    out["personas"]    # the same personas for every price
    out["scenarios"]   # list of {price, currency, responses, total, failed}, in the order given

The same personas see every price, so differences between prices come only from the price. LLM calls = personas x prices.

## Response status

Every result has `status`. `"ok"` means all fields passed validation. `"invalid"` means the agent failed after 3 attempts and carries an `error` message instead of scores. Scoring must use `"ok"` results only and report the invalid count as failed personas.

Optional fields: `would_recommend`, `positive_factors` and `negative_factors` are left out of the result when the agent did not provide them. A missing `would_recommend` means "no answer", which is different from `false` ("the persona said no"). Read these fields with `.get()`, for example `result.get("would_recommend")`. `persona_id`, `product_id`, `status` and all scores are always present in an `"ok"` result.

## How personas are built

- Age comes from the chosen age groups. Occupation depends on age. Income is picked from the levels that are believable for the occupation.
- Each persona gets one of 8 archetypes that fits its age group (budget_student, tech_enthusiast, working_professional, family_consumer, traditional_consumer, trend_follower, health_conscious, premium_consumer). About 30% blend two archetypes.
- Numeric traits (0 to 1) are drawn from ranges combined from age, income and archetype.
- A `seed` makes generation repeatable.

## Rules the agents follow

- Each agent sees only its own persona and the product, never other agents' answers.
- Replies must be JSON and are validated against `AgentResponse`. Broken replies are retried up to 3 times.
- Concurrency is limited (`MAX_CONCURRENT_AGENTS`, default 10) to respect API rate limits.
- Output length per call is capped (`max_output_tokens`).

## Known limitations (include in reports)

- Personas are synthetic. They are not real survey respondents and do not predict real sales.
- Absolute scores run low, because agents are told to avoid polite middle-of-the-road answers. Use scores to compare segments or price points, not as probabilities.
- `price_acceptance` is largely driven by the persona's income level and price sensitivity, so it is not fully independent of them.
- Product wording changes reactions. Words like "cheap" or "affordable" in a description shift how premium personas respond.
- The LLM is not deterministic: two runs on the same persona can differ slightly.
- No calibration against real consumer data has been done yet.

- Segment results depend on the archetype mix. High income appears only with the Premium archetype, so "High income" segments mostly reflect premium taste. Small segments (under about 15 personas) are noisy.
- On a free Gemini key the provider is limited to about 12 requests per minute (`GEMINI_REQUESTS_PER_MINUTE`). Rough run times: 20 personas about 2 minutes, 50 about 4 to 5 minutes, 100 about 8 to 9 minutes. Price scenarios multiply this by the number of prices.
