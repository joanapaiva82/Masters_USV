# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")
st.title("USV Survey Dashboard - By Joana Paiva")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def wrap_label(text, width=35):
    return re.sub(r'(.{1,' + str(width) + r'})(\s+|$)', r'\1\n', text).strip()

def plot_donut(df, question, order, colors):
    counts = df[question].value_counts().reindex(order).dropna()
    fig = px.pie(
        names=counts.index,
        values=counts.values,
        hole=0.4,
        color=counts.index,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

def plot_horizontal_bar(df, question, filter_open_ended=False):
    responses = df[question].dropna().astype(str)
    exploded = responses.str.split(";").explode().str.strip()
    if filter_open_ended:
        exploded = exploded[exploded.str.len() < 80]
    counts = exploded.value_counts().reset_index()
    counts.columns = ['Answer', 'Responses']
    counts['Answer'] = counts['Answer'].apply(lambda x: wrap_label(x, width=40))
    fig = px.bar(
        counts,
        x='Responses',
        y='Answer',
        orientation='h',
        text='Responses',
        color='Answer',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=600
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# === Charts ===

st.subheader("Q6. What percentage of operational cost savings have you observed or expect from USVs?")
plot_donut(
    df,
    "What percentage of operational cost savings have you observed or expect from USVs?",
    ["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"],
    px.colors.qualitative.Pastel
)

st.subheader("Q7. How do maintenance costs compare between USVs and conventional vessels?")
plot_donut(
    df,
    "How do maintenance costs compare between USVs and conventional vessels?",
    ["Much lower", "About the same", "Much higher"],
    px.colors.qualitative.Set2
)

st.subheader("Q9. How do you rate the operational efficiency of USVs vs. traditional vessels?")
plot_donut(
    df,
    "How do you rate the operational efficiency of USVs vs. traditional vessels?",
    ["1 – Much less efficient", "2 – Slightly less efficient", "3 – About the same", "4 – Slightly more efficient", "5 – Much more efficient"],
    px.colors.qualitative.Dark24
)

st.subheader("Q13. Do you consider USV operations safe for commercial hydrographic use today?")
plot_donut(
    df,
    "Do you consider USV operations safe for commercial hydrographic use today?",
    ["Yes – proven in controlled settings", "Yes – with operator supervision", "Yes – depends on site type", "No – still key concerns", "Other"],
    px.colors.qualitative.Set2
)

st.subheader("Q15. What technologies will most influence USV adoption next?")
plot_horizontal_bar(df, "What technologies will most influence USV adoption next?", filter_open_ended=True)

st.subheader("Q16. How does data processing workflow differ when using USVs compared to traditional vessels?")
plot_horizontal_bar(df, "How does data processing workflow differ when using USVs compared to traditional vessels?", filter_open_ended=True)

st.markdown("---")
st.caption("USV Survey Dashboard - Cleaned and validated - Built by Joana Paiva")
