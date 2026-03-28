import streamlit as st
import pandas as pd
from engine.classifier import classify_trade

st.title("BOQ Analyzer")

boq_df = st.session_state.get("boq_df")
libraries = st.session_state.get("libraries")

if boq_df is None or libraries is None:
    st.info("Upload and standardize a BOQ from the main page first.")
else:
    analysis_rows = []
    for _, row in boq_df.iterrows():
        trade, score = classify_trade(str(row["description"]), libraries["synonyms"])
        analysis_rows.append({
            "row_id": row["row_id"],
            "item_no": row["item_no"],
            "description": row["description"],
            "trade_guess": trade,
            "trade_score": score,
        })
    st.dataframe(pd.DataFrame(analysis_rows), use_container_width=True)
