"""
FastAPI application entry point for the low-latency moderation API.
"""

from fastapi import FastAPI, HTTPException

from .config import get_settings
from .models import MessagePayload, ModerationResponse
from . import services

settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)


@app.get("/")
async def health_check():
    """Simple health check to wake up the service."""
    return {"status": "ok", "message": "Service is active"}


@app.on_event("startup")
async def warm_model_cache() -> None:
    """Load the toxicity classification pipeline during startup to avoid request-time latency."""

    services.get_toxicity_pipeline()


@app.post("/api/check-message", response_model=ModerationResponse)
async def check_message(payload: MessagePayload) -> ModerationResponse:
    """
    Classify the incoming text and block highly confident toxic content.
    """

    result = services.analyze_text(payload.text)

    if result.label == "TOXIC" and result.confidence >= settings.negative_threshold:
        return ModerationResponse(
                status="rejected",
                message="Message classified as toxic with high confidence.",
                label=result.label,
                confidence=result.confidence,
            )
        

    return ModerationResponse(
        status= "rejected" if result.label == "TOXIC" else "accepted",
        message="Message passed moderation.",
        label=result.label,
        confidence=result.confidence,
    )

