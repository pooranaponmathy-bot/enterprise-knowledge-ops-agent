graph TD
    User[Business User] --> API[FastAPI / CLI]
    API --> O[Orchestrator Agent]
    O --> P[Planner Agent]
    O --> R[Retriever Agent]
    R --> V[Local Vector Store]
    V --> D[Sample Enterprise Documents]
    O --> S[Reasoner Agent]
    S --> G[Validator Agent]
    G --> M[Memory Agent]
    G --> User

    P -->|decompose query| R
    R -->|grounded evidence| S
    S -->|draft answer| G
    G -->|confidence + trace| M
    M -->|session memory| User
