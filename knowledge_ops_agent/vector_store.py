from __future__ import annotations

from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import DocumentChunk, RetrievalResult


class LocalVectorStore:
    def __init__(self):
        self.documents: List[DocumentChunk] = []
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = None

    def index_documents(self, chunks: List[DocumentChunk]) -> None:
        self.documents = chunks
        texts = [chunk.content for chunk in chunks]
        if not texts:
            self.matrix = None
            return
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        if not self.documents or self.matrix is None:
            return []

        q_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(q_vector, self.matrix).flatten()
        ranked_indexes = similarities.argsort()[::-1][:top_k]

        results: List[RetrievalResult] = []
        for idx in ranked_indexes:
            score = float(similarities[idx])
            if score <= 0:
                continue
            chunk = self.documents[int(idx)]
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    source=chunk.source,
                    content=chunk.content,
                    score=score,
                    metadata=chunk.metadata,
                )
            )
        return results
