import streamlit as st
import pandas as pd

from utils.file_utils import load_boq
from engine.boq_parser import auto_map_columns, standardize_boq
from engine.library_loader import load_libraries
from engine.pipeline import build_spec_register
from engine.exporters import to_csv_bytes, to_docx_bytes
from utils.file_utils import to_excel_bytes
from utils.config import SOURCE_PRIORITY_DEFAULT

st.set_page_config(page_title="TechSpec PRO V2", layout="wide")

if "libraries" not in st.session_state:
    st.session_state["libraries"] = load_libraries()

st.title("🏗️ TechSpec PRO V2")
st.caption("DPWH-first, office-special-provisions-second, and UFGS-fallback BOQ-to-technical-specification generator")

with st.sidebar:
    st.header("Project Settings")
    agency_name = st.text_input("Agency / Office", value=st.session_state.get("agency_name", "Technological University of the Philippines"))
    project_name = st.text_input("Project Name", value=st.session_state.get("project_name", "Sample Project"))
    append_office_clauses = st.checkbox("Append office special provisions when relevant", value=st.session_state.get("append_office_clauses", True))
    source_priority = st.multiselect(
        "Source priority",
        options=["DPWH", "OFFICE", "UFGS", "GENERIC"],
        default=st.session_state.get("source_priority", SOURCE_PRIORITY_DEFAULT),
    )
    st.session_state["agency_name"] = agency_name
    st.session_state["project_name"] = project_name
    st.session_state["append_office_clauses"] = append_office_clauses
    st.session_state["source_priority"] = source_priority or SOURCE_PRIORITY_DEFAULT
    st.markdown("---")
    st.info("Use the pages in the sidebar for standards review, BOQ upload, generation, QA, and export.")

uploaded = st.file_uploader("Upload BOQ file", type=["csv", "xlsx", "xls"])

if uploaded:
    raw_df = load_boq(uploaded)
    st.session_state["raw_df"] = raw_df
    st.subheader("Raw BOQ Preview")
    st.dataframe(raw_df, use_container_width=True)

    auto_map = auto_map_columns(raw_df)
    cols = [""] + list(raw_df.columns)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        item_col = st.selectbox("Item No", cols, index=cols.index(auto_map.get("item_no", "")) if auto_map.get("item_no", "") in cols else 0)
    with c2:
        desc_col = st.selectbox("Description", cols, index=cols.index(auto_map.get("description", "")) if auto_map.get("description", "") in cols else 0)
    with c3:
        unit_col = st.selectbox("Unit", cols, index=cols.index(auto_map.get("unit", "")) if auto_map.get("unit", "") in cols else 0)
    with c4:
        qty_col = st.selectbox("Quantity", cols, index=cols.index(auto_map.get("quantity", "")) if auto_map.get("quantity", "") in cols else 0)
    with c5:
        remarks_col = st.selectbox("Remarks", cols, index=cols.index(auto_map.get("remarks", "")) if auto_map.get("remarks", "") in cols else 0)
    with c6:
        division_col = st.selectbox("Division/Trade", cols, index=cols.index(auto_map.get("division", "")) if auto_map.get("division", "") in cols else 0)

    if desc_col:
        mapping = {
            "item_no": item_col,
            "description": desc_col,
            "unit": unit_col,
            "quantity": qty_col,
            "remarks": remarks_col,
            "division": division_col,
        }
        boq_df = standardize_boq(raw_df, mapping)
        st.session_state["boq_df"] = boq_df
        st.subheader("Standardized BOQ")
        st.dataframe(boq_df, use_container_width=True)

        if st.button("Generate spec register", type="primary"):
            project_meta = {"agency_name": agency_name, "project_name": project_name}
            register_df = build_spec_register(
                boq_df=boq_df,
                libraries=st.session_state["libraries"],
                project_meta=project_meta,
                source_priority=st.session_state["source_priority"],
                append_office_clauses=append_office_clauses,
            )
            st.session_state["register_df"] = register_df

    if "register_df" in st.session_state:
        register_df = st.session_state["register_df"]
        st.subheader("Generated Spec Register")
        st.dataframe(
            register_df[[
                "row_id", "item_no", "description", "trade", "primary_source", "secondary_source",
                "confidence", "matched_section_title", "review_flags"
            ]],
            use_container_width=True,
        )

        export_rows = register_df.to_dict("records")
        st.download_button("Download register CSV", data=to_csv_bytes(register_df), file_name="techspec_register_v2.csv", mime="text/csv")
        st.download_button(
            "Download register XLSX",
            data=to_excel_bytes({"spec_register": register_df}),
            file_name="techspec_register_v2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.download_button(
            "Download all specs DOCX",
            data=to_docx_bytes(project_name, agency_name, export_rows),
            file_name="generated_technical_specs_v2.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
else:
    st.info("Upload a BOQ to begin.")
