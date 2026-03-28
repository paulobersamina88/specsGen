from typing import Dict, List


def review_flags(primary_source: str, confidence: str, spec_record: Dict | None) -> List[str]:
    flags = []
    if primary_source == "UFGS":
        flags.append("UFGS fallback used. Review for Philippine applicability.")
    if primary_source == "GENERIC":
        flags.append("No reliable library match. Manual drafting required.")
    if confidence == "Low":
        flags.append("Low confidence match.")
    if spec_record:
        clauses = spec_record.get("clauses", {})
        for key in ["scope", "materials", "execution", "testing", "measurement", "payment"]:
            if not clauses.get(key):
                flags.append(f"Missing clause: {key}")
    return flags
