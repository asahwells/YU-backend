---
title: Toxic Comment
emoji: 👁
colorFrom: indigo
colorTo: green
sdk: docker
pinned: false
---

# YuChat NLP Backend

## Project Overview

I built this backend service to support **YuChat**, my mobile chat application (developed with React Native and Expo). While building the frontend, I realized that relying on client-side checks for user safety wasn't enough. I needed a robust, server-side way to filter out toxic messages in real-time.

The goal was simple: create a low-latency API that intercepts messages and checks them against a toxicity model before they even reach the recipient. I wanted to keep the community environment healthy without slowing down the chat experience.

---

## Functional Analysis

The backend service supports the following core functions:

1. **Message Moderation API**: A dedicated endpoint to receive text content from the YuChat client.
2. **Toxicity Classification**: Utilizes a pre-trained NLP model (e.g., DistilBERT or Toxic Comment Model) to analyze the sentiment/toxicity of the input text.
3. **Threshold-Based Filtering**: Automatically accepts or rejects messages based on a configurable confidence threshold (e.g., rejecting messages with >0.9 toxicity confidence).
4. **Model Management**: Efficiently loads the heavy NLP model into memory upon application startup to ensure 150ms response times for subsequent requests.

---

## Module Design

The architecture is built using **FastAPI** to ensure modularity and performance.

### Architecture Overview
The system follows a layered architecture:

-   **API Layer (`app/main.py`)**:
    -   **Entry Point**: Manages the HTTP server and API routing.
    -   **Endpoints**: Exposes `POST /api/check-message`.
    -   **Lifecycle**: Handles model pre-loading on startup (`@app.on_event("startup")`).

-   **Service Layer (`app/services.py`)**:
    -   **Inference Engine**: Encapsulates the logic for the specific NLP model (Hugging Face Transformers).
    -   **Abstraction**: Provides a clean `analyze_text(text)` function used by the API layer, isolating the complex model logic.

-   **Data Model Layer (`app/models.py`)**:
    -   **Schema Definition**: Uses Pydantic to strictly define input (`MessagePayload`) and output (`ModerationResponse`) structures, ensuring data validation.

-   **Configuration Layer (`app/config.py`)**:
    -   **Environment Management**: Centralizes settings such as `NEGATIVE_THRESHOLD`, `MODEL_NAME`, and API metadata, reading from environment variables.

### Directory Structure
```
├── app
│   ├── __init__.py
│   ├── config.py          # Configuration & Enironment Variables
│   ├── main.py            # API Routes & Entry Point
│   ├── models.py          # Data Objects (Request/Response)
│   └── services.py        # Business Logic & ML Model Inference
├── check_model_size.py    # Utility script
├── requirements.txt       # Dependencies
└── README.md              # Project Documentation
```

---

## Interface Analysis

### Data Exchange
The system uses **JSON** over **HTTP** for all data exchange between the YuChat React Native client (APK) and the Hugging Face Space.

**Input Interface (Client -> Server):**
-   **Method**: `POST`
-   **Endpoint**: `/api/check-message`
-   **Header**: `Content-Type: application/json`
-   **Payload**:
    ```json
    {
      "text": "User message content here"
    }
    ```

**Output Interface (Server -> Client):**
-   **Format**: JSON
-   **Structure**:
    ```json
    {
      "status": "accepted" | "rejected",
      "message": "Description of the result",
      "label": "TOXIC" | "non-toxic",
      "confidence": 0.98
    }
    ```

### Deployment Infrastructure
The interface is hosted on a cloud environment to support the mobile client.

-   **Platform**: Hugging Face Spaces
-   **Runtime**: Docker Container (via Dockerfile)
-   **Resources**: Hugging Face Spaces (Standard CPU).
-   **Client**: YuChat React Native APK.

---

## Design Choices

### Why FastAPI?
I decided to stick with **FastAPI** for this backend. I've used it before (like for my text summarization API projects) and it's always been reliable.
- **Speed**: Since this is for a chat app, latency is everything. FastAPI's async support means I can handle incoming requests quickly while the model processes in the background.
- **Developer Experience**: I really like Pydantic. Defining the `MessagePayload` schema upfront saved me a lot of time debugging payload errors from the frontend.

### Why a Classification Model?
I considered using a large generative model, but for this specific task, it felt like overkill.
- **Efficiency**: A dedicated classifier (like DistilBERT) is lightweight and fast. I don't need the model to write a poem; I just need it to tell me "Safe" or "Toxic".
- **Predictability**: Classification models give me a clear confidence score. With an LLM, the output can sometimes be unpredictable or hallucinated.

### Docker & Deployment
I've learned the hard way that environment issues can be a nightmare (I've dealt with enough `npm` timeouts and disk space issues on my local machine to know better). Containerizing this app with **Docker** was a priority. It validates that if it runs on my machine, it will run on Hugging Face Spaces without dependency conflicts.

---

## Prompt Engineering

*Note: As this microservice utilizes a specialized **Supervised Learning Model** (BERT-based Classifier) rather than a Generative Large Language Model (LLM), traditional "Prompt Engineering" in the sense of crafting system instructions does not apply.*

However, the "engineering" focus here lies in **Input Processing and Model Selection**:

1. **Input "Prompt"**: The "prompt" to the system is simply the raw user message: `payload.text`.
2. **No Instruction Needed**: Unlike an LLM where I might ask "Please classify this text as toxic...", the `AutoModelForSequenceClassification` is architecturally designed to output a probability distribution over specific labels (`TOXIC`, `SAFE`) without needing natural language instructions.
3. **Threshold Engineering**: Instead of tuning prompts, I tune the **Confidence Threshold**. I set a strict requirement (e.g., `confidence > 0.9` or similar logic in `app/main.py`) to determine when an action (blocking) should be taken.

---

## Lessons Learned & Limitations

While the system is working well, there were definitely some trade-offs I had to make:

1. **Context Blindness**: The model looks at messages one by one. If someone is being harassed over a series of messages that look "safe" individually, the system might miss it. To fix this, I'd probably need a more complex system that tracks conversation history.
2. **Sarcasm is Hard**: This is a classic NLP problem. If someone says "Wow, genius move" sarcastically, the model sees "genius" and marks it safe.
3. **The "Algospeak" Cat-and-Mouse Game**: Users are smart; they'll use numbers for letters or weird spellings to bypass filters. My model catches some of this, but it's not perfect.
4. **False Positives**: Sometimes passionate debates can get flagged. I had to tune the confidence threshold carefully to find a balance between safety and allowing free speech.

## Getting Started

You can run the API locally using standard Python tools or via Docker.

### Option A: Local Python (Recommended for Dev)
This method isolates dependencies in a virtual environment (`.venv`), keeping your system clean—just like a production server, but on your local machine.

1. **Create & Activate Virtual Environment**
   ```bash
   # Create a virtual environment
   python3 -m venv .venv
   
   # Activate it (Mac/Linux)
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Test**
   ```bash
   curl -X POST http://localhost:8000/api/check-message \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this!"}'
   ```

### Option B: Docker (Containerized)
If you prefer not to install Python dependencies locally.

1. **Build the Image**
   ```bash
   docker build -t nlp-backend .
   ```

2. **Run the Container**
   ```bash
   docker run -p 7860:7860 nlp-backend
   ```
   *Note: The Dockerfile uses port 7860 by default.*
