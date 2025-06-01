# Force rebuild

import streamlit as st
import pandas as pd

st.set_page_config(page_title="USV Survey Results", layout="wide")

st.title("🚤 MSc Survey: USVs in Survey Operations")
st.markdown("This dashboard displays results from the LinkedIn survey on Uncrewed Surface Vessels (USVs).")

# --- Load data ---
@st.cache_data
def load_data():
    return pd.read_excel("usv_survey_data.xlsx")

df = load_data()

# --- Show raw table ---
st.subheader("📋 Full Survey Responses")
st.dataframe(df, use_container_width=True)

# --- Column selector ---
columns = df.columns.tolist()
selected = st.multiselect("Select questions to explore:", columns, default=columns)

# --- Filtered View ---
st.subheader("🔍 Filtered Responses")
st.dataframe(df[selected], use_container_width=True)

# --- Optional basic summary ---
st.subheader("📊 Response Count per Question (if applicable)")

for col in selected:
    if df[col].dtype == "object" and df[col].nunique() < 25:
        st.markdown(f"**{col}**")
        st.bar_chart(df[col].value_counts())

st.markdown("---")
st.caption("Powered by Streamlit · Developed by Joana Paiva")
