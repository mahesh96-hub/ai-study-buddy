import streamlit as st


def is_authenticated():
    return st.user.is_logged_in


def get_user_id():
    if not is_authenticated():
        return None

    return st.user.get("sub")


def get_user_name():
    if not is_authenticated():
        return None

    return st.user.get("name", "Student")


def login():
    st.login()


def logout():
    st.logout()
    