from .llm_provider import LLMProvider


class MockLLMProvider(LLMProvider):
    """Fake LLM for tests. Returns the given replies in order, repeating the last one."""

    def __init__(self, responses: list[str]):
        self.responses = list(responses)
        self.calls = 0
        self.prompts: list[str] = []

    async def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        index = min(self.calls, len(self.responses) - 1)
        self.calls += 1
        return self.responses[index]
