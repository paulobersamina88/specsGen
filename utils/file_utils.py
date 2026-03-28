import pandas as pd
import streamlit as st

def load_boq(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith(".xlsx") or name.endswith(".xls"):
        xls = pd.ExcelFile(uploaded_file)
        sheet = st.selectbox("Select BOQ sheet", xls.sheet_names, key="boq_sheet_select")
        return pd.read_excel(xls, sheet_name=sheet)
    raise ValueError("Unsupported file format. Please upload CSV, XLSX, or XLS.")

def to_excel_bytes(df_dict: dict[str, pd.DataFrame]) -> bytes:
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for sheet_name, df in df_dict.items():
            safe_sheet = sheet_name[:31] or "Sheet1"
            df.to_excel(writer, index=False, sheet_name=safe_sheet)
    return buffer.getvalue()
