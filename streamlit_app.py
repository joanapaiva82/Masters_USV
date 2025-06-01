
import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap
from collections import Counter

st.set_page_config(layout="wide")
st.title("USV Survey Results Dashboard")

# Load CSV data
df = pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

# Define chart types from the PDF
donut_qs = [
    "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    "What percentage of operational cost savings have you observed or expect from USVs?",
    "How do maintenance costs compare between USVs and conventional vessels?",
    "How do you rate the operational efficiency of USVs vs. traditional vessels?",
    "Do you consider USV operations safe for commercial hydrographic use today?"
]

bar_qs = [
    "Which cost-related factors most influence USV adoption in your company?",
    "In your view, Which project types are best suited for USVs today?",
    "What are the main barriers to USVs fully replacing manned vessels?",
    "What are the biggest unknowns or uncertainties with USVs in survey use?",
    "How does the data collection capability of USVs compare to conventional vessels?",
    "What technologies will most influence USV adoption next?",
    "How does data processing workflow differ when using USVs compared to traditional vessels?"
]

def wrap_label(label, width=35):
    return "<br>".join(textwrap.wrap(str(label), width=width))

def plot_donut(question):
    responses = df[question].dropna().astype(str).str.strip()
    if responses.empty:
        st.warning("No responses for this question.")
        return
    counts = responses.value_counts()
    fig = px.pie(
        names=[wrap_label(k) for k in counts.index],
        values=counts.values,
        hole=0.4
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=400, margin=dict(t=30, b=30))
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(question):
    responses = df[question].dropna().astype(str)
    exploded = responses.str.split(";").explode().str.strip()
    if exploded.empty:
        st.warning("No responses for this question.")
        return
    counts = exploded.value_counts().reset_index()
    counts.columns = ['Answer', 'Responses']
    counts['Answer'] = counts['Answer'].apply(lambda x: wrap_label(x, 40))
    fig = px.bar(
        counts,
        x='Responses',
        y='Answer',
        orientation='h',
        text='Responses',
        color='Answer',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=max(400, len(counts)*30)
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Render all Q5–Q16
for col in df.columns:
    if col.startswith("How") or col.startswith("What") or col.startswith("In your view") or col.startswith("Do you"):
        st.subheader(col)
        if col in donut_qs:
            plot_donut(col)
        elif col in bar_qs:
            plot_bar(col)
