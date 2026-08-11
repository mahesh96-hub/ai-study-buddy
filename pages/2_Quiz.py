import json
from datetime import datetime

import streamlit as st

from core.db import get_connection, add_attempt
from core.ai_engine import evaluate_answer


st.title("📝 Quiz")

st.write("Answer the questions below and submit your quiz.")


def get_questions():
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
        ORDER BY question_id
        """
    ).fetchall()

    connection.close()

    return rows


questions = get_questions()


if not questions:

    st.info(
        "No quiz questions are available yet. "
        "Go to Study Material and generate a quiz first."
    )

else:

    st.write(f"### {len(questions)} Questions")

    with st.form("quiz_form"):

        for index, question in enumerate(questions, start=1):

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
                    key=f"answer_{question_id}"
                )

            elif question_type == "TrueFalse":

                options = json.loads(options_json)

                st.radio(
                    "Select your answer:",
                    options,
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

        with st.spinner("Evaluating your answers..."):

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
                add_attempt(
                    question_id=question_id,
                    user_answer=user_answer,
                    score=score,
                    feedback=feedback
                )
                total_score += score

                results.append(
                    {
                        "question_id": question_id,
                        "question_number": len(results) + 1,
                        "question_type": question_type,
                        "score": score,
                        "feedback": feedback,
                        "correct_answer": correct_answer
                    }
                )

        final_percentage = (
            total_score / len(questions)
        ) * 100

        st.divider()

        st.subheader("📊 Quiz Result")

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