from copy import deepcopy
from typing import Dict, List
from utils.text_utils import dedupe_keep_order

EMPTY_CLAUSES = {
    "scope": "",
    "references": [],
    "submittals": [],
    "materials": [],
    "execution": [],
    "testing": [],
    "measurement": "",
    "payment": "",
    "special_notes": [],
}

def generic_record(trade: str) -> Dict:
    record = {
        "id": "generic",
        "source": "GENERIC",
        "trade": trade or "Unclassified",
        "title": f"{trade or 'General'} Works",
        "reference": "Project drawings, approved scope of work, and applicable Philippine codes.",
        "clauses": deepcopy(EMPTY_CLAUSES),
    }
    record["clauses"]["scope"] = "Provide all labor, materials, equipment, tools, supervision, and incidentals necessary to complete the work indicated in the BOQ and approved plans."
    record["clauses"]["references"] = [
        "Approved plans and details",
        "Applicable Philippine codes and standards",
        "Contract drawings, BOQ, and special provisions",
    ]
    record["clauses"]["submittals"] = [
        "Product data and catalogue",
        "Shop drawings when required",
        "Method statement and work schedule when required",
    ]
    record["clauses"]["materials"] = ["Materials shall be new, approved, and suitable for the intended use."]
    record["clauses"]["execution"] = ["Install or construct the work true to line, level, plumb, and in accordance with approved plans and manufacturer recommendations."]
    record["clauses"]["testing"] = ["Perform inspection and testing as applicable to the nature of the work."]
    record["clauses"]["measurement"] = "Measure the completed and accepted work based on the BOQ pay item and approved actual quantities where applicable."
    record["clauses"]["payment"] = "Payment shall be at the contract unit price or lump sum price for the pay item, including labor, materials, tools, equipment, tests, and incidentals."
    return record

def merge_records(primary: Dict, secondary: Dict | None = None, office_record: Dict | None = None) -> Dict:
    result = deepcopy(primary)
    clauses = result.setdefault("clauses", deepcopy(EMPTY_CLAUSES))
    if secondary:
        for key in ["references", "submittals", "materials", "execution", "testing", "special_notes"]:
            clauses[key] = dedupe_keep_order(clauses.get(key, []) + secondary.get("clauses", {}).get(key, []))
        for key in ["scope", "measurement", "payment"]:
            if not clauses.get(key) and secondary.get("clauses", {}).get(key):
                clauses[key] = secondary["clauses"][key]
    if office_record:
        office_clauses = office_record.get("clauses", {})
        for key in ["references", "submittals", "materials", "execution", "testing", "special_notes"]:
            clauses[key] = dedupe_keep_order(clauses.get(key, []) + office_clauses.get(key, []))
        if office_clauses.get("scope"):
            clauses["scope"] = office_clauses["scope"] if not clauses.get("scope") else clauses["scope"] + " " + office_clauses["scope"]
        if office_clauses.get("measurement"):
            clauses["measurement"] = clauses.get("measurement") or office_clauses["measurement"]
        if office_clauses.get("payment"):
            clauses["payment"] = clauses.get("payment") or office_clauses["payment"]
    return result
