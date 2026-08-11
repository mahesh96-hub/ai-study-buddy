import streamlit as st

from core.db import init_db
from core.auth import is_authenticated, login, get_user_name


st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)


init_db()


def login_page():
    st.title("📚 AI Study Buddy")

    st.subheader(
        "AI-powered learning with spaced repetition"
    )

    st.write(
        "Upload your study material, generate quizzes, "
        "review difficult questions, and track your progress."
    )

    st.info(
        "Please sign in with Google to continue."
    )

    st.button(
        "🔐 Sign in with Google",
        on_click=login
    )


if not is_authenticated():

    pg = st.navigation(
        [
            st.Page(
                login_page,
                title="Login",
                icon="🔐"
            )
        ],
        position="hidden"
    )

    pg.run()

    st.stop()


st.sidebar.success(
    f"Signed in as {get_user_name()}"
)


if st.sidebar.button("🚪 Logout"):
    st.logout()


study_material_page = st.Page(
    "pages/1_Home.py",
    title="Study Material",
    icon="📄"
)


quiz_page = st.Page(
    "pages/2_Quiz.py",
    title="Quiz",
    icon="📝"
)


review_page = st.Page(
    "pages/3_Review.py",
    title="Review",
    icon="🔄"
)


dashboard_page = st.Page(
    "pages/4_Dashboard.py",
    title="Dashboard",
    icon="📊"
)


pg = st.navigation(
    {
        "AI Study Buddy": [
            study_material_page,
            quiz_page,
            review_page,
            dashboard_page
        ]
    },
    position="sidebar"
)


pg.run()