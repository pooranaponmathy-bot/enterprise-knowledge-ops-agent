from __future__ import annotations

from knowledge_ops_agent.service import EnterpriseKnowledgeOpsService


def test_invalid_question_rejected():
    service = EnterpriseKnowledgeOpsService()
    result = service.ask("")
    assert result["answer"] == "Question cannot be empty."


def test_policy_query_returns_relevant_sources():
    service = EnterpriseKnowledgeOpsService()
    result = service.ask("What is the escalation policy for major compliance incidents?")
    assert "answer" in result
    assert result["evaluation"]["retrieval_count"] > 0
    assert "policy" in result["answer"].lower() or "escalation" in result["answer"].lower()


def test_grounding_is_reported():
    service = EnterpriseKnowledgeOpsService()
    result = service.ask("Which contract clause covers termination and data retention?")
    assert "grounding" in result
    assert "grounding_score" in result["grounding"]
