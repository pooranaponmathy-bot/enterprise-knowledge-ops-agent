from __future__ import annotations

import re
from pathlib import Path
from typing import List

from .config import SAMPLE_DOCS_DIR
from .models import DocumentChunk


class IngestionService:
    def __init__(self, source_dir: str = SAMPLE_DOCS_DIR):
        self.source_dir = Path(source_dir)

    def load_documents(self) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        if not self.source_dir.exists():
            return chunks

        for file_path in sorted(self.source_dir.glob("*.txt")):
            text = file_path.read_text(encoding="utf-8")
            for i, chunk in enumerate(self.chunk_text(text, chunk_size=400, overlap=90), start=1):
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{file_path.stem}-{i}",
                        source=file_path.name,
                        content=chunk.strip(),
                        metadata={"path": str(file_path)},
                    )
                )
        return chunks

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 400, overlap: int = 90) -> List[str]:
        text = re.sub(r"\s+", " ", text).strip()
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: List[str] = []
        buffer = ""
        for sentence in sentences:
            if len(buffer) + len(sentence) <= chunk_size:
                buffer = (buffer + " " + sentence).strip()
            else:
                if buffer:
                    chunks.append(buffer)
                buffer = sentence
                if len(buffer) > chunk_size:
                    words = buffer.split()
                    for i in range(0, len(words), chunk_size):
                        segment = " ".join(words[i:i + chunk_size])
                        if segment:
                            chunks.append(segment)
                    buffer = ""
        if buffer:
            chunks.append(buffer)

        if overlap > 0 and len(chunks) > 1:
            merged: List[str] = []
            for idx, chunk in enumerate(chunks):
                if idx == 0:
                    merged.append(chunk)
                    continue
                previous = merged[-1]
                overlap_text = " ".join(previous.split()[-overlap//4:])
                merged.append((overlap_text + " " + chunk).strip())
            return merged
        return chunks
