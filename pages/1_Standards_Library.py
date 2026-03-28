import streamlit as st
import pandas as pd
from engine.library_loader import load_libraries

st.title("Standards Library")
libraries = st.session_state.get("libraries") or load_libraries()

for source_key, title in [("dpwh", "DPWH Library"), ("office", "Office Special Provisions"), ("ufgs", "UFGS Fallback Library")]:
    st.subheader(title)
    df = pd.DataFrame(libraries[source_key])
    if not df.empty:
        view = df[["id", "title", "trade", "reference", "keywords"]].copy()
        view["keywords"] = view["keywords"].apply(lambda x: ", ".join(x))
        st.dataframe(view, use_container_width=True)
    else:
        st.info(f"No records in {title}.")
