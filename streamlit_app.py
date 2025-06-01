import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap

st.set_page_config(layout="wide")
st.title("USV Survey Results Dashboard")

# Load data
df = pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

# Donut questions
donut_qs = [
    "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    "What percentage of operational cost savings have you observed or expect from USVs?",
    "How do maintenance costs compare between USVs and conventional vessels?",
    "How do you rate the operational efficiency of USVs vs. traditional vessels?"
]

# Bar questions
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

# Wrap long labels
def wrap_label(label, width=40):
    return "<br>".join(textwrap.wrap(str(label).replace("-", "–"), width))

# Gradient for Q9
def get_q9_color(label):
    label = label.strip()
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

# Gradient for Q1, Q2, Q3
def get_q1_q2_q3_color(label):
    label = label.replace("-", "–").strip().lower()
    if "much lower" in label or "<10%" in label:
        return "#2ca02c"
    elif "somewhat lower" in label or "10–25%" in label:
        return "#8fd19e"
    elif "about the same" in label or "25–50%" in label:
        return "#c7c7c7"
    elif "somewhat higher" in label:
        return "#ff9896"
    elif "much higher" in label or ">50%" in label:
        return "#d62728"
    return "#1f77b4"

# Group Q13 multi-responses
def group_safety_q13(series):
    mapping = {}
    for val in series:
        clean = "–".join([s.strip().replace("-", "–") for s in val.split(";")])
        mapping[clean] = mapping.get(clean, 0) + 1
    return pd.Series(mapping).sort_values(ascending=False)

# Plot donut
def plot_donut(question):
    responses = df[question].dropna().astype(str).str.strip()
    if responses.empty:
        st.warning("No responses.")
        return

    counts = responses.value_counts()
    labels = list(counts.index)

    if question == "How do you rate the operational efficiency of USVs vs. traditional vessels?":
        colors = [get_q9_color(l) for l in labels]
    elif question in donut_qs[:3]:
        colors = [get_q1_q2_q3_color(l) for l in labels]
    else:
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

# Plot bar
def plot_bar(question):
    responses = df[question].dropna().astype(str)
    if question == "Do you consider USV operations safe for commercial hydrographic use today?":
        counts = group_safety_q13(responses).reset_index()
        counts.columns = ['Answer', 'Responses']
    else:
        exploded = responses.str.split(";").explode().str.strip()
        counts = exploded.value_counts().reset_index()
        counts.columns = ['Answer', 'Responses']

    # Group long single answers into "Other"
    other_texts = counts[(counts['Responses'] == 1) & (counts['Answer'].str.len() > 60)]
    shown = counts[~counts.index.isin(other_texts.index)].copy()
    if not other_texts.empty:
        total = other_texts['Responses'].sum()
        shown = pd.concat([shown, pd.DataFrame([{'Answer': 'Other (open-text)', 'Responses': total}])], ignore_index=True)

    shown['Answer'] = shown['Answer'].apply(lambda x: wrap_label(x, 40))
    fig = px.bar(
        shown,
        x='Responses',
        y='Answer',
        orientation='h',
        text='Responses',
        color='Answer',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=max(500, len(shown) * 32)
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, margin=dict(t=30, l=250))
    st.plotly_chart(fig, use_container_width=True)

# Loop through questions
for col in df.columns:
    if col in donut_qs + bar_qs:
        st.subheader(col)
        if col in donut_qs:
            plot_donut(col)
        else:
            plot_bar(col)
