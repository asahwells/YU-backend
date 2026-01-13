"""
Pydantic models shared across the API.
"""

from typing import Literal

from pydantic import BaseModel, Field


class IncomingMessage(BaseModel):
    text: str = Field(..., min_length=1)


class ToxicityResult(BaseModel):
    """Normalized output from the toxicity classification model."""

    label: Literal["TOXIC", "NON-TOXIC"]
    confidence: float = Field(..., ge=0.0, le=1.0)


class FilterResult(BaseModel):
    status: Literal["accepted", "rejected"]
    message: str
    label: Literal["TOXIC", "NON-TOXIC"]
    confidence: float

