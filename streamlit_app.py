
import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap

st.set_page_config(layout="wide")
st.title("USV Survey Results Dashboard")

df = pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.replace(u' ', ' ', regex=True).str.strip()

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

def get_q6_q7_color(label):
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

def plot_donut(question):
    responses = df[question].dropna().astype(str).str.strip()
    if responses.empty:
        st.warning("No responses.")
        return
    counts = responses.value_counts()
    labels = list(counts.index)
    colors = [get_q6_q7_color(l) for l in labels]
    fig = px.pie(
        names=[wrap_label(l) for l in labels],
        values=counts.values,
        hole=0.4,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=450, margin=dict(t=30, b=30), showlegend=True, legend_title_text='')
    st.plotly_chart(fig, use_container_width=True)

# Display just Q6 and Q7
for q in donut_qs:
    if q in [
        "What percentage of operational cost savings have you observed or expect from USVs?",
        "How do maintenance costs compare between USVs and conventional vessels?"
    ]:
        st.subheader(q)
        plot_donut(q)
