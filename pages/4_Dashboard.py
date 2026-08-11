from datetime import date

import streamlit as st

from core.db import get_connection


st.title("📊 Dashboard")

st.write("Track your study progress and performance.")


def get_dashboard_data():
    connection = get_connection()

    total_questions = connection.execute(
        "SELECT COUNT(*) FROM questions"
    ).fetchone()[0]

    total_attempts = connection.execute(
        "SELECT COUNT(*) FROM attempts"
    ).fetchone()[0]

    average_score = connection.execute(
        "SELECT AVG(score) FROM attempts"
    ).fetchone()[0]

    due_today = connection.execute(
        """
        SELECT COUNT(*)
        FROM questions
        WHERE next_review_date <= ?
        """,
        (date.today().isoformat(),)
    ).fetchone()[0]

    connection.close()

    return (
        total_questions,
        total_attempts,
        average_score,
        due_today
    )


(
    total_questions,
    total_attempts,
    average_score,
    due_today
) = get_dashboard_data()


if average_score is None:
    average_score = 0.0


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Questions",
        total_questions
    )


with col2:
    st.metric(
        "Total Attempts",
        total_attempts
    )


with col3:
    st.metric(
        "Average Score",
        f"{average_score * 100:.0f}%"
    )


with col4:
    st.metric(
        "Due Today",
        due_today
    )


st.divider()

if due_today > 0:

    st.warning(
        f"📚 You have {due_today} question(s) "
        "due for review today."
    )

else:

    st.success(
        "🎉 You have no questions due for review today."
    )