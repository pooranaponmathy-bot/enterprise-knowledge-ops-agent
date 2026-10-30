from __future__ import annotations

import sys

from .service import EnterpriseKnowledgeOpsService


def main():
    service = EnterpriseKnowledgeOpsService()
    print("Enterprise Knowledge Ops Agent")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("Ask a question: ")
        if question.strip().lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        result = service.ask(question)
        print("\nAnswer:")
        print(result["answer"])
        print("\nGrounding:")
        print(result["grounding"])
        print("\nEvaluation:")
        print(result["evaluation"])
        print("\n")


if __name__ == "__main__":
    main()
    sys.exit(0)
