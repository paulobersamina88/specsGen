import streamlit as st
import pandas as pd

st.title("QA Review")

register_df = st.session_state.get("register_df")
if register_df is None or register_df.empty:
    st.info("Generate the spec register first.")
else:
    flagged = register_df[register_df["review_flags"].astype(str).str.strip() != ""].copy()
    st.metric("Total BOQ items", len(register_df))
    st.metric("Flagged items", len(flagged))
    st.metric("UFGS fallback items", int((register_df["primary_source"] == "UFGS").sum()))
    st.metric("Generic items", int((register_df["primary_source"] == "GENERIC").sum()))
    if not flagged.empty:
        st.dataframe(flagged[["row_id", "item_no", "description", "primary_source", "confidence", "review_flags"]], use_container_width=True)
    else:
        st.success("No flagged items found.")
