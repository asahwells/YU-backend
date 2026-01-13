"""
Service layer for interacting with the Hugging Face toxic comment classification pipeline.
"""

from functools import lru_cache
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

from .config import settings
from .models import ToxicityResult





def _build_pipeline():
    # Helper to load the model from Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(settings.model_name)
    return TextClassificationPipeline(model=model, tokenizer=tokenizer)


@lru_cache(maxsize=1)
def get_model():
    return _build_pipeline()


def classify_message(text: str) -> ToxicityResult:
    # Main logic to check if text is toxic
    pipe = get_model()
    result = pipe(text)[0]
    
    label = result["label"].upper()
    score = float(result["score"])

    return ToxicityResult(label=label, confidence=score)

