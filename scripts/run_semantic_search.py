
from app.semantic_search import SemanticSearch


search_engine = SemanticSearch()

questions = [
    "What does LeadPilot AI do?",
    "How can this software help a company?",
    "How much does the product cost?",
]

for question in questions:
    results = search_engine.search(
    "How can this software help a company?",
    top_k=3
)

for result in results:
    print(result)
