"""OpenRouter API client with retries and timeouts."""

import httpx

from app.config import DEFAULT_MODEL, OPENROUTER_API_KEY, OPENROUTER_URL
from app.retry import retry_async


# Simple example prompt for quick testing
SIMPLE_PROMPT = "Say 'Hello!' in one word."


class OpenRouterClient:
    def __init__(self, model: str = DEFAULT_MODEL, timeout_s: float = 15.0) -> None:
        self.model = model
        self.timeout_s = timeout_s

    async def generate(self, prompt: str) -> str:
        """
        Requirements:
        - Use httpx.AsyncClient
        - Apply timeout
        - Retry on timeouts, transport errors, HTTP 429 and 5xx
        - Do NOT retry on other 4xx errors
        """

        def should_retry(e: Exception) -> bool:
            """Retry on timeouts, transport errors, 429, 5xx. Don't retry other 4xx."""
            if isinstance(e, httpx.HTTPStatusError):
                status = e.response.status_code
                if 400 <= status < 500 and status != 429:
                    return False
            return True

        async def _do_request() -> str:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                response = await client.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return content.strip()

        return await retry_async(_do_request, retries=3, retry_if=should_retry)
