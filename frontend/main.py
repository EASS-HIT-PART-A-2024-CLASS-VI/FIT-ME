import streamlit as st
from app.dashboard import dashboard_page
from app.login import login_page

def main():
    """Main application flow."""
    # Initialize session state variables
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Handle page transitions
    if st.session_state["current_page"] == "login":
        login_page()
    elif st.session_state["current_page"] == "dashboard":
        dashboard_page()
    else:
        st.error("Page not implemented yet.")

if __name__ == "__main__":
    main()

