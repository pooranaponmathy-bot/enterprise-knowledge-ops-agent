# Enterprise Knowledge Ops Agent

A local, agentic AI system for enterprise knowledge retrieval, reasoning, validation, and explainability.

## Features
- Multi-agent orchestration for planning, retrieval, reasoning, validation, and memory
- Local document ingestion and indexing using a lightweight vector-style retrieval engine
- Grounded answer generation with source attribution
- Guardrails for invalid input, low-confidence answers, and unsafe queries
- Evaluation logging for retrieval relevance, grounding, and failure detection
- FastAPI API and CLI interface

## Project Structure
- `knowledge_ops_agent/` — application logic
- `data/sample_documents/` — enterprise sample documents
- `docs/` — architecture, guardrails, evaluation, and unit test documentation
- `tests/` — unit tests

## Quick Start

### 1. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the CLI
```bash
python -m knowledge_ops_agent.cli
```

### 4. Run the API server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Test the API
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the escalation policy for major compliance incidents?"}'
```

## Demo Questions
- What are the escalation steps for major compliance issues?
- Which contract clauses define termination and data retention?
- What should an employee do when a policy exception is requested?
- Which SOP steps are required before onboarding a vendor?

## Architecture
See: `docs/architecture.md`

## Evaluation and Guardrails
See: `docs/evaluation_and_guardrails.md`

## Unit Test Documentation
See: `docs/unit_test_cases.md`
