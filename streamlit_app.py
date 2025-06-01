
# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")
st.title("🚤 Masters Research USV Survey Dashboard - By Joana Paiva")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")
st.title("🚤 USV Survey Dashboard – Final Layout Matched")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def wrap_labels(series, width=25):
    return ['<br>'.join([line[i:i+width] for i in range(0, len(line), width)]) for line in series]

def plot_donut(df, question, order, colors):
    data = df[question].value_counts().reindex(order).dropna()
    fig = px.pie(
        names=data.index,
        values=data.values,
        hole=0.4,
        color=data.index,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

def plot_bar_wrapped(df, question):
    exploded = df[question].dropna().str.split(";").explode().str.strip()
    counts = exploded.value_counts().reset_index()
    counts.columns = ['Answer', 'Responses']
    counts['Answer'] = wrap_labels(counts['Answer'])
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

# === Chart Definitions ===
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
plot_bar_wrapped(df, "What technologies will most influence USV adoption next?")

st.subheader("Q16. How does data processing workflow differ when using USVs compared to traditional vessels?")
plot_bar_wrapped(df, "How does data processing workflow differ when using USVs compared to traditional vessels?")

st.markdown("---")
st.caption("📊 Final layout – verified column names and label wrapping – Joana Paiva · Streamlit 2025")

# Force rebuild

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="USV Survey Dashboard", layout="wide")
st.title("🚤 USV Survey Dashboard – Final Layout Matched")

@st.cache_data
def load_data():
    return pd.read_csv("usv_survey_data.csv", encoding="ISO-8859-1")

df = load_data()
df.columns = df.columns.str.replace(u'\xa0', ' ', regex=True).str.strip()

def wrap_labels(series, width=25):
    return ['<br>'.join([line[i:i+width] for i in range(0, len(line), width)]) for line in series]

def plot_donut(df, question, order, colors):
    data = df[question].value_counts().reindex(order).dropna()
    fig = px.pie(
        names=data.index,
        values=data.values,
        hole=0.4,
        color=data.index,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

def plot_bar_wrapped(df, question):
    exploded = df[question].dropna().str.split(";").explode().str.strip()
    counts = exploded.value_counts().reset_index()
    counts.columns = ['Answer', 'Responses']
    counts['Answer'] = wrap_labels(counts['Answer'])
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

# === Chart Definitions ===
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
plot_bar_wrapped(df, "What technologies will most influence USV adoption next?")

st.subheader("Q16. How does data processing workflow differ when using USVs compared to traditional vessels?")
plot_bar_wrapped(df, "How does data processing workflow differ when using USVs compared to traditional vessels?")

st.markdown("---")
st.caption("📊 Final layout – verified column names and label wrapping – Joana Paiva · Streamlit 2025")

def plot_donut(df, question, order, colors):
    data = df[question].value_counts().reindex(order).dropna()
    fig = px.pie(
        names=data.index,
        values=data.values,
        hole=0.4,
        color=data.index,
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(df, question):
    exploded = df[question].dropna().str.split(";").explode().str.strip()
    counts = exploded.value_counts().reset_index()
    counts.columns = ['Answer', 'Responses']
    fig = px.bar(
        counts,
        x='Responses',
        y='Answer',
        orientation='h',
        text='Responses',
        color='Answer',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=500
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Q5 (Donut)
st.subheader("Q5. How do you rate the initial investment cost of USVs compared to traditional vessels?")
plot_donut(
    df,
    "How do you rate the initial investment cost of USVs compared to traditional vessels?",
    ["Much lower", "Somewhat lower", "About the same", "Somewhat higher", "Much higher"],
    ["#636EFA", "#EF476F", "#00B6AD", "#B983FF", "#80C904"]
)

# Q6 (Donut)
st.subheader("Q6. What percentage of operational cost savings have you observed or expect from USVs?")
plot_donut(
    df,
    "What percentage of operational cost savings have you observed or expect from USVs?",
    ["<10% savings", "10–25% savings", "25–50% savings", ">50% savings"],
    px.colors.qualitative.Pastel
)

# Q7 (Donut)
st.subheader("Q7. How do maintenance costs compare between USVs and conventional vessels?")
plot_donut(
    df,
    "How do maintenance costs compare between USVs and conventional vessels?",
    ["Much lower", "About the same", "Much higher"],
    px.colors.qualitative.Set2
)

# Q8 (Bar)
st.subheader("Q8. Cost-related factors influencing USV adoption")
plot_bar(df, "Which cost-related factors most influence USV adoption in your company?")

# Q9 (Donut)
st.subheader("Q9. How do you rate the operational efficiency of USVs vs. traditional vessels?")
plot_donut(
    df,
    "How do you rate the operational efficiency of USVs vs. traditional vessels?",
    ["1 – Much less efficient", "2 – Slightly less efficient", "3 – About the same", "4 – Slightly more efficient", "5 – Much more efficient"],
    px.colors.qualitative.Dark24
)

# Q10 (Bar)
st.subheader("Q10. Project types best suited for USVs")
plot_bar(df, "In your view, Which project types are best suited for USVs today?")

# Q11 (Bar)
st.subheader("Q11. Barriers to fully replacing manned vessels")
plot_bar(df, "What are the main barriers to USVs fully replacing manned vessels?")

# Q12 (Bar)
st.subheader("Q12. Unknowns or uncertainties with USVs")
plot_bar(df, "What are the biggest unknowns or uncertainties with USVs in survey use?")

# Q13 (Donut)
st.subheader("Q13. Safety of USV operations")
plot_donut(
    df,
    "Do you consider USV operations safe for commercial hydrographic use today?",
    ["Yes – proven in controlled settings", "Yes – with operator supervision", "Yes – depends on site type", "No – still key concerns", "Other"],
    px.colors.qualitative.Set2
)

# Q14 (Bar)
st.subheader("Q14. Data collection capability vs. conventional vessels")
plot_bar(df, "How does the data collection capability of USVs compare to conventional vessels?")

# Q15 (Bar)
st.subheader("Q15. Technologies influencing USV adoption")
plot_bar(df, "What technologies will most influence USV adoption next?")

# Q16 (Bar)
st.subheader("Q16. How does data processing workflow differ when using USVs?")
plot_bar(df, "How does data processing workflow differ when using USVs compared to traditional vessels?")

st.markdown("---")
st.caption("📊 Fully verified layout – built by Joana Paiva – Streamlit 2025")
