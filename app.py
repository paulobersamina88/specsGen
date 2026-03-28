import streamlit as st
import pandas as pd

from utils.file_utils import load_boq
from engine.boq_parser import auto_map_columns, standardize_boq
from engine.library_loader import load_libraries
from engine.classifier import classify_trade
from engine.matcher import match_item, match_library
from engine.clause_builder import generic_record, merge_clauses
from engine.generator import render_spec_text
from engine.qa_checker import review_flags
from engine.exporters import to_csv_bytes, to_docx_bytes

st.set_page_config(page_title="TechSpec PRO", layout="wide")

st.title("🏗️ TechSpec PRO")
st.caption("DPWH-first and UFGS-fallback BOQ to technical specification generator")

libraries = load_libraries()

with st.sidebar:
    st.header("Project Settings")
    agency_name = st.text_input("Agency / Office", value="Technological University of the Philippines")
    project_name = st.text_input("Project Name", value="Sample Project")
    st.markdown("---")
    st.write("This starter package is designed for internal drafting and review.")

uploaded = st.file_uploader("Upload BOQ file", type=["csv", "xlsx", "xls"])

if uploaded:
    raw_df = load_boq(uploaded)
    st.subheader("1) Raw BOQ")
    st.dataframe(raw_df, use_container_width=True)

    auto_map = auto_map_columns(raw_df)
    st.subheader("2) Column Mapping")
    cols = [""] + list(raw_df.columns)
    c1, c2, c3, c4, c5 = st.columns(5)
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

    if desc_col:
        mapping = {
            "item_no": item_col,
            "description": desc_col,
            "unit": unit_col,
            "quantity": qty_col,
            "remarks": remarks_col,
        }
        boq_df = standardize_boq(raw_df, mapping)
        generated = []
        for _, row in boq_df.iterrows():
            trade, trade_score = classify_trade(str(row["description"]), libraries["synonyms"])
            match = match_item(str(row["description"]), trade, libraries)
            primary_record = match["record"] or generic_record(trade)
            secondary_record = None
            if match["secondary_source"] == "UFGS":
                secondary_record = match_library(str(row["description"]), libraries["ufgs"])
            elif match["secondary_source"] == "OFFICE":
                secondary_record = match_library(str(row["description"]), libraries["office"])

            spec = merge_clauses(primary_record, secondary_record)
            flags = review_flags(match["primary_source"], match["confidence"], spec["clauses"] if False else primary_record.get("clauses") and primary_record)
            text = render_spec_text(row.to_dict(), spec, match["primary_source"], match["secondary_source"])
            generated.append({
                **row.to_dict(),
                "trade": trade,
                "trade_score": trade_score,
                "primary_source": match["primary_source"],
                "secondary_source": match["secondary_source"],
                "confidence": match["confidence"],
                "fallback_used": match["fallback_used"],
                "section_title": spec["title"],
                "review_flags": " | ".join(flags),
                "generated_spec": text,
            })

        result_df = pd.DataFrame(generated)

        st.subheader("3) Match Summary")
        st.dataframe(result_df[[
            "item_no", "description", "trade", "primary_source", "secondary_source", "confidence", "section_title", "review_flags"
        ]], use_container_width=True)

        st.subheader("4) Review Draft Spec")
        idx = st.selectbox(
            "Select item",
            result_df.index.tolist(),
            format_func=lambda i: f"{result_df.loc[i, 'item_no']} - {result_df.loc[i, 'description']}"
        )
        edited = st.text_area("Editable Specification", value=result_df.loc[idx, "generated_spec"], height=520)
        result_df.loc[idx, "generated_spec"] = edited

        st.subheader("5) Export")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "Download selected TXT",
                data=edited.encode("utf-8"),
                file_name="selected_spec.txt",
                mime="text/plain",
            )
        with c2:
            st.download_button(
                "Download register CSV",
                data=to_csv_bytes(result_df.drop(columns=["generated_spec"])),
                file_name="spec_register.csv",
                mime="text/csv",
            )
        with c3:
            st.download_button(
                "Download compiled DOCX",
                data=to_docx_bytes(result_df, project_name, agency_name),
                file_name="compiled_technical_specifications.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    else:
        st.info("Please map the description column.")
else:
    st.info("Upload a BOQ file to begin.")
