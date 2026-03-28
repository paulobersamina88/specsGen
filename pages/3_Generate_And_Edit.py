import streamlit as st

st.title("Generate and Edit Specs")

register_df = st.session_state.get("register_df")
if register_df is None or register_df.empty:
    st.info("Generate the spec register from the main page first.")
else:
    options = register_df["row_id"].tolist()
    selected = st.selectbox("Select BOQ row", options=options, format_func=lambda rid: f"Row {rid} - {register_df.loc[register_df['row_id']==rid, 'description'].iloc[0]}")
    row = register_df.loc[register_df["row_id"] == selected].iloc[0]
    edited = st.text_area("Editable technical specification", value=row["generated_spec"], height=700)
    st.download_button("Download selected spec TXT", data=edited.encode("utf-8"), file_name=f"techspec_row_{selected}.txt", mime="text/plain")
