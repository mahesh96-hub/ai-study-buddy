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
from core.auth import get_user_id


st.title("🔄 Review")

st.write(
    "Review questions that are due based on your "
    "spaced-repetition schedule."
)


user_id = get_user_id()


def get_due_questions(user_id):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            q.question_id,
            q.topic,
            q.question_type,
            q.question_text,
            q.options_json,
            q.correct_answer,
            q.next_review_date,
            m.filename
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE m.user_id = ?
          AND q.next_review_date <= ?
        ORDER BY q.next_review_date ASC,
                 q.question_id ASC
        """,
        (
            user_id,
            date.today().isoformat()
        )
    ).fetchall()

    connection.close()

    return rows


due_questions = get_due_questions(user_id)


if not due_questions:

    st.success(
        "🎉 No questions are due for review today!"
    )

else:

    st.write(
        f"### {len(due_questions)} "
        f"question(s) due for review"
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
                next_review_date,
                filename
            ) = question


            st.markdown(
                f"### Question {index}"
            )

            st.caption(
                f"Material: {filename} | "
                f"Topic: {topic} | "
                f"Type: {question_type}"
            )

            st.write(question_text)


            if question_type == "MCQ":

                options = json.loads(
                    options_json
                )

                st.radio(
                    "Select your answer:",
                    options,
                    index=None,
                    key=f"review_answer_{question_id}"
                )


            elif question_type == "TrueFalse":

                options = json.loads(
                    options_json
                )

                st.radio(
                    "Select your answer:",
                    options,
                    index=None,
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

        unanswered = 0


        with st.spinner(
            "Evaluating your review..."
        ):

            for question in due_questions:

                (
                    question_id,
                    topic,
                    question_type,
                    question_text,
                    options_json,
                    correct_answer,
                    next_review_date,
                    filename
                ) = question


                user_answer = st.session_state.get(
                    f"review_answer_{question_id}",
                    ""
                )


                if user_answer is None:

                    user_answer = ""


                score = 0.0

                feedback = ""


                if not str(user_answer).strip():

                    unanswered += 1

                    score = 0.0

                    feedback = (
                        "No answer provided."
                    )


                elif question_type in [
                    "MCQ",
                    "TrueFalse"
                ]:

                    if user_answer == correct_answer:

                        score = 1.0

                        feedback = (
                            "Correct answer."
                        )

                    else:

                        score = 0.0

                        feedback = (
                            f"Correct answer: "
                            f"{correct_answer}"
                        )


                elif question_type == "ShortAnswer":

                    evaluation = evaluate_answer(
                        question_text=question_text,
                        correct_answer=correct_answer,
                        student_answer=user_answer
                    )

                    score = evaluation.score

                    feedback = evaluation.feedback


                new_review_date = (
                    calculate_next_review(score)
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


        if unanswered > 0:

            st.warning(
                f"You left {unanswered} "
                f"question(s) unanswered."
            )


        st.metric(
            "Review Score",
            f"{final_percentage:.0f}%"
        )


        for result in results:

            st.markdown(
                f"### Question "
                f"{result['question_number']}"
            )


            if result["score"] == 1.0:

                st.success(
                    f"Correct ✅ — "
                    f"Score: {result['score']}"
                )

            elif result["score"] == 0.5:

                st.warning(
                    f"Partially Correct ⚠️ — "
                    f"Score: {result['score']}"
                )

            else:

                st.error(
                    f"Wrong ❌ — "
                    f"Score: {result['score']}"
                )


            st.write(
                result["feedback"]
            )


            if result["score"] < 1.0:

                st.write(
                    f"Correct answer: "
                    f"**{result['correct_answer']}**"
                )


            st.write(
                f"📅 Next review: "
                f"**{result['next_review_date']}**"
            )