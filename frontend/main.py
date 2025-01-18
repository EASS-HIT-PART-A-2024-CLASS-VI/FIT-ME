import streamlit as st
import base64

st.set_page_config(
    page_title="Fit-Me System",
    layout="wide"
)

from app.dashboard import dashboard_page
from app.login import login_page
from app.dashboard_services.client_management import client_management_services
from app.dashboard_services.add_interested_client import add_interested_client_page
from app.dashboard_services.task_management import task_management_page
from app.dashboard_services.group_lessons import group_lessons_page
from app.dashboard_services.personal_trainings import personal_trainings_page
from app.dashboard_services.gym_staff import gym_staff_page

def add_background():
    """Set the background image for the page."""
    image_path = "app/assets/BackgroundSystem.jpg"
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh; /* Set height to full viewport */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    """Main application flow."""
    # Initialize session state variables
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "current_page" in st.session_state and st.session_state["current_page"] != "login":
        add_background()

    # Handle page transitions
    if st.session_state["current_page"] == "login":
        login_page()
    elif st.session_state["current_page"] == "dashboard":
        dashboard_page()
    elif st.session_state["current_page"] == "client_management":
        client_management_services()
    elif st.session_state["current_page"] == "add_interested_client":
        add_interested_client_page()
    elif st.session_state["current_page"] == "task_management":
        task_management_page()
    elif st.session_state["current_page"] == "group_lessons":
        group_lessons_page()
    elif st.session_state["current_page"] == "personal_trainings":
        personal_trainings_page()
    elif st.session_state["current_page"] == "gym_staff":
        gym_staff_page()
    else:
        st.error("Page not implemented yet.")

if __name__ == "__main__":
    main()

