# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")

st.title("🚤 USV Survey Dashboard – May 2025")
st.markdown("Visualized insights from 58 responses on Uncrewed Surface Vessels (USVs).")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

# === Bar chart for single-answer questions ===
def plot_bar_chart(df, question, order=None):
    counts = df[question].value_counts().sort_index() if order is None else df[question].value_counts().reindex(order)
    counts = counts.dropna()
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        color=counts.index,
        labels={'x': 'Responses', 'y': question},
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=400
    )
    fig.update_layout(showlegend=False, margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig, use_container_width=True, key=question)

# === Bar chart for multi-select questions ===
def plot_multi_bar(df, question):
    responses = df[question].dropna().str.split(";").explode().str.strip()
    counts = responses.value_counts().reset_index()
    counts.columns = ['Response', 'Count']
    fig = px.bar(
        counts,
        x='Count',
        y='Response',
        orientation='h',
        color='Response',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=500
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True, key=question)

# === Tabs per question ===
tabs = st.tabs([
    "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16"
])

with tabs[0]:
    plot_bar_chart(df,
        "How do you rate the initial investment cost of USVs compared to traditional vessels?",
        order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"]
    )

with tabs[1]:
    plot_bar_chart(df,
        "What percentage of operational cost savings have you observed or expect from USVs?",
        order=["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"]
    )

with tabs[2]:
    plot_bar_chart(df,
        "How do maintenance costs compare between USVs and conventional vessels?",
        order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"]
    )

with tabs[3]:
    plot_multi_bar(df, "Which cost-related factors most influence USV adoption in your company?")

with tabs[4]:
    plot_bar_chart(df,
        "How do you rate the operational efficiency of USVs vs. traditional vessels?",
        order=["1 – Much less efficient", "2 – Slightly less efficient", "3 – About the same", "4 – Slightly more efficient", "5 – Much more efficient"]
    )

with tabs[5]:
    plot_multi_bar(df, "In your view, Which project types are best suited for USVs today?")

with tabs[6]:
    plot_multi_bar(df, "What are the main barriers to USVs fully replacing manned vessels?")

with tabs[7]:
    plot_multi_bar(df, "What are the biggest unknowns or uncertainties with USVs in survey use?")

with tabs[8]:
    plot_bar_chart(df,
        "Do you consider USV operations safe for commercial hydrographic use today?",
        order=[
            "No – not proven yet",
            "Yes – with operator supervision",
            "Yes – proven in controlled settings",
            "Yes – in most commercial environments",
            "Yes – depends on site type",
            "Other"
        ]
    )

with tabs[9]:
    plot_bar_chart(df,
        "How does the data collection capability of USVs compare to conventional vessels?",
        order=[
            "Significantly better with USVs",
            "Slightly better with USVs",
            "About the same",
            "Slightly better with conventional vessels",
            "Significantly better with conventional vessels",
            "Other"
        ]
    )

with tabs[10]:
    plot_multi_bar(df, "What technologies will most influence USV adoption next?")

with tabs[11]:
    plot_bar_chart(df,
        "How does data processing workflow differ when using USVs compared to traditional vessels?",
        order=[
            "Significantly faster",
            "Slightly faster",
            "About the same",
            "Slower",
            "Not applicable / I don’t know",
            "Other"
        ]
    )

st.markdown("---")
st.caption("📊 Data treated & visualized · Built by Joana Paiva · Streamlit 2025")
