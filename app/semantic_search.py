
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge_base"
    / "faq.txt"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.documents = []
        self.index = None

    def load_documents(self):
        if not KNOWLEDGE_FILE.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {KNOWLEDGE_FILE}"
            )

        lines = KNOWLEDGE_FILE.read_text(
            encoding="utf-8"
        ).splitlines()

        self.documents = []

        for line in lines:
            if ":" not in line or not line.strip():
                continue

            category, answer = line.split(":", 1)

            category = category.strip()
            answer = answer.strip()

            if category and answer:
                self.documents.append({
                    "category": category,
                    "answer": answer,
                    "text": f"{category}: {answer}",
                })

        if not self.documents:
            raise ValueError("No FAQ entries found.")

        texts = [
            document["text"]
            for document in self.documents
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        self.index = faiss.IndexFlatIP(
            embeddings.shape[1]
        )

        self.index.add(embeddings)

    def search(self, question: str, top_k: int = 1):
        # Check the question before loading the model or documents.
        question = question.strip()

        if not question:
            return []

        if top_k <= 0:
            return []

        if self.index is None:
            self.load_documents()

        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        k = min(top_k, len(self.documents))

        if k == 0:
            return []

        scores, indices = self.index.search(
            query_embedding,
            k,
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            document = self.documents[int(idx)]

            results.append({
                "category": document["category"],
                "answer": document["answer"],
                "score": float(score),
            })

        return results
