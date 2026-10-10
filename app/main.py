
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.semantic_search import SemanticSearch
from app.llm import generate_answer
from app.guardrails import (
    is_integration_question,
    INTEGRATION_FALLBACK,
    FALLBACK_ANSWER,
    PRICING_TERMS,
    is_capability_question,
    has_documented_capability,
)

app = FastAPI(title="LeadPilot AI")

search_engine = SemanticSearch()


class AskRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)


@app.get("/")
def home():
    return {"message": "Welcome to LeadPilot AI!"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "LeadPilot AI",
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    question = request.query.strip()
    question_lower = question.lower()

    # Reject empty or whitespace-only questions.
    if not question:
        return {
            "question": question,
            "answer": FALLBACK_ANSWER,
            "sources": [],
        }

    results = search_engine.search(question, top_k=3)

    print("\nQuestion:", question)
    print("Search results:", results)

    # Reject undocumented integrations.
    if is_integration_question(question):
        return {
            "question": question,
            "answer": INTEGRATION_FALLBACK,
            "sources": [],
        }

    # Return pricing information directly from the FAQ.
    if any(term in question_lower for term in PRICING_TERMS):
        if search_engine.index is None:
            search_engine.load_documents()

        pricing_result = next(
            (
                document
                for document in search_engine.documents
                if document["category"].lower() == "pricing"
            ),
            None,
        )

        if pricing_result:
            return {
                "question": question,
                "answer": pricing_result["answer"],
                "sources": [
                    f'{pricing_result["category"]}: '
                    f'{pricing_result["answer"]}'
                ],
            }

    # Reject unsupported capability questions.
    if (
        is_capability_question(question)
        and not has_documented_capability(question)
    ):
        return {
            "question": question,
            "answer": FALLBACK_ANSWER,
            "sources": [],
        }

    # Handle missing retrieval results.
    if not results:
        return {
            "question": question,
            "answer": (
                "I couldn't find a verified answer in the FAQ. "
                "I can arrange a human follow-up."
            ),
            "sources": [],
        }

    # Build context for the local LLM.
    context = "\n".join(
        f'{result["category"]}: {result["answer"]}'
        for result in results
    )

    answer = generate_answer(question, context)

    # Avoid presenting sources for fallback answers.
    if answer.strip() == FALLBACK_ANSWER:
        sources = []
    else:
        sources = [
            f'{result["category"]}: {result["answer"]}'
            for result in results
        ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }
