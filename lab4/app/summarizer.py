"""Summarization logic: placeholder or OpenRouter-based."""
import httpx
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL


class SummarizationError(Exception):
    """Raised when summarization fails (missing key, upstream error)."""
    pass


def process_summary(text: str, max_length: int) -> dict:
    """
    Summarize text using OpenRouter API when configured,
    or raise if API key is missing.
    """
    if not OPENROUTER_API_KEY:
        raise SummarizationError("OPENROUTER_API_KEY is not set")

    prompt = (
        f"Summarize the following text in at most {max_length} words. "
        f"Return only the summary, no additional commentary.\n\n{text}"
    )

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://lab4.local",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_length * 2,  # Allow enough tokens for summary
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError as e:
        raise SummarizationError(f"OpenRouter API error: {e.response.status_code} - {e.response.text}") from e
    except httpx.RequestError as e:
        raise SummarizationError(f"OpenRouter request failed: {str(e)}") from e

    content = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
        .strip()
    )

    if not content:
        raise SummarizationError("OpenRouter returned empty response")

    words = content.split()
    is_truncated = len(words) > max_length
    summary_text = " ".join(words[:max_length]) if is_truncated else content

    return {
        "summary": summary_text,
        "model": OPENROUTER_MODEL,
        "truncated": is_truncated,
    }
