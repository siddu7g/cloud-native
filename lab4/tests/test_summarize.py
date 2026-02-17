"""Tests for POST /summarize endpoint."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

AUTH_HEADERS = {"Authorization": "Bearer dev-token"}


@pytest.fixture(autouse=True)
def _ensure_config_loaded():
    """Ensure config module is imported so dotenv loads (tests may override env)."""
    import app.config  # noqa: F401
    yield


def _mock_openrouter_response(summary_text: str):
    """Build a mock OpenRouter API response."""
    return MagicMock(
        status_code=200,
        json=lambda: {
            "choices": [
                {"message": {"content": summary_text}}
            ]
        },
        raise_for_status=MagicMock(),
    )


@patch("app.summarizer.OPENROUTER_API_KEY", "test-key")
@patch("app.summarizer.httpx.post")
def test_summarize_valid_with_truncation(mock_post):
    """Valid request with truncation returns first max_length words, truncated=True."""
    mock_post.return_value = _mock_openrouter_response(
        "One two three four five six seven eight"
    )
    response = client.post(
        "/summarize",
        json={"text": "A B C D E F G H", "max_length": 5},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "model" in data
    assert data["truncated"] is True
    words = data["summary"].split()
    assert len(words) <= 5
    assert data["model"] != "placeholder"  # comes from OpenRouter model


@patch("app.summarizer.OPENROUTER_API_KEY", "test-key")
@patch("app.summarizer.httpx.post")
def test_summarize_valid_without_truncation(mock_post):
    """Valid request without truncation returns full summary, truncated=False."""
    mock_post.return_value = _mock_openrouter_response("Short summary.")
    response = client.post(
        "/summarize",
        json={"text": "Some input text.", "max_length": 100},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["truncated"] is False
    assert "summary" in data


def test_summarize_missing_text():
    """Missing text returns 422."""
    response = client.post(
        "/summarize",
        json={"max_length": 10},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422


def test_summarize_empty_text():
    """Empty text returns 422."""
    response = client.post(
        "/summarize",
        json={"text": "", "max_length": 10},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422


def test_summarize_missing_authorization():
    """Missing Authorization header returns 401."""
    response = client.post(
        "/summarize",
        json={"text": "Hello world", "max_length": 5},
    )
    assert response.status_code == 401
    assert "error" in response.json() or "detail" in response.json()


def test_summarize_invalid_token():
    """Invalid token returns 401."""
    response = client.post(
        "/summarize",
        json={"text": "Hello world", "max_length": 5},
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_health_without_auth():
    """GET /health works without authorization."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@patch("app.summarizer.OPENROUTER_API_KEY", "")
@patch("app.summarizer.httpx.post")
def test_summarize_missing_api_key(mock_post):
    """Missing OPENROUTER_API_KEY returns 500."""
    mock_post.side_effect = AssertionError("Should not call API when key is missing")
    response = client.post(
        "/summarize",
        json={"text": "Hello world", "max_length": 5},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 500
    data = response.json()
    detail = data.get("detail")
    assert "OPENROUTER_API_KEY" in str(detail)
