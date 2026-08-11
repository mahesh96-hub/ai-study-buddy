import streamlit as st

from core.pdf_processor import extract_text_from_pdf
from core.db import add_material, add_question
from core.ai_engine import generate_questions


st.title("📄 Study Material")

st.write("Upload your study material PDF to get started.")


uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract & Generate Quiz"):

        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        if not extracted_text.strip():

            st.warning(
                "No readable text was found in this PDF. "
                "Please upload a text-based PDF."
            )

        else:

            st.success("Text extracted successfully!")

            material_id = add_material(uploaded_file.name)

            st.session_state["material_id"] = material_id
            st.session_state["study_text"] = extracted_text
            st.session_state["material_filename"] = uploaded_file.name

            st.info("Generating quiz questions with Gemini...")

            try:

                question_list = generate_questions(
                    extracted_text,
                    number_of_questions=5
                )

                for question in question_list.questions:

                    add_question(
                        material_id=material_id,
                        topic=question.topic,
                        question_type=question.question_type,
                        question_text=question.question_text,
                        options=question.options,
                        correct_answer=question.correct_answer
                    )

                st.success(
                    f"Quiz generated successfully! "
                    f"{len(question_list.questions)} questions created."
                )

                st.session_state["quiz_generated"] = True

            except Exception as error:

                st.error(
                    f"Failed to generate quiz questions: {error}"
                )

            with st.expander("Preview extracted text"):

                st.text_area(
                    "Extracted Text",
                    extracted_text,
                    height=400
                )