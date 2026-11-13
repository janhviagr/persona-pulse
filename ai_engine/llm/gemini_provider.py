import os
import re
import time
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .llm_provider import LLMProvider

# HTTP codes worth retrying: rate limit, server errors, "busy".
RETRYABLE_CODES = {429, 500, 502, 503, 504}


def parse_retry_delay(message: str) -> float | None:
    """Find 'retry in 10.5s' or 'retry in 547ms' in an error message. Returns seconds."""
    match = re.search(r"retry in ([\d.]+)\s*(ms|s)\b", message)
    if not match:
        return None
    value = float(match.group(1))
    return value / 1000 if match.group(2) == "ms" else value


class RateLimiter:
    """Spaces out requests so we never exceed `per_minute` calls per minute."""

    def __init__(self, per_minute: float):
        self.interval = 60.0 / per_minute
        self._next = 0.0

    async def wait(self) -> None:
        now = time.monotonic()
        start = max(now, self._next)
        self._next = start + self.interval  # reserve this time slot
        if start > now:
            await asyncio.sleep(start - now)


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        model: str = "gemini-3.5-flash-lite",
        max_output_tokens: int = 1024,
        temperature: float = 0.8,
        max_retries: int = 6,
        requests_per_minute: float | None = None,
    ):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

        if requests_per_minute is None:
            try:
                requests_per_minute = float(os.getenv("GEMINI_REQUESTS_PER_MINUTE", "12"))
            except ValueError:
                requests_per_minute = 12.0

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.max_retries = max_retries
        self.limiter = RateLimiter(requests_per_minute)

    async def generate(self, prompt: str) -> str:
        for attempt in range(self.max_retries):
            await self.limiter.wait()
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
                code = getattr(error, "code", None)
                retryable = code is None or code in RETRYABLE_CODES
                if not retryable or attempt == self.max_retries - 1:
                    raise  # wrong key, wrong model name, or out of retries

                suggested = parse_retry_delay(str(error))
                if suggested is not None:
                    wait_seconds = min(suggested + 1, 65)  # Gemini told us how long to wait
                else:
                    wait_seconds = min(2 ** (attempt + 1), 30)
                print(f"  Gemini is limited or busy (code {code}). Waiting {wait_seconds:.0f}s, then retrying...")
                await asyncio.sleep(wait_seconds)
