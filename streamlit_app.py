
# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")
st.title("🚤 USV Survey Dashboard – May 2025")
st.markdown("Visualization structured to match the official Microsoft Forms response summary.")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def plot_bar_pdf_style(df, question, order):
    counts = df[question].value_counts().reindex(order).dropna()
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        text=counts.values,
        color=counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=400
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig, use_container_width=True, key=question)

def plot_multiselect_bar(df, question):
    responses = df[question].dropna().str.split(";").explode().str.strip()
    counts = responses.value_counts()
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        text=counts.values,
        color=counts.index,
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=500
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True, key=question)

# Q5–Q16 layout
plot_bar_pdf_style(df, "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    ["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"])

plot_bar_pdf_style(df, "What percentage of operational cost savings have you observed or expect from USVs?",
    ["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"])

plot_bar_pdf_style(df, "How do maintenance costs compare between USVs and conventional vessels?",
    ["Much lower", "About the same", "Much higher"])

plot_multiselect_bar(df, "Which cost-related factors most influence USV adoption in your company?")

plot_bar_pdf_style(df, "How do you rate the operational efficiency of USVs vs. traditional vessels?",
    ["1 – Much less efficient", "2 – Slightly less efficient", "3 – About the same", "4 – Slightly more efficient", "5 – Much more efficient"])

plot_multiselect_bar(df, "In your view, Which project types are best suited for USVs today?")
plot_multiselect_bar(df, "What are the main barriers to USVs fully replacing manned vessels?")
plot_multiselect_bar(df, "What are the biggest unknowns or uncertainties with USVs in survey use?")

plot_bar_pdf_style(df, "Do you consider USV operations safe for commercial hydrographic use today?",
    ["Yes – proven in controlled settings", "Yes – with operator supervision", "Yes – depends on site type", "No – still key concerns", "Other"])

plot_bar_pdf_style(df, "How does the data collection capability of USVs compare to conventional vessels?",
    ["Significantly better with USVs", "Slightly better with USVs", "About the same", "Slightly better with conventional vessels", "Significantly better with conventional vessels", "Other"])

plot_multiselect_bar(df, "What technologies will most influence USV adoption next?")

plot_bar_pdf_style(df, "How does data processing workflow differ when using USVs compared to traditional vessels?",
    ["Significantly faster", "Slightly faster", "About the same", "Slower", "Not applicable / I don’t know", "Other"])

st.markdown("---")
st.caption("📊 Layout aligned with Microsoft Forms PDF · Built by Joana Paiva · Streamlit 2025")
