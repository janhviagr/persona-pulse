from .json_utils import extract_json
from .prompt_builder import build_prompt
from .response_model import AgentResponse


class ConsumerAgent:
    """One synthetic customer. Evaluates a product from its own point of view."""

    def __init__(self, persona: dict, llm, max_attempts: int = 3):
        self.persona = persona
        self.llm = llm
        self.max_attempts = max_attempts

    def _invalid(self, error: str) -> dict:
        return {
            "persona_id": self.persona["persona_id"],
            "status": "invalid",
            "error": error[:300],
        }

    async def evaluate_product(self, product: dict) -> dict:
        """Always returns a dict and never raises.

        Success: the AgentResponse fields plus "status": "ok".
        Failure: {"persona_id", "status": "invalid", "error"}.
        """
        prompt = build_prompt(self.persona, product)
        last_error = "unknown error"

        for _ in range(self.max_attempts):
            try:
                raw = await self.llm.generate(prompt)
            except Exception as error:
                # The provider already retried. Retrying here would only burn more quota.
                return self._invalid(f"LLMError: {type(error).__name__}: {error}")

            try:
                data = extract_json(raw)
                # The agent sets these itself, so the model can't get them wrong.
                data["persona_id"] = self.persona["persona_id"]
                data["product_id"] = product.get("product_id", "")
                checked = AgentResponse(**data).model_dump()
                return {**checked, "status": "ok"}
            except Exception as error:  # bad JSON or bad scores: ask again
                last_error = f"{type(error).__name__}: {error}"

        return self._invalid(last_error)
