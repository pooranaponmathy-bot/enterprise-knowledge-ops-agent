# Architecture and Agent Flow

The architecture diagram below is stored in the docs folder and can be opened directly in a browser or converted to PNG/JPG if needed.

- Source diagram: `docs/architecture-flow.svg`

```mermaid
flowchart TD
    U[Business User] --> API[FastAPI / CLI]
    API --> O[Orchestrator Agent]
    O --> P[Planner Agent]
    O --> R[Retriever Agent]
    R --> V[Local Vector Store]
    V --> D[Enterprise Documents]
    O --> S[Reasoner Agent]
    S --> G[Validator Agent]
    G --> M[Memory Agent]
    G --> A[Final Answer]
    P -->|decompose query| R
    R -->|grounded evidence| S
    S -->|draft answer| G
    G -->|confidence + trace| M
    M -->|session memory| A
```

The vector version is the source asset and is preferred for documentation because it scales cleanly while preserving clarity. It can also be exported to PNG/JPG using common tools such as browser print-to-PDF or image conversion utilities.
