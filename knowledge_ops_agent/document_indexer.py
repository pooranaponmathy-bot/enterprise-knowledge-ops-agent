from __future__ import annotations

from pathlib import Path


class DocumentIndexer:
    def __init__(self, source_dir: str = "data/sample_documents"):
        self.source_dir = Path(source_dir)

    def ensure_demo_documents(self) -> None:
        self.source_dir.mkdir(parents=True, exist_ok=True)
        default_files = {
            "policy_manual.txt": """Policy Manual\n\n1. Compliance Oversight\nAll employees must report material compliance incidents to the Legal and Compliance Office within 24 hours. Major incidents include regulatory violations, data breaches, or repeated policy non-compliance.\n\n2. Escalation Policy\nEscalation should move from team leads to Division Compliance, and then to General Counsel when the incident is high impact or threatens legal exposure.\n\n3. Exception Handling\nAny policy deviation must be approved through a written exception request and managed by Risk and Compliance.\n""",
            "sop_vendor_onboarding.txt": """Vendor Onboarding SOP\n\n1. Due diligence review\nThe vendor onboarding workflow includes screening, contract approval, and security review.\n\n2. Operational controls\nBefore onboarding, the responsible manager must confirm insurance, regulatory alignment, and approved terms.\n\n3. Approval authority\nA final approval is required by the Procurement Lead and the Compliance Officer before activation.\n""",
            "contract_terms.txt": """Master Services Agreement\n\nSection 8: Term and Termination\nThis Agreement may be terminated for material breach, non-payment, or repeated regulatory non-compliance. Termination requires written notice and a 30-day cure period, unless the breach is severe.\n\nSection 12: Data Retention\nCustomer data must be retained in accordance with the agreed retention schedule and internal legal holds.\n""",
            "audit_report.txt": """Internal Audit Summary\n\nThe latest audit found that training completion, policy sign-off, and escalation logs were generally compliant. Minor gaps were noted in document version control and approval traceability. Corrective actions must be monitored by the Audit and Risk Committee.\n""",
        }
        for filename, content in default_files.items():
            target = self.source_dir / filename
            if not target.exists():
                target.write_text(content, encoding="utf-8")
