import json
from datetime import date

import streamlit as st

from core.db import (
    get_connection,
    add_attempt,
    update_question_review
)
from core.ai_engine import evaluate_answer
from core.scheduler import calculate_next_review


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

    with st.form("review_form"):

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

            if question_type == "MCQ":

                options = json.loads(options_json)

                st.radio(
                    "Select your answer:",
                    options,
                    key=f"review_answer_{question_id}"
                )

            elif question_type == "TrueFalse":

                options = json.loads(options_json)

                st.radio(
                    "Select your answer:",
                    options,
                    key=f"review_answer_{question_id}"
                )

            elif question_type == "ShortAnswer":

                st.text_area(
                    "Your answer:",
                    key=f"review_answer_{question_id}"
                )

            st.divider()

        submitted = st.form_submit_button(
            "Submit Review"
        )


    if submitted:

        total_score = 0.0
        results = []

        with st.spinner("Evaluating your review..."):

            for question in due_questions:

                (
                    question_id,
                    topic,
                    question_type,
                    question_text,
                    options_json,
                    correct_answer,
                    next_review_date
                ) = question

                user_answer = st.session_state.get(
                    f"review_answer_{question_id}",
                    ""
                )

                score = 0.0
                feedback = ""

                if question_type in ["MCQ", "TrueFalse"]:

                    if user_answer == correct_answer:

                        score = 1.0
                        feedback = "Correct answer."

                    else:

                        score = 0.0
                        feedback = (
                            f"Correct answer: {correct_answer}"
                        )

                elif question_type == "ShortAnswer":

                    if user_answer.strip():

                        evaluation = evaluate_answer(
                            question_text=question_text,
                            correct_answer=correct_answer,
                            student_answer=user_answer
                        )

                        score = evaluation.score
                        feedback = evaluation.feedback

                    else:

                        score = 0.0
                        feedback = "No answer provided."

                new_review_date = calculate_next_review(
                    score
                )

                add_attempt(
                    question_id=question_id,
                    user_answer=user_answer,
                    score=score,
                    feedback=feedback
                )

                update_question_review(
                    question_id=question_id,
                    score=score,
                    next_review_date=new_review_date
                )

                total_score += score

                results.append(
                    {
                        "question_number": len(results) + 1,
                        "score": score,
                        "feedback": feedback,
                        "correct_answer": correct_answer,
                        "next_review_date": new_review_date
                    }
                )

        final_percentage = (
            total_score / len(due_questions)
        ) * 100

        st.divider()

        st.subheader("📊 Review Result")

        st.metric(
            "Review Score",
            f"{final_percentage:.0f}%"
        )

        for result in results:

            st.markdown(
                f"### Question {result['question_number']}"
            )

            if result["score"] == 1.0:

                st.success(
                    f"Correct ✅ — Score: {result['score']}"
                )

            elif result["score"] == 0.5:

                st.warning(
                    f"Partially Correct ⚠️ — "
                    f"Score: {result['score']}"
                )

            else:

                st.error(
                    f"Wrong ❌ — Score: {result['score']}"
                )

            st.write(result["feedback"])

            if result["score"] < 1.0:

                st.write(
                    f"Correct answer: "
                    f"**{result['correct_answer']}**"
                )

            st.write(
                f"📅 Next review: "
                f"**{result['next_review_date']}**"
            )