# streamlit_app.py

import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Page configuration
st.set_page_config(page_title="USV Survey Dashboard", layout="wide")
st.title("USV Survey Results Dashboard")

# Load survey data from Excel or CSV
df = None
data_loaded = False
try:
    # Try Excel file first
    df = pd.read_excel('usv_survey_data.xlsx', engine='openpyxl')
    data_loaded = True
except Exception as e:
    try:
        # Fallback to CSV if Excel not found/failed
        df = pd.read_csv('usv_survey_data.csv')
        data_loaded = True
    except Exception as e:
        st.error("Error: Could not load survey data. Please ensure the Excel or CSV data file is present.")
        data_loaded = False

if not data_loaded:
    st.stop()  # Stop app if no data was loaded

# Helper function to wrap long labels into two lines for readability
def wrap_label(label, width=20):
    """Wrap a label string into at most two lines for better readability."""
    label = str(label)
    if len(label) <= width:
        return label
    # Find a space near the middle of the label to break the line
    midpoint = len(label) // 2
    break_idx = label.find(' ', midpoint)
    if break_idx == -1 or break_idx < width * 0.5 or break_idx > width * 1.5:
        # If no suitable space around midpoint, break at the last space before the width
        break_idx = label.rfind(' ', 0, width)
    if break_idx == -1:
        # If no space found, just break at the specified width
        break_idx = width
    # Construct the new label with a line break
    return label[:break_idx] + "<br>" + label[break_idx+1:]

# Define which questions use donut vs bar charts
donut_questions = [5, 6, 7, 9, 13]           # questions to plot as donut charts
bar_questions   = [8, 10, 11, 12, 14, 15, 16]  # questions to plot as horizontal bar charts

# Utility to get all column names corresponding to a given question number (handles multi-part questions)
def get_question_columns(q_number):
    q_prefix = f"Q{q_number}"
    return [col for col in df.columns if str(col).startswith(q_prefix)]

# Plot donut charts (two charts per row for better use of space)
for idx in range(0, len(donut_questions), 2):
    cols = st.columns(2)
    for j in range(2):
        if idx + j >= len(donut_questions):
            break  # no more donut questions to plot in this row
        q = donut_questions[idx + j]
        col_list = get_question_columns(q)
        if not col_list:
            cols[j].warning(f"Question Q{q} data not found.")
            continue
        # Expect a single column for each donut question
        col_name = col_list[0]
        question_text = col_name  # use column name (which includes question text) as title
        # Get responses for this question, drop empty responses
        series = df[col_name].dropna()
        series = series[series.astype(str).str.strip() != ""]
        if series.empty:
            cols[j].warning(f"No responses for {question_text}")
            continue
        # Compute frequency of each response category
        counts = series.astype(str).value_counts(dropna=True)
        labels = list(counts.index)
        values = counts.values
        # Create donut chart with percentages and labels
        fig = px.pie(values=values, names=[wrap_label(label) for label in labels], hole=0.4)
        fig.update_traces(textinfo='percent+label')  # show percentage and label on slices
        fig.update_layout(margin=dict(t=40, b=40), legend_title_text='')
        # Display the question heading and chart in the column
        cols[j].subheader(question_text)
        cols[j].plotly_chart(fig, use_container_width=True)

# Plot horizontal bar charts (one per row)
for q in bar_questions:
    col_list = get_question_columns(q)
    if not col_list:
        st.warning(f"Question Q{q} data not found.")
        continue
    # Determine how to aggregate answers for this question
    if len(col_list) > 1:
        # Multi-column question (e.g., multi-select with one column per option)
        prefix = os.path.commonprefix(col_list).rstrip(" -:")
        # Use the common prefix as the question text if it's more than just "Q{num}"
        question_text = prefix if prefix and len(prefix) > len(f"Q{q}") + 1 else col_list[0]
        st.subheader(question_text)
        categories = []
        counts = []
        # Count selections for each option column
        for col_name in col_list:
            # Drop empty responses
            series = df[col_name].dropna()
            series = series[series.astype(str).str.strip() != ""]
            if series.empty:
                continue  # no one selected this option
            # Determine how to count a "selected" response for this option
            vals = series.unique()
            vals_clean = [str(v).strip().lower() for v in vals if str(v).strip() != ""]
            if any(v in ["yes", "y", "true", "t", "1", "checked", "selected"] for v in vals_clean):
                # Count entries that indicate a positive selection (Yes/True/1/etc.)
                count_val = sum(str(v).strip().lower() in ["yes", "y", "true", "t", "1", "checked", "selected"] for v in series)
            else:
                # If no explicit boolean values, count any non-empty entry as a selection
                count_val = len(series)
            if count_val > 0:
                # Use the option's label (column name without common prefix) for the category
                label = col_name
                if prefix:
                    label = col_name.replace(prefix, "").strip(" -:")
                categories.append(label)
                counts.append(count_val)
    else:
        # Single-column question
        col_name = col_list[0]
        question_text = col_name
        st.subheader(question_text)
        # Get all responses, drop empties
        series = df[col_name].dropna()
        series = series[series.astype(str).str.strip() != ""]
        if series.empty:
            st.warning(f"No responses for {question_text}")
            continue
        # Check if multiple answers are encoded in one cell (e.g., comma or semicolon separated)
        values_str = series.astype(str)
        delimiter = None
        if values_str.str.contains(';').any():
            delimiter = ';'
        elif values_str.str.contains(',').any():
            delimiter = ','
        if delimiter:
            # Split each response by the delimiter and collect all choices
            all_choices = []
            for response in values_str:
                parts = [p.strip() for p in response.split(delimiter) if p.strip() != ""]
                all_choices.extend(parts)
            count_series = pd.Series(all_choices).value_counts()
            categories = list(count_series.index)
            counts = list(count_series.values)
        else:
            # Single-choice question, just count the frequency of each answer
            count_series = values_str.value_counts()
            categories = list(count_series.index)
            counts = list(count_series.values)
    # If no categories were gathered (no data), show a warning
    if not counts:
        st.warning(f"No responses for {question_text}")
        continue
    # Filter out irrelevant long one-off responses for open-ended questions (e.g., Q15 and Q16)
    if q in [15, 16]:
        filtered = [(cat, cnt) for cat, cnt in zip(categories, counts) if not (cnt == 1 and len(str(cat)) > 30)]
        if not filtered:
            st.warning(f"No significant responses for {question_text}")
            continue
        categories, counts = zip(*filtered)
        categories = list(categories)
        counts = list(counts)
    # Sort categories by frequency (descending) for clear presentation
    sorted_items = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
    categories_sorted = [item[0] for item in sorted_items]
    counts_sorted = [item[1] for item in sorted_items]
    # Wrap category labels for better readability on the y-axis
    categories_wrapped = [wrap_label(cat) for cat in categories_sorted]
    # Create horizontal bar chart
    fig = px.bar(x=counts_sorted, y=categories_wrapped, orientation='h', text=counts_sorted)
    fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text='')
    # Ensure the bars are ordered as sorted (so highest count is at the top)
    fig.update_layout(yaxis=dict(categoryorder='array', categoryarray=categories_wrapped))
    # Adjust left margin to accommodate long labels (to prevent cutoff)
    max_label_len = max(len(str(lbl)) for lbl in categories_wrapped)
    if max_label_len > 20:
        fig.update_layout(margin=dict(l=min(300, max_label_len * 7)))
    else:
        fig.update_layout(margin=dict(l=80))
    # Display the bar chart
    st.plotly_chart(fig, use_container_width=True)
