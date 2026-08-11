import streamlit as st
from core.db import init_db

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)

init_db()

st.title("📚 AI Study Buddy")
st.subheader("AI-powered learning with spaced repetition")

st.write(
    "Upload your study material, generate quizzes, "
    "review difficult questions, and track your progress."
)