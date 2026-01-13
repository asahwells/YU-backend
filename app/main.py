"""
FastAPI application entry point for the low-latency moderation API.
"""

from fastapi import FastAPI, HTTPException

from .config import settings
from .models import IncomingMessage, FilterResult
from . import services

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
async def load_model():
    # Load model into memory so the first request isn't slow
    print("Loading model...")
    services.get_model()
    print("Model loaded!")


@app.post("/api/check-message", response_model=FilterResult)
async def check_message(msg: IncomingMessage):
    
    # Run the classification
    result = services.classify_message(msg.text)

    # Block if toxic and confident
    if result.label == "TOXIC" and result.confidence >= settings.negative_threshold:
        return FilterResult(
            status="rejected",
            message="Message was flagged as toxic.",
            label=result.label,
            confidence=result.confidence,
        )

    # Otherwise accept
    return FilterResult(
        status="accepted",
        message="Message is safe.",
        label=result.label,
        confidence=result.confidence,
    )

