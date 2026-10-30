from __future__ import annotations

import re

from .config import CONFIDENCE_THRESHOLD, MAX_QUERY_LENGTH


def validate_query(question: str) -> dict:
    if question is None or not str(question).strip():
        return {"valid": False, "error": "Question cannot be empty."}

    q = str(question).strip()
    if len(q) > MAX_QUERY_LENGTH:
        return {"valid": False, "error": "Question exceeds supported length."}

    suspicious_patterns = [
        r"ignore previous instructions",
        r"system prompt",
        r"developer prompt",
        r"act as",
        r"override",
    ]
    lowered = q.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, lowered):
            return {"valid": False, "error": "Question contains unsupported prompt injection patterns."}

    return {"valid": True, "normalized_question": q}


def grounding_score(answer: str, retrieved_results: list) -> float:
    if not retrieved_results:
        return 0.0

    evidence_text = " ".join([r.content.lower() for r in retrieved_results]).strip()
    if not answer:
        return 0.0

    answer_tokens = set(re.findall(r"[a-zA-Z0-9]+", answer.lower()))
    if not answer_tokens:
        return 0.0

    overlap = sum(1 for token in answer_tokens if token in evidence_text)
    base_score = overlap / max(len(answer_tokens), 1)
    top_score = max(r.score for r in retrieved_results)
    score = min(1.0, (base_score * 0.6) + (top_score * 0.4))
    return round(score, 3)


def validate_grounding(answer: str, retrieved_results: list) -> dict:
    score = grounding_score(answer, retrieved_results)
    allowed = score >= CONFIDENCE_THRESHOLD
    return {
        "grounding_score": score,
        "is_grounded": allowed,
        "threshold": CONFIDENCE_THRESHOLD,
        "message": "Answer is grounded in retrieved documents." if allowed else "Low grounding confidence: answer may be unsupported.",
    }
