class LLMProvider:
    """Template for any AI model. Every provider must implement generate()."""

    async def generate(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement generate()")
