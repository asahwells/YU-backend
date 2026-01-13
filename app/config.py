"""
Configuration helpers for the moderation service.
"""

import os

class Settings:
    # Default config
    model_name = "martin-ha/toxic-comment-model"
    negative_threshold = 0.90
    api_title = "YuChat NLP Backend"
    api_description = "API for filtering toxic messages in YuChat."
    api_version = "1.0.0"

    def __init__(self):
        # Override with env vars if they exist
        self.model_name = os.getenv("MODEL_NAME", self.model_name)
        self.negative_threshold = float(os.getenv("NEGATIVE_THRESHOLD", self.negative_threshold))

settings = Settings()

