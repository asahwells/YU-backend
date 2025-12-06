# Low-Latency Moderation API

Backend service built with FastAPI that intercepts chat messages, classifies them with a DistilBERT sentiment model, and blocks high-confidence negative text in under 150 ms.

## Features

- Uses Hugging Face `distilbert-base-uncased-finetuned-sst-2-english`
- Model is loaded once on startup to avoid per-request overhead
- Single endpoint `POST /api/check-message`
- Configurable negative-confidence threshold via env vars
- Pytest suite with FastAPI TestClient stubs

## Project Layout

```
├── app
│   ├── __init__.py
│   ├── config.py          # Settings + env overrides
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # Pydantic request/response models
│   └── services.py        # Pipeline loader + sentiment helpers
├── tests
│   └── test_api.py
├── requirements.txt
└── README.md
```

## Getting Started

1. **Install dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **(Optional) Configure environment**

   ```bash
   export MODEL_NAME=martin-ha/toxic-comment-model
   export NEGATIVE_THRESHOLD=0.9
   ```

3. **Run the API**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Call the endpoint**
   ```bash
   curl -X POST http://localhost:8000/api/check-message \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this!"}'
   ```

## Testing

```
pytest
```

Tests monkeypatch the service layer so they run quickly without downloading the model.
