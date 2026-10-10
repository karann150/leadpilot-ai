# LeadPilot AI — RAG-Based AI Voice Agent

LeadPilot AI is a locally running AI voice agent designed to answer prospect questions using a knowledge base. It combines speech recognition, semantic retrieval, local LLM inference, and text-to-speech to demonstrate a foundation for AI-assisted lead qualification.

## Features

- **Voice input:** Converts speech to text using Faster-Whisper.
- **RAG pipeline:** Retrieves relevant knowledge-base information using Sentence Transformers and FAISS.
- **Local LLM:** Generates responses using Llama 3.2 3B through Ollama.
- **Text-to-speech:** Speaks responses using pyttsx3.
- **Guardrails:** Handles unsupported questions and unverified pricing or third-party integrations.
- **REST API:** Exposes endpoints through FastAPI.
- **Testing:** Includes automated tests for knowledge-base and semantic-search functionality.

## Tech Stack

Python · FastAPI · Ollama · Llama 3.2 · FAISS · Sentence Transformers · Faster-Whisper · pyttsx3 · pytest

## Architecture

1. The user asks a question through voice or the API.
2. Faster-Whisper transcribes voice input into text.
3. Sentence Transformers generates an embedding for the query.
4. FAISS retrieves relevant information from the knowledge base.
5. Ollama generates an answer using the retrieved context and configured guardrails.
6. The API returns the response, and the voice interface reads it aloud.

## Project Structure

```text
leadpilot-ai/
├── app/
│   ├── main.py
│   ├── knowledge.py
│   ├── semantic_search.py
│   ├── llm.py
│   ├── guardrails.py
│   └── voice.py
├── knowledge_base/
│   └── faq.txt
├── scripts/
├── tests/
├── requirements.txt
└── .gitignore
```

## Prerequisites

- Python
- Git
- Ollama
- The `llama3.2:3b` model

## Setup

Clone the repository:

```bash
git clone https://github.com/karann150/leadpilot-ai.git
cd leadpilot-ai
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Install and start Ollama, then pull the model:

```powershell
ollama pull llama3.2:3b
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

## Current Scope

This project currently demonstrates local voice interaction, knowledge-base question answering, semantic retrieval, and API-based access. Production phone calling, multi-business configuration, and persistent lead management are not yet implemented.

## Future Improvements

- Add business-specific knowledge bases.
- Implement lead qualification and structured lead storage.
- Improve retrieval evaluation and document chunking.
- Add integration tests and a documented voice demo.
- Explore telephony integration with consent and opt-out handling.

## Author

**Karan Shewale**

GitHub: https://github.com/karann150
