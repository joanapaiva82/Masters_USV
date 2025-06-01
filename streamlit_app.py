
import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap

st.set_page_config(layout="wide")
st.title("USV Survey Results Dashboard")

df = pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

donut_qs = [
    "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    "What percentage of operational cost savings have you observed or expect from USVs?",
    "How do maintenance costs compare between USVs and conventional vessels?",
    "How do you rate the operational efficiency of USVs vs. traditional vessels?"
]

bar_qs = [
    "Which cost-related factors most influence USV adoption in your company?",
    "In your view, Which project types are best suited for USVs today?",
    "What are the main barriers to USVs fully replacing manned vessels?",
    "What are the biggest unknowns or uncertainties with USVs in survey use?",
    "How does the data collection capability of USVs compare to conventional vessels?",
    "What technologies will most influence USV adoption next?",
    "How does data processing workflow differ when using USVs compared to traditional vessels?",
    "Do you consider USV operations safe for commercial hydrographic use today?"
]

def wrap_label(label, width=40):
    return "<br>".join(textwrap.wrap(label.replace("–", "–").replace("-", "–"), width))

def get_color(label):
    label = label.replace("–", "-").strip()
    if label in ["Much lower", "<10%", "1 – Much less efficient"]:
        return "#2ca02c"
    elif label in ["Somewhat lower", "10–25%", "2 – Slightly less efficient"]:
        return "#8fd19e"
    elif label in ["About the same", "3 – About the same"]:
        return "#c7c7c7"
    elif label in ["Somewhat higher", "25–50%", "4 – Slightly more efficient"]:
        return "#ff9896"
    elif label in ["Much higher", ">50%", "5 – Much more efficient"]:
        return "#d62728"
    return "#1f77b4"

def clean_q13(text):
    parts = sorted([p.strip().replace("-", "–") for p in text.split(";")])
    if "Yes – with operator supervision" in parts and "Yes – depends on site type" in parts:
        return "Yes – with supervision + depends on site type"
    if "Yes – proven in controlled settings" in parts and "Yes – with operator supervision" in parts:
        return "Yes – proven + supervision"
    if "Yes – proven in controlled settings" in parts and "Yes – depends on site type" in parts:
        return "Yes – proven + depends on site type"
    return "; ".join(parts)

def plot_donut(question):
    responses = df[question].dropna().astype(str).str.strip()
    if responses.empty:
        st.warning("No responses.")
        return
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
    fig.update_layout(height=450, margin=dict(t=30, b=30), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(question):
    responses = df[question].dropna().astype(str)
    if question == "Do you consider USV operations safe for commercial hydrographic use today?":
        grouped = responses.map(clean_q13)
        counts = grouped.value_counts().reset_index()
        counts.columns = ['Answer', 'Responses']
    else:
        exploded = responses.str.split(";").explode().str.strip()
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
        height=max(500, len(counts)*32)
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, margin=dict(t=30, l=250))
    st.plotly_chart(fig, use_container_width=True)

# Run all
for col in df.columns:
    if col in donut_qs + bar_qs:
        st.subheader(col)
        if col in donut_qs:
            plot_donut(col)
        else:
            plot_bar(col)
