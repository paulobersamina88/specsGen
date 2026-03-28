import streamlit as st
from engine.exporters import to_csv_bytes, to_docx_bytes
from utils.file_utils import to_excel_bytes

st.title("Export Center")
register_df = st.session_state.get("register_df")
project_name = st.session_state.get("project_name", "Sample Project")
agency_name = st.session_state.get("agency_name", "Agency")

if register_df is None or register_df.empty:
    st.info("Generate the spec register first.")
else:
    rows = register_df.to_dict("records")
    st.download_button("Download CSV register", data=to_csv_bytes(register_df), file_name="techspec_register_v2.csv", mime="text/csv")
    st.download_button(
        "Download XLSX register",
        data=to_excel_bytes({"spec_register": register_df}),
        file_name="techspec_register_v2.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.download_button(
        "Download DOCX compiled specs",
        data=to_docx_bytes(project_name, agency_name, rows),
        file_name="generated_technical_specs_v2.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
