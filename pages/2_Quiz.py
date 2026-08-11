import json

import streamlit as st

from core.db import (
    get_connection,
    add_attempt,
    update_question_review
)

from core.ai_engine import evaluate_answer
from core.scheduler import calculate_next_review
from core.auth import get_user_id


st.title("📝 Quiz")

st.write(
    "Select a study material and take its quiz."
)


user_id = get_user_id()


def get_user_materials(user_id):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            material_id,
            filename,
            upload_date
        FROM materials
        WHERE user_id = ?
        ORDER BY material_id DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return rows


def get_questions(material_id, user_id):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            q.question_id,
            q.topic,
            q.question_type,
            q.question_text,
            q.options_json,
            q.correct_answer
        FROM questions q
        INNER JOIN materials m
            ON q.material_id = m.material_id
        WHERE q.material_id = ?
          AND m.user_id = ?
        ORDER BY q.question_id
        """,
        (
            material_id,
            user_id
        )
    ).fetchall()

    connection.close()

    return rows


materials = get_user_materials(user_id)


if not materials:

    st.info(
        "📄 You haven't uploaded any study material yet."
    )

    st.write(
        "Go to **Study Material** and upload a PDF "
        "to generate your first quiz."
    )

    st.stop()


material_options = {
    material[1]: material[0]
    for material in materials
}


selected_filename = st.selectbox(
    "📚 Select study material",
    list(material_options.keys())
)


selected_material_id = material_options[
    selected_filename
]


questions = get_questions(
    selected_material_id,
    user_id
)


if not questions:

    st.warning(
        "No questions have been generated for this "
        "study material yet."
    )

    st.stop()


st.success(
    f"{len(questions)} questions available for "
    f"**{selected_filename}**."
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
            f"### Question {index} — {topic}"
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
                key=f"answer_{question_id}"
            )


        elif question_type == "TrueFalse":

            options = json.loads(
                options_json
            )

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
                    "question_number": len(results) + 1,
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
            f"You left {unanswered} "
            f"question(s) unanswered."
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