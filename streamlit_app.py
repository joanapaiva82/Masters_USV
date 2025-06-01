# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")

st.title("🚤 USV Survey Dashboard – May 2025")
st.markdown("Charts based on the original Microsoft Forms response summary.")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def plot_pdf_style_bar(df, question, order=None, show_percent=True):
    counts = df[question].value_counts().sort_index() if order is None else df[question].value_counts().reindex(order)
    counts = counts.dropna()
    total = counts.sum()
    percent = counts / total * 100 if show_percent else None
    labels = [f"{v} ({p:.1f}%)" if show_percent else f"{v}" for v, p in zip(counts.index, percent)]
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        text=[f"{int(v)}" for v in counts.values],
        labels={'x': 'Responses', 'y': ''},
        color=counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=400
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

def plot_pdf_multibar(df, question):
    responses = df[question].dropna().str.split(";").explode().str.strip()
    counts = responses.value_counts()
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        text=[f"{int(v)}" for v in counts.values],
        labels={'x': 'Responses', 'y': ''},
        color=counts.index,
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=500
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# === Section layout by Q number ===
st.header("Q5 – Initial Investment Cost")
plot_pdf_style_bar(df, "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"])

st.header("Q6 – Operational Cost Savings")
plot_pdf_style_bar(df, "What percentage of operational cost savings have you observed or expect from USVs?",
    order=["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"])

st.header("Q7 – Maintenance Costs")
plot_pdf_style_bar(df, "How do maintenance costs compare between USVs and conventional vessels?",
    order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"])

st.header("Q8 – Cost-Related Factors for Adoption")
plot_pdf_multibar(df, "Which cost-related factors most influence USV adoption in your company?")

st.header("Q9 – Operational Efficiency")
plot_pdf_style_bar(df, "How do you rate the operational efficiency of USVs vs. traditional vessels?",
    order=["1 – Much less efficient", "2 – Slightly less efficient", "3 – About the same", "4 – Slightly more efficient", "5 – Much more efficient"])

st.header("Q10 – Best-Suited Project Types")
plot_pdf_multibar(df, "In your view, Which project types are best suited for USVs today?")

st.header("Q11 – Barriers to USV Adoption")
plot_pdf_multibar(df, "What are the main barriers to USVs fully replacing manned vessels?")

st.header("Q12 – Unknowns or Uncertainties")
plot_pdf_multibar(df, "What are the biggest unknowns or uncertainties with USVs in survey use?")

st.header("Q13 – Safety of USV Operations")
plot_pdf_style_bar(df, "Do you consider USV operations safe for commercial hydrographic use today?",
    order=[
        "No – not proven yet",
        "Yes – with operator supervision",
        "Yes – proven in controlled settings",
        "Yes – in most commercial environments",
        "Yes – depends on site type",
        "Other"
    ])

st.header("Q14 – Data Collection Capability")
plot_pdf_style_bar(df, "How does the data collection capability of USVs compare to conventional vessels?",
    order=[
        "Significantly better with USVs",
        "Slightly better with USVs",
        "About the same",
        "Slightly better with conventional vessels",
        "Significantly better with conventional vessels",
        "Other"
    ])

st.header("Q15 – Technologies Influencing Adoption")
plot_pdf_multibar(df, "What technologies will most influence USV adoption next?")

st.header("Q16 – Data Processing Workflow Differences")
plot_pdf_style_bar(df, "How does data processing workflow differ when using USVs compared to traditional vessels?",
    order=[
        "Significantly faster",
        "Slightly faster",
        "About the same",
        "Slower",
        "Not applicable / I don’t know",
        "Other"
    ])

st.markdown("---")
st.caption("🧾 Matched to Microsoft Forms chart layout · Built by Joana Paiva · Streamlit 2025")
