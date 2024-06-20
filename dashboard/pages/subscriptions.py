"""A dashboard page that lets you sign up for notifications."""

import streamlit as st

if __name__ == "__main__":

    st.page_link("./main.py", label="Home")

    email = ""
    age = ""

    with st.form("notification-subscription", clear_on_submit=True, border=True):
        st.header("Subscribe to notifications")
        email = st.text_input("Email")
        if email and "@" not in email:
            st.error("Terrible input")
        age = st.number_input("Age", step=1)
        st.form_submit_button()

    if email and age:
        st.write(email)
