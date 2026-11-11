import asyncio
import time

from ai_engine.agents import ConsumerAgent
from ai_engine.llm import LLMProvider
from ai_engine.llm.gemini_provider import RateLimiter, parse_retry_delay
from ai_engine.personas import generate_personas

PRODUCT = {"product_id": "PROD001", "name": "Watch", "description": "A watch",
           "category": "Wearable", "price": 4999, "currency": "INR", "features": []}
PERSONA = generate_personas({}, 1, seed=1)[0]


class BrokenLLM(LLMProvider):
    def __init__(self):
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        raise RuntimeError("quota exceeded")


def test_parse_retry_delay():
    assert round(parse_retry_delay("Please retry in 10.155100627s."), 2) == 10.16
    assert round(parse_retry_delay("Please retry in 547.339734ms."), 3) == 0.547
    assert parse_retry_delay("something else entirely") is None


def test_rate_limiter_spaces_requests():
    limiter = RateLimiter(per_minute=1200)  # one request every 0.05s

    async def burst():
        await asyncio.gather(*(limiter.wait() for _ in range(5)))

    start = time.monotonic()
    asyncio.run(burst())
    assert time.monotonic() - start >= 0.18  # 5 requests need 4 gaps of 0.05s


def test_llm_failure_is_not_retried_by_the_agent():
    llm = BrokenLLM()
    result = asyncio.run(ConsumerAgent(PERSONA, llm).evaluate_product(PRODUCT))
    assert result["status"] == "invalid"
    assert result["error"].startswith("LLMError")
    assert llm.calls == 1
