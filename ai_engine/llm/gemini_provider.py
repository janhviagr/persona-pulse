import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .llm_provider import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        model: str = "gemini-3.5-flash-lite",
        max_output_tokens: int = 1024,
        temperature: float = 0.8,
        max_retries: int = 3,
    ):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.max_retries = max_retries

    async def generate(self, prompt: str) -> str:
        for attempt in range(self.max_retries):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=self.max_output_tokens,
                        temperature=self.temperature,
                    ),
                )
                return response.text or ""
            except Exception as error:
                if attempt == self.max_retries - 1:
                    raise
                wait_seconds = 2 ** attempt
                print(f"Gemini call failed ({error}). Retrying in {wait_seconds}s...")
                await asyncio.sleep(wait_seconds)
