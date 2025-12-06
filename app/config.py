"""
Configuration helpers for the moderation service.
"""

from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    """Simple immutable settings object."""

    model_name: str = "martin-ha/toxic-comment-model"
    negative_threshold: float = 0.90
    api_title: str = "Low-Latency Moderation API"
    api_description: str = (
        "Intercepts chat messages and blocks high-confidence toxic content in under 150ms."
    )
    api_version: str = "1.0.0"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Load settings once, allowing environment variables to override defaults.

    Environment variables:
        MODEL_NAME: Hugging Face model identifier.
        NEGATIVE_THRESHOLD: Float between 0 and 1 for blocking TOXIC messages.
    """

    model_name = os.getenv("MODEL_NAME", Settings.model_name)
    negative_threshold = float(os.getenv("NEGATIVE_THRESHOLD", Settings.negative_threshold))

    return Settings(model_name=model_name, negative_threshold=negative_threshold)

