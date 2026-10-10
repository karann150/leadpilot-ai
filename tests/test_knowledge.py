
from app.knowledge import search_faq


def test_product_description():
    answer = search_faq(
        "What does LeadPilot AI do?"
    )

    assert "AI-powered voice agent" in answer


def test_pricing():
    answer = search_faq(
        "What is the pricing?"
    )

    assert "not yet been finalized" in answer


def test_product_question_with_different_wording():
    answer = search_faq("Explain your product")
    assert "AI-powered voice agent" in answer


def test_business_benefit_question():
    answer = search_faq("How can this help my business?")
    assert "AI-powered voice agent" in answer


from app.semantic_search import SemanticSearch


def test_semantic_search_returns_results():
    engine = SemanticSearch()
    results = engine.search(
        "How can this software help a company?",
        top_k=3
    )

    assert len(results) > 0

    # The expected information should appear in the retrieved entries,
    # even if it is not ranked first.
    answers = [result["answer"] for result in results]

    assert any(
        "AI-powered voice agent" in answer
        for answer in answers
    )



def test_semantic_search_returns_pricing():
    engine = SemanticSearch()
    results = engine.search("How much does the product cost?")

    assert len(results) > 0
    assert "pricing has not yet been finalized" in results[0]["answer"].lower()
    
def test_unsupported_question_returns_fallback():
    from app.llm import FALLBACK_ANSWER

    answer = FALLBACK_ANSWER

    assert answer == (
        "I don't have verified information to answer that question. "
        "I can arrange a human follow-up to confirm it."
    )

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ask_endpoint_rejects_unsupported_email_followups():
    response = client.post(
        "/ask",
        json={
            "query": (
                "Does LeadPilot AI support automatic "
                "email follow-ups?"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "I don't have verified information to answer "
        "that question. I can arrange a human follow-up "
        "to confirm it."
    )
    assert data["sources"] == []

def test_unsupported_crm_integration_returns_fallback():
    response = client.post(
        "/ask",
        json={
            "query": "Does LeadPilot AI integrate with Salesforce?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "I don't have verified information about that integration. "
        "I can arrange a human follow-up to confirm it."
    )
    assert data["sources"] == []

def test_unsupported_calendar_integration_returns_fallback():
    response = client.post(
        "/ask",
        json={
            "query": "Can LeadPilot AI connect to Google Calendar?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "I don't have verified information about that integration. "
        "I can arrange a human follow-up to confirm it."
    )
    assert data["sources"] == []

