from __future__ import annotations

from knowledge_ops_agent.ingestion import IngestionService
from knowledge_ops_agent.vector_store import LocalVectorStore


def test_vector_retrieval_works_for_policy_terms():
    chunks = IngestionService("data/sample_documents").load_documents()
    vector_store = LocalVectorStore()
    vector_store.index_documents(chunks)
    results = vector_store.search("major compliance incidents escalation policy", top_k=3)
    assert len(results) > 0
    assert results[0].score > 0
