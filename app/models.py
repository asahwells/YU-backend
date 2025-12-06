"""
Pydantic models shared across the API.
"""

from typing import Literal

from pydantic import BaseModel, Field


class MessagePayload(BaseModel):
    """Incoming chat message payload."""

    text: str = Field(..., min_length=1, description="User-provided message to moderate.")


class ToxicityResult(BaseModel):
    """Normalized output from the toxicity classification model."""

    label: Literal["TOXIC", "NON-TOXIC"]
    confidence: float = Field(..., ge=0.0, le=1.0)


class ModerationResponse(BaseModel):
    """API response returned to the chat application."""

    status: Literal["accepted", "rejected"]
    message: str
    label: Literal["TOXIC", "NON-TOXIC"]
    confidence: float

