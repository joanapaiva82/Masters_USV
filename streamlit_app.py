# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")

st.title("🚤 USV Survey Dashboard – May 2025")
st.markdown("Visual overview of survey responses related to Uncrewed Surface Vessels (USVs).")

@st.cache_data
def load_data():
    return pd.read_excel("usv_survey_data.xlsx")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def plot_question_summary(df, question, order=None, colors=None):
    value_counts = df[question].value_counts().sort_index() if order is None else df[question].value_counts().reindex(order)
    value_counts = value_counts.dropna()
    labels = value_counts.index.tolist()
    counts = value_counts.values.tolist()

    fig = px.pie(
        names=labels,
        values=counts,
        hole=0.4,
        color_discrete_sequence=colors or px.colors.qualitative.Set2
    )
    fig.update_traces(textinfo='percent+label', textposition='outside')
    fig.update_layout(showlegend=True, margin=dict(t=20, b=20, l=20, r=20), height=400)

    st.plotly_chart(fig, use_container_width=True, key=question)

# --- Tabs ---
tabs = st.tabs([
    "Q5: Investment Cost", "Q6: Operational Savings", "Q7: Maintenance Costs",
    "Q9: Efficiency", "Q13: Safety", "Q14: Data Capability", "Q16: Processing Workflow"
])

with tabs[0]:
    plot_question_summary(
        df,
        "How do you rate the initial investment cost of USVs compared to traditional vessels?",
        order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"]
    )

with tabs[1]:
    plot_question_summary(
        df,
        "What percentage of operational cost savings have you observed or expect from USVs?",
        order=["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"]
    )

with tabs[2]:
    plot_question_summary(
        df,
        "How do maintenance costs compare between USVs and conventional vessels?",
        order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"]
    )

with tabs[3]:
    plot_question_summary(
        df,
        "How do you rate the operational efficiency of USVs vs. traditional vessels?",
        order=["1 – Much less efficient", "2", "3 – About the same", "4", "5 – Much more efficient"]
    )

with tabs[4]:
    plot_question_summary(
        df,
        "Do you consider USV operations safe for commercial hydrographic use today?",
        order=[
            "No – not proven yet", 
            "Yes – with operator supervision", 
            "Yes – proven in controlled settings", 
            "Yes – in most commercial environments"
        ]
    )

with tabs[5]:
    plot_question_summary(
        df,
        "How does the data collection capability of USVs compare to conventional vessels?",
        order=[
            "Significantly better with conventional vessels",
            "Slightly better with conventional vessels",
            "About the same",
            "Slightly better with USVs",
            "Significantly better with USVs"
        ]
    )

with tabs[6]:
    plot_question_summary(
        df,
        "How does data processing workflow differ when using USVs compared to traditional vessels?",
        order=[
            "Significantly slower",
            "Slightly slower",
            "About the same",
            "Slightly faster",
            "Significantly faster"
        ]
    )

st.markdown("---")
st.caption("📊 Charts only · Powered by Streamlit · Built by Joana Paiva")
