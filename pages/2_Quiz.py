import json

import streamlit as st

from core.db import (
    get_connection,
    add_attempt,
    update_question_review
)

from core.ai_engine import evaluate_answer

from core.scheduler import calculate_next_review


st.title("📝 Quiz")

st.write("Answer the questions below and submit your quiz.")


def get_latest_material_id():
    connection = get_connection()

    row = connection.execute(
        """
        SELECT material_id
        FROM materials
        ORDER BY material_id DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    if row:
        return row[0]

    return None


def get_questions(material_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            question_id,
            topic,
            question_type,
            question_text,
            options_json,
            correct_answer
        FROM questions
        WHERE material_id = ?
        ORDER BY question_id
        """,
        (material_id,)
    ).fetchall()

    connection.close()

    return rows


material_id = get_latest_material_id()


if material_id is None:

    st.info(
        "No study material is available yet. "
        "Go to Study Material and upload a PDF first."
    )

else:

    questions = get_questions(material_id)

    if not questions:

        st.info(
            "No quiz questions are available for this "
            "study material yet."
        )

    else:

        st.write(
            f"### {len(questions)} Questions"
        )

        with st.form("quiz_form"):

            for index, question in enumerate(
                questions,
                start=1
            ):

                (
                    question_id,
                    topic,
                    question_type,
                    question_text,
                    options_json,
                    correct_answer
                ) = question

                st.markdown(
                    f"**Question {index} — {topic}**"
                )

                st.write(question_text)

                if question_type == "MCQ":

                    options = json.loads(options_json)

                    st.radio(
                        "Select your answer:",
                        options,
                        index=None,
                        key=f"answer_{question_id}"
                    )

                elif question_type == "TrueFalse":

                    options = json.loads(options_json)

                    st.radio(
                        "Select your answer:",
                        options,
                        index=None,
                        key=f"answer_{question_id}"
                    )

                elif question_type == "ShortAnswer":

                    st.text_area(
                        "Your answer:",
                        key=f"answer_{question_id}"
                    )

                st.divider()

            submitted = st.form_submit_button(
                "Submit Quiz"
            )


        if submitted:

            total_score = 0.0
            results = []

            unanswered = 0

            with st.spinner(
                "Evaluating your answers..."
            ):

                for question in questions:

                    (
                        question_id,
                        topic,
                        question_type,
                        question_text,
                        options_json,
                        correct_answer
                    ) = question

                    user_answer = st.session_state.get(
                        f"answer_{question_id}",
                        ""
                    )

                    if user_answer is None:
                        user_answer = ""

                    score = 0.0
                    feedback = ""

                    if not user_answer.strip():

                        unanswered += 1

                        score = 0.0

                        feedback = "No answer provided."

                    elif question_type in [
                        "MCQ",
                        "TrueFalse"
                    ]:

                        if user_answer == correct_answer:

                            score = 1.0

                            feedback = "Correct answer."

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

                    next_review_date = calculate_next_review(
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
                        next_review_date=next_review_date
                    )

                    total_score += score

                    results.append(
                        {
                            "question_id": question_id,
                            "question_number": len(results) + 1,
                            "question_type": question_type,
                            "score": score,
                            "feedback": feedback,
                            "correct_answer": correct_answer,
                            "next_review_date": next_review_date
                        }
                    )

            final_percentage = (
                total_score / len(questions)
            ) * 100

            st.divider()

            st.subheader("📊 Quiz Result")

            if unanswered > 0:

                st.warning(
                    f"You left {unanswered} question(s) unanswered."
                )

            st.metric(
                "Final Score",
                f"{final_percentage:.0f}%"
            )

            st.write(
                f"You scored {total_score:.1f} "
                f"out of {len(questions)}."
            )

            st.divider()

            st.subheader("📋 Answer Review")

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