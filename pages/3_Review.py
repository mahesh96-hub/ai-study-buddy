from datetime import date

import streamlit as st

from core.db import get_connection


st.title("🔄 Review")

st.write(
    "Review questions that are due based on your spaced-repetition schedule."
)


def get_due_questions():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            question_id,
            topic,
            question_type,
            question_text,
            options_json,
            correct_answer,
            next_review_date
        FROM questions
        WHERE next_review_date <= ?
        ORDER BY next_review_date ASC
        """,
        (date.today().isoformat(),)
    ).fetchall()

    connection.close()

    return rows


due_questions = get_due_questions()


if not due_questions:

    st.success(
        "🎉 No questions are due for review today!"
    )

else:

    st.write(
        f"### {len(due_questions)} question(s) due for review"
    )

    for index, question in enumerate(
        due_questions,
        start=1
    ):

        (
            question_id,
            topic,
            question_type,
            question_text,
            options_json,
            correct_answer,
            next_review_date
        ) = question

        st.markdown(
            f"### Question {index}"
        )

        st.caption(
            f"Topic: {topic} | Type: {question_type}"
        )

        st.write(question_text)

        st.write(
            f"📅 Due: {next_review_date}"
        )

        with st.expander("Show Answer"):

            st.success(
                f"Answer: {correct_answer}"
            )

        st.divider()