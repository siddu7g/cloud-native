"""Configuration for lab3 OpenRouter client."""

import os

OPENROUTER_API_KEY: str = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL: str = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL: str = "openai/gpt-4o-mini"
