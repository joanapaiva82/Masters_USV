import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import textwrap

# Configure page layout for a wide display
st.set_page_config(layout="wide")
st.title("USV Survey Results Dashboard")

# Load the cleaned survey data
df = pd.read_csv("usv_survey_data.csv")

# If needed, find the first question column (starting at Q5) and skip any initial metadata columns
start_index = 0
for idx, col in enumerate(df.columns):
    col_name = str(col).strip().lower()
    if col_name.startswith("q5"):
        start_index = idx
        break
df_questions = df.iloc[:, start_index:]

# Helper function to wrap long labels for better display on charts
def wrap_label(label, width=30):
    """Wrap text label to multiple lines at the given width."""
    return "<br>".join(textwrap.wrap(str(label), width)) if len(str(label)) > width else str(label)

# Loop through each question column and generate the appropriate visualization
for col in df_questions.columns:
    question_text = str(col).strip()  # exact text of the question from CSV header
    st.subheader(question_text)       # display question as section title (e.g., "Q5. ...question text...")

    # Get all responses for this question, ignoring blank responses
    responses = df_questions[col].dropna()
    responses = responses[responses.astype(str).str.strip() != ""]  # drop empty strings
    if responses.empty:
        st.write("_No responses for this question._")
        continue

    # Determine if this question allows multiple selections by checking for delimiter
    multi_select = any(';' in str(x) for x in responses)
    if multi_select:
        # **Multiple-choice (multi-select)**: split the selections and count each option
        counts = Counter()
        total_respondents = len(responses)  # total people who answered this question
        for ans in responses:
            choices = [c.strip() for c in str(ans).split(';') if c.strip()]
            for choice in choices:
                counts[choice] += 1

        # Group all "Other..." responses into one category
        other_count = 0
        other_texts = []
        new_counts = {}
        for option, cnt in counts.items():
            opt_lower = option.lower()
            if opt_lower.startswith("other"):
                other_count += cnt
                # Extract the free-text detail after "Other:" (if any)
                if ":" in option:
                    detail = option.split(":", 1)[1].strip()
                    if detail:
                        other_texts.append(detail)
            else:
                new_counts[option] = cnt
        if other_count > 0:
            new_counts["Other"] = other_count

        # Prepare data for chart
        sorted_options = sorted(new_counts.items(), key=lambda x: x[1], reverse=True)
        categories = [opt for opt, cnt in sorted_options]
        values = [cnt for opt, cnt in sorted_options]
        percents = [(cnt / total_respondents * 100) for cnt in values]
        # Wrap category labels to avoid long text overflow
        categories_wrapped = [wrap_label(opt) for opt in categories]

        # Create a horizontal bar chart with counts and percentages
        fig = px.bar(x=values, y=categories_wrapped, orientation='h',
                     text=[f"{cnt} ({pct:.1f}%)" for cnt, pct in zip(values, percents)],
                     labels={"x": "Responses", "y": ""})
        fig.update_traces(textposition='outside')  # label at end of bar
        fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(l=20, r=20, t=20, b=40))
        fig.update_yaxes(automargin=True)         # allow more margin for long labels
        st.plotly_chart(fig, use_container_width=True)

        # If there were Other responses, list the actual texts below the chart
        if other_texts:
            st.markdown("**Other responses (verbatim):**")
            for text in other_texts:
                st.write(f"- {text}")

    else:
        # **Single-selection or Free-text question**
        counts = Counter(responses.astype(str).map(lambda x: x.strip()))
        total_responses = sum(counts.values())
        num_unique = len(counts)

        # Decide how to display: chart vs table, based on uniqueness of answers
        if num_unique < total_responses and num_unique < 0.9 * total_responses:
            # There are some duplicate answers (not all answers are unique)
            if num_unique <= 15:
                # **Fixed options or few common answers**: use a donut chart
                other_count = 0
                other_texts = []
                new_counts = {}
                for answer, cnt in counts.items():
                    ans_lower = str(answer).lower()
                    if ans_lower.startswith("other"):
                        other_count += cnt
                        if ":" in str(answer):
                            detail = str(answer).split(":", 1)[1].strip()
                            if detail:
                                other_texts.append(detail)
                    else:
                        new_counts[answer] = cnt
                if other_count > 0:
                    new_counts["Other"] = other_count

                # Prepare data for donut chart
                sorted_answers = sorted(new_counts.items(), key=lambda x: x[1], reverse=True)
                categories = [ans for ans, cnt in sorted_answers]
                values = [cnt for ans, cnt in sorted_answers]
                percents = [(cnt / total_responses * 100) for cnt in values]

                if len(categories) == 1:
                    # If only one unique answer (everyone gave the same answer)
                    only_answer = categories[0]
                    st.write(f"**{only_answer}** – {values[0]} responses (100%)")
                else:
                    # Donut chart for distribution of answers
                    fig = px.pie(values=values, names=categories, hole=0.4)
                    fig.update_traces(textinfo='none',
                                      texttemplate='%{percent:.1%} (%{value})',
                                      textfont_size=14)  # show percentage and count on slices
                    fig.update_layout(showlegend=True, legend_title_text='', margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                # List out Other texts if any were grouped
                if other_texts:
                    st.markdown("**Other responses (verbatim):**")
                    for text in other_texts:
                        st.write(f"- {text}")
            else:
                # **Many unique answers but some repeats**: show all as a horizontal bar chart
                sorted_answers = sorted(counts.items(), key=lambda x: x[1], reverse=True)
                categories = [ans for ans, cnt in sorted_answers]
                values = [cnt for ans, cnt in sorted_answers]
                percents = [(cnt / total_responses * 100) for cnt in values]
                categories_wrapped = [wrap_label(ans) for ans in categories]

                fig = px.bar(x=values, y=categories_wrapped, orientation='h',
                             text=[f"{cnt} ({pct:.1f}%)" for cnt, pct in zip(values, percents)],
                             labels={"x": "Responses", "y": ""})
                fig.update_traces(textposition='outside')
                fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(l=20, r=20, t=20, b=40))
                fig.update_yaxes(automargin=True)
                st.plotly_chart(fig, use_container_width=True)
        else:
            # **All answers unique (open-ended)**: display each response in a list
            st.markdown("**Individual responses:**")
            for answer in responses:
                st.write(f"- {answer}")
