from __future__ import annotations

from .agent_core import KnowledgeOpsAgent
from .document_indexer import DocumentIndexer
from .guardrails import validate_query
from .ingestion import IngestionService
from .vector_store import LocalVectorStore


class EnterpriseKnowledgeOpsService:
    def __init__(self):
        indexer = DocumentIndexer()
        indexer.ensure_demo_documents()
        chunks = IngestionService("data/sample_documents").load_documents()
        vector_store = LocalVectorStore()
        vector_store.index_documents(chunks)
        self.agent = KnowledgeOpsAgent(vector_store)

    def ask(self, question: str, session_id: str = "cli"):
        validation = validate_query(question)
        if not validation["valid"]:
            return {
                "answer": validation["error"],
                "plan": [],
                "grounding": {"grounding_score": 0.0, "is_grounded": False},
                "evaluation": {"failure_flags": ["invalid_query"]},
            }
        return self.agent.orchestrate(question, session_id=session_id)
