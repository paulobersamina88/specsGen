from typing import Dict, List
from utils.config import REQUIRED_CLAUSE_KEYS

def review_flags(primary_source: str, confidence: str, spec_record: Dict | None, description: str = "") -> List[str]:
    flags = []
    if primary_source == "UFGS":
        flags.append("UFGS fallback used. Review for Philippine applicability, submittal language, and procurement compatibility.")
    if primary_source == "GENERIC":
        flags.append("No reliable library match. Manual drafting or additional library entry required.")
    if confidence == "Low":
        flags.append("Low confidence match. Check BOQ wording and section assignment.")
    if len(str(description).split()) <= 2:
        flags.append("BOQ description appears too short or vague.")
    if spec_record:
        clauses = spec_record.get("clauses", {})
        for key in REQUIRED_CLAUSE_KEYS:
            value = clauses.get(key)
            if value is None or value == "" or value == []:
                flags.append(f"Missing clause: {key}")
    return flags
