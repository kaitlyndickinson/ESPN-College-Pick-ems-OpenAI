import streamlit as st
import json
from db_manager import get_all_datasets

st.set_page_config(page_title="Saved Predictions", layout="wide", page_icon="📚")

st.title("Saved Predictions")
st.markdown("Browse previously saved LLM predictions.")

datasets = get_all_datasets()

if not datasets:
    st.warning("No datasets found. Please generate predictions first.")
else:
    options = {f"{name}": json.loads(results) for id_, name, results in datasets}
    selected_label = st.sidebar.selectbox("Select a Dataset", list(options.keys()))

    selected_dataset = options[selected_label]

    st.subheader(f"Dataset: {selected_label}")
    for matchup, prediction in selected_dataset.items():
        st.markdown(f"#### {matchup}")
        with st.container():
            st.markdown(f"<div style='white-space: pre-wrap'>{prediction}</div>", unsafe_allow_html=True)
