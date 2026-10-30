from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent_core import KnowledgeOpsAgent
from .document_indexer import DocumentIndexer
from .ingestion import IngestionService
from .vector_store import LocalVectorStore
from .guardrails import validate_query


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class QueryResponse(BaseModel):
    answer: str
    plan: list[str]
    grounding: dict
    evaluation: dict


indexer = DocumentIndexer()
indexer.ensure_demo_documents()

ingestion = IngestionService("data/sample_documents")
chunks = ingestion.load_documents()
vector_store = LocalVectorStore()
vector_store.index_documents(chunks)
agent = KnowledgeOpsAgent(vector_store)

app = FastAPI(title="Enterprise Knowledge Ops Agent")


@app.get("/health")
def health():
    return {"status": "ok", "documents_loaded": len(chunks)}


@app.post("/ask", response_model=QueryResponse)
def ask(question: QueryRequest):
    validation = validate_query(question.question)
    if not validation["valid"]:
        return QueryResponse(
            answer=validation["error"],
            plan=[],
            grounding={"grounding_score": 0.0, "is_grounded": False},
            evaluation={"failure_flags": ["invalid_query"]},
        )
    result = agent.orchestrate(question.question, session_id="api-session")
    return QueryResponse(
        answer=result["answer"],
        plan=result["plan"],
        grounding=result["grounding"],
        evaluation=result["evaluation"],
    )
