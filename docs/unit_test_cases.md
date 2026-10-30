## Unit Test Case Documentation

### Test Goals
The unit tests validate that the agent performs safely, retrieves relevant documents, and generates grounded responses.

### Core Test Cases
1. Query validation rejects empty input
2. Query validation rejects malicious instructions
3. Retrieval returns relevant results for policy-related questions
4. Low-confidence grounding returns a conservative response
5. Orchestration produces plan, evidence, and evaluation output

### Example Structure
- `tests/test_agent_service.py`
- `tests/test_guardrails.py`
- `tests/test_vector_retrieval.py`

### Expected Results
- No invalid query should pass the system
- Relevant source documents must appear in retrieval results
- Final response must include the evaluation context and grounding metadata
