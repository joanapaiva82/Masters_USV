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
    return "<br>".join(textwrap.wrap(str(label).replace(">", ">").replace("<", "<"), width))

def get_q9_color(label):
    if label.startswith("1"):
        return "#2ca02c"
    elif label.startswith("2"):
        return "#8fd19e"
    elif label.startswith("3"):
        return "#c7c7c7"
    elif label.startswith("4"):
        return "#ff9896"
    elif label.startswith("5"):
        return "#d62728"
    return "#1f77b4"

def clean_q13_answer(text):
    parts = sorted([p.strip() for p in text.split(";")])
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

    if question == "How do you rate the operational efficiency of USVs vs. traditional vessels?":
        counts = responses.value_counts()
        labels = list(counts.index)
        colors = [get_q9_color(l) for l in labels]
    elif question == "Do you consider USV operations safe for commercial hydrographic use today?":
        grouped = responses.map(clean_q13_answer)
        counts = grouped.value_counts()
        labels = list(counts.index)
        colors = ["#1f77b4"] * len(labels)
    else:
        counts = responses.value_counts()
        labels = list(counts.index)
        colors = ["#1f77b4"] * len(labels)

    fig = px.pie(
        names=[wrap_label(l) for l in labels],
        values=counts.values,
        hole=0.4,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=450, margin=dict(t=30, b=30), showlegend=True, legend_title_text='')
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(question):
    responses = df[question].dropna().astype(str)
    exploded = responses.str.split(";").explode().str.strip()
    if exploded.empty:
        st.warning("No data.")
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
        height=max(500, len(counts) * 32)
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, margin=dict(t=30, l=250))
    st.plotly_chart(fig, use_container_width=True)

# Display all questions
for col in df.columns:
    if col in donut_qs + bar_qs:
        st.subheader(col)
        if col in donut_qs:
            plot_donut(col)
        else:
            plot_bar(col)
