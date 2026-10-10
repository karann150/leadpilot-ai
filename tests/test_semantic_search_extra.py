
from app.semantic_search import SemanticSearch


def test_empty_question_returns_no_results():
    search = SemanticSearch.__new__(SemanticSearch)
    search.documents = []
    search.index = None

    results = search.search("   ")

    assert results == []
