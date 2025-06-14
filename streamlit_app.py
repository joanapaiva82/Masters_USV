import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap
import unicodedata

st.set_page_config(layout="wide")

# === PAGE STYLING ===
st.markdown("""
<style>
body {
    font-family: 'Arial Unicode MS', sans-serif;
}
div.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
h1, h2, h3 {
    color: #053752;
}
</style>
""", unsafe_allow_html=True)

# === TITLE + CONTEXT ===
st.title("📊 USV Industry Survey Dashboard – Expert Insights May 2025")
st.markdown("""
> This dashboard summarizes the results of a LinkedIn survey of hydrographic professionals on the **use of Uncrewed Surface Vessels (USVs)** vs. conventional platforms.

- 🗓️ Date Collected: **May 2025**  
- 🌍 Total Responses: **58**  
- 💡 Topics Covered: Cost, Efficiency, Technology, Operations
""")

with st.sidebar:
    st.markdown("### 🔎 Explore Sections")
    st.markdown("- 💰 Investment & Operational Cost")
    st.markdown("- ⚙️ Maintenance & Processing")
    st.markdown("- 📡 Task Suitability & Technology")
    st.markdown("- 🔒 Safety & Regulatory Considerations")

# === LOAD DATA ===
df = pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

# === QUESTIONS ===
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

# === HELPERS ===
def clean_chars(text):
    return (
        unicodedata.normalize("NFKC", str(text))
        .replace("’", "'").replace("‘", "'")
        .replace("–", "-").replace("−", "-")
        .replace("“", '"').replace("”", '"')
        .strip()
    )

def wrap_label(label, width=36):
    return "<br>".join(textwrap.wrap(clean_chars(label), width))

def get_q9_inverted_color(label):
    label = clean_chars(label)
    if label.startswith("1"): return "#d62728"
    elif label.startswith("2"): return "#ff9896"
    elif label.startswith("3"): return "#c7c7c7"
    elif label.startswith("4"): return "#8fd19e"
    elif label.startswith("5"): return "#2ca02c"
    return "#1f77b4"

def get_q1_q2_q3_color(label):
    l = clean_chars(label).lower()
    if "much lower" in l or "<10%" in l: return "#2ca02c"
    elif "somewhat lower" in l or "10-25%" in l: return "#8fd19e"
    elif "about the same" in l or "25-50%" in l: return "#c7c7c7"
    elif "somewhat higher" in l: return "#ff9896"
    elif "much higher" in l or ">50%" in l: return "#d62728"
    return "#1f77b4"

def group_safety_q13(series):
    mapping = {}
    for val in series:
        parts = sorted([clean_chars(s) for s in val.split(";")])
        key = "; ".join(parts)
        mapping[key] = mapping.get(key, 0) + 1
    return pd.Series(mapping).sort_values(ascending=False)

# === DONUT PLOT ===
def plot_donut(question):
    responses = df[question].dropna().astype(str).map(clean_chars)
    if responses.empty:
        st.warning("No responses.")
        return
    counts = responses.value_counts()
    labels = list(counts.index)

    if question == "How do you rate the operational efficiency of USVs vs. traditional vessels?":
        colors = [get_q9_inverted_color(l) for l in labels]
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
    fig.update_traces(textinfo='percent+label', textfont=dict(family="Arial Unicode MS", size=14))
    fig.update_layout(height=450, margin=dict(t=30, b=30), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# === BAR CHART ===
def plot_bar(question):
    responses = df[question].dropna().astype(str).map(clean_chars)
    if question == "Do you consider USV operations safe for commercial hydrographic use today?":
        counts = group_safety_q13(responses).reset_index()
        counts.columns = ['Answer', 'Responses']
    else:
        exploded = responses.str.split(";").explode().map(clean_chars)
        counts = exploded.value_counts().reset_index()
        counts.columns = ['Answer', 'Responses']

    # Group open-texts with <=1 response
    other_df = counts[(counts['Responses'] <= 1) & (counts['Answer'].str.len() > 50)].copy()
    shown = counts[~counts.index.isin(other_df.index)].copy()
    if not other_df.empty:
        total = other_df['Responses'].sum()
        shown = pd.concat([shown, pd.DataFrame([{'Answer': 'Other (open-text)', 'Responses': total}])], ignore_index=True)

    shown['Answer'] = shown['Answer'].apply(lambda x: wrap_label(x, 36))
    fig = px.bar(
        shown,
        x='Responses',
        y='Answer',
        orientation='h',
        text='Responses',
        color='Answer',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=max(580, len(shown)*40)
    )
    fig.update_traces(textposition='outside', textfont=dict(family="Arial Unicode MS", size=14))
    fig.update_layout(showlegend=False, margin=dict(t=30, l=320))
    st.plotly_chart(fig, use_container_width=True)

    if not other_df.empty:
        with st.expander("Show all 'Other (open-text)' responses"):
            st.dataframe(other_df[['Answer', 'Responses']].reset_index(drop=True), use_container_width=True)

# === PLOT ALL ===
for col in df.columns:
    if col in donut_qs + bar_qs:
        st.markdown("---")
        st.subheader(col)
        if col in donut_qs:
            plot_donut(col)
        else:
            plot_bar(col)
