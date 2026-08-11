import streamlit as st
import fitz

from core.pdf_processor import extract_text_from_pdf
from core.db import add_material, add_question
from core.ai_engine import generate_questions
from core.auth import get_user_id


st.title("📄 Study Material")

st.write(
    "Upload one or more PDF study materials to generate "
    "AI-powered quizzes."
)


user_id = get_user_id()


def get_question_count(page_count):
    if page_count <= 9:
        return 5

    if page_count <= 20:
        return 15

    if page_count <= 50:
        return 25

    return 35


uploaded_files = st.file_uploader(
    "Choose your study material PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(
        f"{len(uploaded_files)} PDF(s) selected."
    )

    st.subheader("📚 Selected Materials")

    file_information = []

    for uploaded_file in uploaded_files:

        try:

            pdf_document = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )

            page_count = pdf_document.page_count

            pdf_document.close()

            question_count = get_question_count(
                page_count
            )

            file_information.append(
                (
                    uploaded_file,
                    page_count,
                    question_count
                )
            )

            st.write(
                f"**{uploaded_file.name}** — "
                f"{page_count} pages → "
                f"**{question_count} questions**"
            )

        except Exception as error:

            st.error(
                f"Could not read {uploaded_file.name}: "
                f"{error}"
            )


    st.divider()


    if st.button(
        "🚀 Extract & Generate Quizzes",
        type="primary"
    ):

        total_materials = len(file_information)
        successful_materials = 0
        total_questions_created = 0

        progress_bar = st.progress(0)

        status_text = st.empty()


        for index, (
            uploaded_file,
            page_count,
            question_count
        ) in enumerate(
            file_information,
            start=1
        ):

            status_text.write(
                f"Processing {index}/{total_materials}: "
                f"**{uploaded_file.name}**"
            )


            try:

                with st.spinner(
                    f"Extracting text from "
                    f"{uploaded_file.name}..."
                ):

                    extracted_text = extract_text_from_pdf(
                        uploaded_file
                    )


                if not extracted_text.strip():

                    st.warning(
                        f"No readable text was found in "
                        f"**{uploaded_file.name}**. "
                        f"This PDF was skipped."
                    )

                    progress_bar.progress(
                        index / total_materials
                    )

                    continue


                st.success(
                    f"Text extracted from "
                    f"**{uploaded_file.name}**."
                )


                material_id = add_material(
                    filename=uploaded_file.name,
                    user_id=user_id
                )


                st.session_state[
                    f"material_id_{material_id}"
                ] = material_id


                st.info(
                    f"Generating {question_count} "
                    f"questions for "
                    f"**{uploaded_file.name}**..."
                )


                question_list = generate_questions(
                    extracted_text,
                    number_of_questions=question_count
                )


                questions_created = 0


                for question in question_list.questions:

                    add_question(
                        material_id=material_id,
                        topic=question.topic,
                        question_type=question.question_type,
                        question_text=question.question_text,
                        options=question.options,
                        correct_answer=question.correct_answer
                    )

                    questions_created += 1


                successful_materials += 1

                total_questions_created += (
                    questions_created
                )


                st.success(
                    f"✅ {uploaded_file.name}: "
                    f"{questions_created} questions created."
                )


                with st.expander(
                    f"Preview: {uploaded_file.name}"
                ):

                    st.write(
                        f"Pages: **{page_count}**"
                    )

                    st.write(
                        f"Questions requested: "
                        f"**{question_count}**"
                    )

                    st.write(
                        f"Questions generated: "
                        f"**{questions_created}**"
                    )

                    st.text_area(
                        "Extracted Text",
                        extracted_text,
                        height=300,
                        key=f"text_preview_{material_id}"
                    )


            except Exception as error:

                st.error(
                    f"❌ Failed to process "
                    f"**{uploaded_file.name}**: {error}"
                )


            progress_bar.progress(
                index / total_materials
            )


        status_text.empty()


        st.divider()


        if successful_materials > 0:

            st.success(
                f"🎉 Successfully processed "
                f"{successful_materials} "
                f"material(s) and generated "
                f"{total_questions_created} "
                f"question(s) in total."
            )

            st.session_state[
                "quiz_generated"
            ] = True


        else:

            st.error(
                "No materials were successfully processed."
            )