import io
import pandas as pd
from docx import Document


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def to_docx_bytes(df: pd.DataFrame, project_name: str, agency_name: str) -> bytes:
    doc = Document()
    doc.add_heading("Compiled Technical Specifications", level=1)
    doc.add_paragraph(f"Project: {project_name}")
    doc.add_paragraph(f"Agency/Office: {agency_name}")
    doc.add_paragraph("Generated draft for internal review.")
    for _, row in df.iterrows():
        doc.add_page_break()
        doc.add_heading(f"{row.get('item_no', '')} - {row.get('description', '')}", level=2)
        for line in str(row.get("generated_spec", "")).split("\n"):
            doc.add_paragraph(line)
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()
