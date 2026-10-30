from dataclasses import dataclass, field
from typing import Any, Dict, List

DATA_DIR = "data"
SAMPLE_DOCS_DIR = "data/sample_documents"
ARTIFACTS_DIR = "artifacts"
TRACE_FILE = "artifacts/agent_trace.jsonl"
EVALUATION_FILE = "artifacts/evaluation_summary.json"
CONFIDENCE_THRESHOLD = 0.55
MAX_QUERY_LENGTH = 1000


@dataclass
class DocumentChunk:
    chunk_id: str
    source: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalResult:
    chunk_id: str
    source: str
    content: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentTrace:
    agent_name: str
    step: str
    details: Dict[str, Any]
