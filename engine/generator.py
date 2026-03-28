from typing import Dict


def render_spec_text(row: Dict, spec: Dict, primary_source: str, secondary_source: str = "") -> str:
    lines = []
    lines.append("TECHNICAL SPECIFICATION")
    lines.append(f"BOQ Item No.: {row.get('item_no', '')}")
    lines.append(f"BOQ Description: {row.get('description', '')}")
    if row.get("unit"):
        lines.append(f"Unit: {row.get('unit')}")
    if row.get("quantity"):
        lines.append(f"Quantity: {row.get('quantity')}")
    lines.append(f"Section Title: {spec.get('title', '')}")
    lines.append(f"Primary Source Logic: {primary_source}")
    if secondary_source:
        lines.append(f"Secondary Enrichment Source: {secondary_source}")
    lines.append(f"Reference Basis: {spec.get('reference', '')}")
    lines.append("")
    lines.append("1. SCOPE")
    lines.append(spec["clauses"].get("scope", ""))
    lines.append("")
    lines.append("2. MATERIAL REQUIREMENTS")
    for i, item in enumerate(spec["clauses"].get("materials", []), 1):
        lines.append(f"2.{i} {item}")
    lines.append("")
    lines.append("3. EXECUTION REQUIREMENTS")
    for i, item in enumerate(spec["clauses"].get("execution", []), 1):
        lines.append(f"3.{i} {item}")
    lines.append("")
    lines.append("4. QUALITY CONTROL / TESTING")
    for i, item in enumerate(spec["clauses"].get("testing", []), 1):
        lines.append(f"4.{i} {item}")
    lines.append("")
    lines.append("5. METHOD OF MEASUREMENT")
    lines.append(spec["clauses"].get("measurement", ""))
    lines.append("")
    lines.append("6. BASIS OF PAYMENT")
    lines.append(spec["clauses"].get("payment", ""))
    lines.append("")
    lines.append("7. REVIEW NOTE")
    lines.append("This draft must be checked against the latest approved project drawings, special provisions, DPWH references, and applicable Philippine codes before final issuance.")
    return "\n".join(lines)
