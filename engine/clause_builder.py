from typing import Dict, List


def generic_record(trade: str) -> Dict:
    return {
        "id": f"generic_{trade.lower().replace('/', '_')}",
        "title": f"{trade} Works",
        "trade": trade,
        "reference": "Project drawings, owner requirements, applicable Philippine codes, and approved special provisions.",
        "clauses": {
            "scope": f"This work covers all labor, materials, equipment, supervision, testing, and incidentals necessary to complete the required {trade.lower()} items indicated in the contract documents.",
            "materials": ["Provide materials that are new, approved, and suitable for the intended application."],
            "execution": ["Install the work in accordance with approved plans, manufacturer recommendations, and good engineering practice."],
            "testing": ["Perform inspections and tests required by the contract documents and applicable codes."],
            "measurement": "Measurement shall be based on the BOQ pay item or actual accepted quantity, as applicable.",
            "payment": "Payment shall be made at the applicable contract unit price or lump-sum pay item, including all labor, materials, equipment, testing, and incidentals.",
        },
    }


def merge_clauses(primary: Dict, secondary: Dict | None = None) -> Dict:
    base = primary["clauses"].copy()
    if secondary:
        for key in ["materials", "execution", "testing"]:
            if key in secondary.get("clauses", {}):
                merged = list(base.get(key, []))
                for item in secondary["clauses"][key]:
                    if item not in merged:
                        merged.append(item)
                base[key] = merged
    return {
        "title": primary.get("title", "Draft Specification"),
        "reference": primary.get("reference", ""),
        "clauses": base,
    }
