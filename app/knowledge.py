
from pathlib import Path

KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge_base"
    / "faq.txt"
)


def search_faq(question: str) -> str:
    if not KNOWLEDGE_FILE.exists():
        return "Knowledge base file not found."

    question = question.lower().strip()

    if not question:
        return "Please enter a question."

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    # Check specific question types before general keywords.
    categories = {
        "pricing": [
            "price", "pricing", "cost", "expensive", "discount"
        ],
        "features": [
            "feature", "features", "capability", "capabilities"
        ],
        "support": [
            "support", "human", "representative", "person"
        ],
        "description": [
            "product", "leadpilot", "what do you do", "explain",
            "help my business", "solve", "what problem"
        ],
        "target customers": [
            "customer", "customers", "target", "target audience"
        ],
    }

    selected_category = None

    for category, keywords in categories.items():
        if any(keyword in question for keyword in keywords):
            selected_category = category
            break

    if selected_category is None:
        return "I couldn't find a relevant answer in the FAQ."

    prefix = f"{selected_category}:"

    for line in text.splitlines():
        if line.lower().startswith(prefix):
            return line.split(":", 1)[1].strip()

    return "I couldn't find a relevant answer in the FAQ."
