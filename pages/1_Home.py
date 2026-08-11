import streamlit as st

from core.pdf_processor import extract_text_from_pdf


st.title("📄 Study Material")

st.write("Upload your study material PDF to get started.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract Text"):
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text.strip():
            st.success("Text extracted successfully!")

            with st.expander("Preview extracted text"):
                st.text_area(
                    "Extracted Text",
                    extracted_text,
                    height=400
                )
        else:
            st.warning(
                "No readable text was found in this PDF. "
                "Please upload a text-based PDF."
            )