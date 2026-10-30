from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .config import ARTIFACTS_DIR, CONFIDENCE_THRESHOLD
from .logging import EvaluationLogger, TraceLogger
from .vector_store import validate_grounding


class PlannerAgent:
    def plan(self, question: str) -> List[str]:
        q = question.lower()
        plan = ["retrieve_documents", "reason_over_evidence", "validate_answer"]
        if "policy" in q or "compliance" in q:
            plan.insert(1, "policy_cross_check")
        if "contract" in q or "termination" in q or "retention" in q:
            plan.insert(1, "contract_clause_review")
        if "sop" in q or "procedure" in q or "vendor" in q:
            plan.insert(1, "operational_steps_review")
        return plan


class RetrieverAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, question: str, top_k: int = 5):
        return self.vector_store.search(question, top_k=top_k)


class ReasonerAgent:
    def reason(self, question: str, retrieved_results: List[Any]) -> str:
        if not retrieved_results:
            return "I could not find enough grounded documentation in the local knowledge base to answer this question confidently."

        context = "\n".join(
            f"Source: {item.source}\nEvidence: {item.content}"
            for item in retrieved_results[:3]
        )
        key_terms = [token for token in question.lower().split() if len(token) > 3][:4]
        summary = " ".join(key_terms) if key_terms else "relevant policy"
        answer = (
            f"Based on the local enterprise knowledge base, the most relevant material points to {summary}. "
            f"The supporting evidence includes:\n{context}\n\n"
            "The answer should be interpreted as a grounded summary of the retrieved documents, not a replacement for formal policy review."
        )
        return answer


class ValidatorAgent:
    def validate(self, answer: str, retrieved_results: List[Any]) -> Dict[str, Any]:
        return validate_grounding(answer, retrieved_results)


class MemoryAgent:
    def __init__(self, memory_path: str = "artifacts/session_memory.json"):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        if not self.memory_path.exists():
            return {"sessions": []}
        return json.loads(self.memory_path.read_text(encoding="utf-8"))

    def save(self, session: Dict[str, Any]) -> None:
        memory = self.load()
        memory.setdefault("sessions", [])
        memory["sessions"].append(session)
        self.memory_path.write_text(json.dumps(memory, indent=2), encoding="utf-8")


class KnowledgeOpsAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.planner = PlannerAgent()
        self.retriever = RetrieverAgent(vector_store)
        self.reasoner = ReasonerAgent()
        self.validator = ValidatorAgent()
        self.memory = MemoryAgent()
        self.trace_logger = TraceLogger()
        self.evaluation_logger = EvaluationLogger()

    def orchestrate(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        plan = self.planner.plan(question)
        self.trace_logger.log("orchestrator", "plan_created", {"plan": plan})

        retrieval_results = self.retriever.retrieve(question, top_k=5)
        self.trace_logger.log("retriever", "documents_retrieved", {"count": len(retrieval_results)})

        answer = self.reasoner.reason(question, retrieval_results)
        self.trace_logger.log("reasoner", "answer_generated", {"length": len(answer)})

        validation = self.validator.validate(answer, retrieval_results)
        confidence = float(validation["grounding_score"])
        failure_flags = []
        if len(retrieval_results) == 0:
            failure_flags.append("insufficient_retrieval")
        if confidence < CONFIDENCE_THRESHOLD:
            failure_flags.append("low_grounding_confidence")

        final_answer = answer
        if failure_flags:
            final_answer = (
                "I cannot answer this with sufficient confidence from the available local knowledge base. "
                "Please check the query or provide more source documents."
            )

        evaluation = {
            "query": question,
            "session_id": session_id,
            "retrieval_count": len(retrieval_results),
            "retrieval_scores": [round(item.score, 3) for item in retrieval_results],
            "grounding_score": confidence,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "failure_flags": failure_flags,
            "plan": plan,
            "sources": [
                {"source": item.source, "score": round(item.score, 3), "content": item.content[:220]}
                for item in retrieval_results
            ],
        }
        self.evaluation_logger.write(evaluation)

        self.memory.save({
            "session_id": session_id,
            "query": question,
            "answer": final_answer,
            "grounding_score": confidence,
            "failure_flags": failure_flags,
        })

        return {
            "answer": final_answer,
            "plan": plan,
            "retrieval_results": [
                {"source": item.source, "score": round(item.score, 3), "content": item.content}
                for item in retrieval_results
            ],
            "grounding": validation,
            "evaluation": evaluation,
            "traces": [
                {"agent_name": "orchestrator", "step": "plan_created", "details": {"plan": plan}},
                {"agent_name": "retriever", "step": "documents_retrieved", "details": {"count": len(retrieval_results)}},
                {"agent_name": "reasoner", "step": "answer_generated", "details": {"preview": answer[:200]}},
                {"agent_name": "validator", "step": "grounding_checked", "details": validation},
            ],
        }
