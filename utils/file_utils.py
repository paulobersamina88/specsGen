import pandas as pd


def load_boq(uploaded_file, sheet_name=None):
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith((".xlsx", ".xls")):
        if sheet_name is None:
            return pd.read_excel(uploaded_file)
        return pd.read_excel(uploaded_file, sheet_name=sheet_name)
    raise ValueError("Unsupported file format. Please upload CSV, XLSX, or XLS.")
