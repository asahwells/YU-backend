"""
Lightweight tests for the moderation endpoint.
"""

from fastapi.testclient import TestClient
import pytest

from app.main import app
from app import services
from app.models import SentimentResult

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cache():
    """Ensure per-test isolation for cached pipeline calls."""

    services.get_sentiment_pipeline.cache_clear()  # type: ignore[attr-defined]
    yield
    services.get_sentiment_pipeline.cache_clear()  # type: ignore[attr-defined]


def test_rejects_high_confidence_negative(monkeypatch):
    """Requests should be blocked when the model is confident a message is negative."""

    monkeypatch.setattr(
        services,
        "analyze_text",
        lambda _text: SentimentResult(label="NEGATIVE", confidence=0.93),
    )

    response = client.post("/api/check-message", json={"text": "You are awful."})
    assert response.status_code == 400
    detail = response.json()
    assert detail["status"] == "rejected"
    assert detail["label"] == "NEGATIVE"


def test_accepts_positive_or_low_confidence(monkeypatch):
    """Requests should succeed when the message is allowed."""

    monkeypatch.setattr(
        services,
        "analyze_text",
        lambda _text: SentimentResult(label="POSITIVE", confidence=0.52),
    )

    response = client.post("/api/check-message", json={"text": "Great job!"})
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "accepted"
    assert payload["label"] == "POSITIVE"

