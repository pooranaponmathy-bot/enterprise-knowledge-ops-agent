from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .config import ARTIFACTS_DIR, EVALUATION_FILE, TRACE_FILE


class TraceLogger:
    def __init__(self, trace_path: str = TRACE_FILE):
        self.trace_path = Path(trace_path)
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, agent_name: str, step: str, details: Dict[str, Any]) -> None:
        entry = {
            "agent_name": agent_name,
            "step": step,
            "details": details,
        }
        with self.trace_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")

    def reset(self) -> None:
        if self.trace_path.exists():
            self.trace_path.unlink()


class EvaluationLogger:
    def __init__(self, path: str = EVALUATION_FILE):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, payload: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
