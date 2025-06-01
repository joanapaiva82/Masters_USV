
import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap
from collections import Counter

st.set_page_config(layout="wide")
st.title("USV Survey Results Dashboard")

# Load CSV
df = pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

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

def wrap_label(label, width=40):
    return "<br>".join(textwrap.wrap(label.replace(">", "\u003e").replace("<", "\u003c"), width))

def get_color(label):
    label = label.lower().strip()
    if "much lower" in label or "<10" in label or "1 –" in label:
        return "#2ca02c"  # green
    elif "somewhat lower" in label or "10" in label or "2 –" in label:
        return "#8fd19e"
    elif "about the same" in label or "3 –" in label:
        return "#c7c7c7"
    elif "somewhat higher" in label or "25" in label or "4 –" in label:
        return "#ff9896"
    elif "much higher" in label or ">50" in label or "5 –" in label:
        return "#d62728"  # red
    return "#1f77b4"

def group_responses(series):
    group_map = {}
    for resp in series:
        parts = [p.strip() for p in str(resp).split(";") if p.strip()]
        sorted_parts = ";".join(sorted(parts))
        group_map[sorted_parts] = group_map.get(sorted_parts, 0) + 1
    grouped = pd.Series(group_map).sort_values(ascending=False)
    return grouped

def plot_donut(question):
    responses = df[question].dropna().astype(str).str.strip()
    if responses.empty:
        st.warning("No responses for this question.")
        return
    if question == "Do you consider USV operations safe for commercial hydrographic use today?":
        counts = group_responses(responses)
        labels = list(counts.index)
    else:
        counts = responses.value_counts()
        labels = list(counts.index)

    colors = [get_color(l) for l in labels]
    fig = px.pie(
        names=[wrap_label(l) for l in labels],
        values=counts.values,
        hole=0.4,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        height=450,
        margin=dict(t=30, b=30),
        showlegend=True,
        legend_title_text=''
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(question):
    responses = df[question].dropna().astype(str)
    exploded = responses.str.split(";").explode().str.strip()
    if exploded.empty:
        st.warning("No responses for this question.")
        return
    counts = exploded.value_counts().reset_index()
    counts.columns = ['Answer', 'Responses']

    other_texts = counts[(counts['Responses'] == 1) & (counts['Answer'].str.len() > 60)]
    shown = counts[~counts.index.isin(other_texts.index)].copy()
    if not other_texts.empty:
        other_count = other_texts['Responses'].sum()
        other_row = pd.DataFrame([{'Answer': 'Other (open-text)', 'Responses': other_count}])
        shown = pd.concat([shown, other_row], ignore_index=True)

    shown['Answer'] = shown['Answer'].apply(lambda x: wrap_label(x, 40))
    fig = px.bar(
        shown,
        x='Responses',
        y='Answer',
        orientation='h',
        text='Responses',
        color='Answer',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=max(500, len(shown)*32)
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, margin=dict(t=30, l=250))
    st.plotly_chart(fig, use_container_width=True)

for col in df.columns:
    if col in donut_qs + bar_qs:
        st.subheader(col)
        if col in donut_qs:
            plot_donut(col)
        else:
            plot_bar(col)
