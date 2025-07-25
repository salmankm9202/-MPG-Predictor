import streamlit as st
import hashlib

# Simple username-password store (for production use a real DB)
users = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin"
    },
    "user": {
        "password": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user"
    }
}


def authenticate():
    """Basic Streamlit login form"""
    with st.sidebar:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if (username in users and
                    users[username]["password"] == hashlib.sha256(password.encode()).hexdigest()):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    return st.session_state["authenticated"], st.session_state.get("username", "")