"""
Service layer for interacting with the Hugging Face toxic comment classification pipeline.
"""

from functools import lru_cache
from typing import Callable, List, TypedDict

from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

from .config import get_settings
from .models import ToxicityResult


class PipelineOutput(TypedDict):
    label: str
    score: float


def _build_pipeline() -> Callable[[str], List[PipelineOutput]]:
    """
    Instantiate the Hugging Face TextClassificationPipeline for toxic comment detection.
    Returns a callable that accepts text and yields label/score dictionaries.
    """

    settings = get_settings()
    tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(settings.model_name)
    return TextClassificationPipeline(model=model, tokenizer=tokenizer)


@lru_cache(maxsize=1)
def get_toxicity_pipeline() -> Callable[[str], List[PipelineOutput]]:
    """Return a cached instance of the toxicity classification pipeline."""

    return _build_pipeline()


def analyze_text(text: str) -> ToxicityResult:
    """
    Run toxicity classification on text and normalize the response.
    The model outputs labels that we normalize to TOXIC/NON-TOXIC.
    """

    predictor = get_toxicity_pipeline()
    result = predictor(text)[0]
    raw_label = result["label"].upper()
    confidence = float(result["score"])
    # print(f"{raw_label}....raw_label, {result}")

    return ToxicityResult(label=raw_label, confidence=confidence)

