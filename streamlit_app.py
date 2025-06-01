
# Force rebuild

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="USV Survey Dashboard – Q5 & Q6", layout="wide")
st.title("🚤 USV Survey Dashboard – Q5 & Q6 Visual Match")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def plot_q_pdf_style(question, order, colors):
    counts = df[question].value_counts().reindex(order).dropna()
    total = counts.sum()
    percentages = (counts / total * 100).round(1)
    labels = [f"{int(c)} ({p}%)" for c, p in zip(counts, percentages)]

    fig = go.Figure(go.Bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        marker_color=colors[:len(counts)],
        text=labels,
        textposition='auto'
    ))
    fig.update_layout(
        xaxis_title="Responses",
        yaxis_title="",
        height=400,
        margin=dict(t=40, b=40),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# === Q5 ===
st.subheader("Q5. How do you rate the initial investment cost of USVs compared to traditional vessels?")
plot_q_pdf_style(
    "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    order=["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"],
    colors=["#636EFA", "#EF476F", "#00B6AD", "#B983FF", "#80C904"]
)

# === Q6 ===
st.subheader("Q6. What percentage of operational cost savings have you observed or expect from USVs?")
plot_q_pdf_style(
    "What percentage of operational cost savings have you observed or expect from USVs?",
    order=["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"],
    colors=["#636EFA", "#EF476F", "#00B6AD", "#B983FF"]
)

st.markdown("---")
st.caption("✅ Matched exactly to FormSummary – built by Joana Paiva")
