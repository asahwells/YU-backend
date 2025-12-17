# YuChat NLP Backend

## 1. User Requirements Analysis

### 1.1 Project Introduction
YuChat is a mobile chat application built with React Native designed to provide seamless communication. To ensure a safe and positive user experience, the system incorporates an intelligent backend service ("Nlp backend") that filters harmful or toxic content in real-time.

### 1.2 Project Goal
The primary goal of this project is to implement a high-performance, low-latency API that automatically intercepts, analyzes, and moderates user generated content. By filtering out toxic messages before they reach the recipient, YuChat aims to maintain a healthy community environment.

---

## 2. Functional Analysis

The backend service supports the following core functions:

1.  **Message Moderation API**: A dedicated endpoint to receive text content from the YuChat client.
2.  **Toxicity Classification**: Utilizes a pre-trained NLP model (e.g., DistilBERT or Toxic Comment Model) to analyze the sentiment/toxicity of the input text.
3.  **Threshold-Based Filtering**: Automatically accepts or rejects messages based on a configurable confidence threshold (e.g., rejecting messages with >0.9 toxicity confidence).
4.  **Model Management**: Efficiently loads the heavy NLP model into memory upon application startup to ensure sub-150ms response times for subsequent requests.

---

## 3. Module Design

The architecture is built using **FastAPI** to ensure modularity and performance.

### 3.1 Architecture Overview
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

### 3.2 Directory Structure
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

## 4. Interface Analysis

### 4.1 Data Exchange
The system uses **JSON** over **HTTP** for all data exchange between the YuChat React Native client (APK) and the AWS Backend.

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

### 4.2 Deployment Infrastructure
The interface is hosted on a high-availability cloud environment to support the mobile client.

-   **Platform**: AWS EC2
-   **Instance Type**: `t3.medium` or `t3.large` (2–4 GB RAM) to handle ML model memory requirements.
-   **Storage**: EBS Volume modified to 20GB+ (from distinct 8GB default) to accommodate model weights and dependencies.
-   **Client**: YuChat React Native APK.

---

## Getting Started (Development)

1. **Install dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the API**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Test with Curl**
   ```bash
   curl -X POST http://localhost:8000/api/check-message \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this!"}'
   ```
