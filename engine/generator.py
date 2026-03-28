from typing import Dict

def render_spec_text(project_meta: Dict, row: Dict, spec: Dict, primary_source: str, secondary_source: str = "", flags: list[str] | None = None) -> str:
    flags = flags or []
    clauses = spec.get("clauses", {})
    lines = []
    lines.append("TECHNICAL SPECIFICATION")
    lines.append(f"Project: {project_meta.get('project_name', '')}")
    lines.append(f"Agency / Office: {project_meta.get('agency_name', '')}")
    lines.append(f"BOQ Row ID: {row.get('row_id', '')}")
    lines.append(f"BOQ Item No.: {row.get('item_no', '')}")
    lines.append(f"BOQ Description: {row.get('description', '')}")
    if row.get("unit"):
        lines.append(f"Unit: {row.get('unit')}")
    if row.get("quantity"):
        lines.append(f"Quantity: {row.get('quantity')}")
    if row.get("remarks"):
        lines.append(f"Remarks: {row.get('remarks')}")
    lines.append(f"Trade: {spec.get('trade', '')}")
    lines.append(f"Section Title: {spec.get('title', '')}")
    lines.append(f"Primary Source Logic: {primary_source}")
    if secondary_source:
        lines.append(f"Secondary Enrichment Source: {secondary_source}")
    lines.append(f"Reference Basis: {spec.get('reference', '')}")
    lines.append("")
    lines.append("1. SCOPE")
    lines.append(clauses.get("scope", ""))
    lines.append("")
    lines.append("2. REFERENCES")
    for i, item in enumerate(clauses.get("references", []), 1):
        lines.append(f"2.{i} {item}")
    lines.append("")
    lines.append("3. SUBMITTALS")
    for i, item in enumerate(clauses.get("submittals", []), 1):
        lines.append(f"3.{i} {item}")
    lines.append("")
    lines.append("4. MATERIAL REQUIREMENTS")
    for i, item in enumerate(clauses.get("materials", []), 1):
        lines.append(f"4.{i} {item}")
    lines.append("")
    lines.append("5. EXECUTION REQUIREMENTS")
    for i, item in enumerate(clauses.get("execution", []), 1):
        lines.append(f"5.{i} {item}")
    lines.append("")
    lines.append("6. QUALITY CONTROL / TESTING")
    for i, item in enumerate(clauses.get("testing", []), 1):
        lines.append(f"6.{i} {item}")
    lines.append("")
    lines.append("7. METHOD OF MEASUREMENT")
    lines.append(clauses.get("measurement", ""))
    lines.append("")
    lines.append("8. BASIS OF PAYMENT")
    lines.append(clauses.get("payment", ""))
    if clauses.get("special_notes"):
        lines.append("")
        lines.append("9. SPECIAL NOTES")
        for i, item in enumerate(clauses.get("special_notes", []), 1):
            lines.append(f"9.{i} {item}")
    if flags:
        lines.append("")
        lines.append("10. REVIEW FLAGS")
        for i, item in enumerate(flags, 1):
            lines.append(f"10.{i} {item}")
    lines.append("")
    lines.append("11. FINAL REVIEW NOTE")
    lines.append("This draft shall be checked against the latest approved plans, special provisions, applicable DPWH references, and discipline-specific Philippine codes before final issuance.")
    return "\n".join(lines)
