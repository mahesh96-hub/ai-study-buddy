from datetime import date

import streamlit as st

from core.db import get_connection
from core.auth import get_user_id


st.title("📊 Dashboard")

st.write(
    "Track your study progress and performance."
)


user_id = get_user_id()


def get_dashboard_data(user_id):

    connection = get_connection()


    total_questions = connection.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
        """,
        (user_id,)
    ).fetchone()[0]


    total_attempts = connection.execute(
        """
        SELECT COUNT(*)
        FROM attempts a
        INNER JOIN questions q
            ON a.question_id = q.question_id
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
        """,
        (user_id,)
    ).fetchone()[0]


    average_score = connection.execute(
        """
        SELECT AVG(a.score)
        FROM attempts a
        INNER JOIN questions q
            ON a.question_id = q.question_id
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
        """,
        (user_id,)
    ).fetchone()[0]


    due_today = connection.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
          AND q.next_review_date <= ?
        """,
        (
            user_id,
            date.today().isoformat()
        )
    ).fetchone()[0]


    mastered_questions = connection.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
          AND q.last_score = 1.0
        """,
        (user_id,)
    ).fetchone()[0]


    needs_improvement = connection.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
          AND q.last_score < 1.0
        """,
        (user_id,)
    ).fetchone()[0]


    correct_attempts = connection.execute(
        """
        SELECT COUNT(*)
        FROM attempts a
        INNER JOIN questions q
            ON a.question_id = q.question_id
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
          AND a.score = 1.0
        """,
        (user_id,)
    ).fetchone()[0]


    upcoming_reviews = connection.execute(
        """
        SELECT
            q.next_review_date,
            COUNT(*) AS question_count
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
          AND q.next_review_date > ?
        GROUP BY q.next_review_date
        ORDER BY q.next_review_date ASC
        LIMIT 7
        """,
        (
            user_id,
            date.today().isoformat()
        )
    ).fetchall()


    total_materials = connection.execute(
        """
        SELECT COUNT(*)
        FROM materials
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()[0]


    connection.close()


    return (
        total_questions,
        total_attempts,
        average_score,
        due_today,
        mastered_questions,
        needs_improvement,
        correct_attempts,
        upcoming_reviews,
        total_materials
    )


(
    total_questions,
    total_attempts,
    average_score,
    due_today,
    mastered_questions,
    needs_improvement,
    correct_attempts,
    upcoming_reviews,
    total_materials
) = get_dashboard_data(user_id)


if average_score is None:

    average_score = 0.0


overall_accuracy = 0.0


if total_attempts > 0:

    overall_accuracy = (
        correct_attempts /
        total_attempts
    ) * 100


st.subheader("📚 Your Study Materials")


st.metric(
    "Total Materials",
    total_materials
)


st.divider()


st.subheader("📊 Quiz Statistics")


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
        f"📚 You have {due_today} "
        f"question(s) due for review today."
    )

else:

    st.success(
        "🎉 You have no questions due "
        "for review today."
    )


st.subheader("📈 Study Progress")


progress_col1, progress_col2, progress_col3 = (
    st.columns(3)
)


with progress_col1:

    st.metric(
        "Questions Mastered",
        mastered_questions
    )


with progress_col2:

    st.metric(
        "Needs Improvement",
        needs_improvement
    )


with progress_col3:

    st.metric(
        "Overall Accuracy",
        f"{overall_accuracy:.0f}%"
    )


st.divider()


st.subheader("📅 Upcoming Reviews")


if upcoming_reviews:

    for review_date, question_count in (
        upcoming_reviews
    ):

        st.write(
            f"**{review_date}** — "
            f"{question_count} question(s)"
        )

else:

    st.info(
        "No upcoming reviews scheduled."
    )