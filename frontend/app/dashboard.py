import streamlit as st
from app.dashboard_services.client_management import client_management_services
from app.dashboard_services.add_interested_client import add_interested_client_page
from app.dashboard_services.task_management import task_management_page
from app.dashboard_services.group_lessons import group_lessons_page
from app.dashboard_services.personal_trainings import personal_trainings_page
from app.dashboard_services.gym_staff import gym_staff_page
from app.dashboard_services.birthday_page import birthday_page
from app.dashboard_services.chatbot import chatbot_page

def dashboard_page():
    """Main dashboard page with navigation buttons."""

    st.markdown(
        """
        <style>
            .center-title {
                font-size: 65px;
                font-weight: bold;
                color: white;
                text-align: center;
                margin-bottom: 10px;
            }
            .center-subtitle {
                font-size: 32px;
                font-weight: lighter;
                color: white;
                text-align: center;
                margin-bottom: 30px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='center-title'>Fit-Me System</div>", unsafe_allow_html=True)

    st.markdown("<div class='center-subtitle'>Choose a Service</div>", unsafe_allow_html=True)

    if "dashboard_selected_service" not in st.session_state:
        st.session_state["dashboard_selected_service"] = None

    # Service buttons
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    with col1:
        if st.button("Client Management"):
            st.session_state["dashboard_selected_service"] = "client_management"
    with col2:
        if st.button("Add an Interested Client"):
            st.session_state["dashboard_selected_service"] = "add_interested_client"
    with col3:
        if st.button("Tasks Management"):
            st.session_state["dashboard_selected_service"] = "task_management"
    with col4:
        if st.button("Group Lessons"):
            st.session_state["dashboard_selected_service"] = "group_lessons"
    with col5:
        if st.button("Personal Trainings"):
            st.session_state["dashboard_selected_service"] = "personal_trainings"
    with col6:
        if st.button("Gym Staff"):
            st.session_state["dashboard_selected_service"] = "gym_staff"
    with col7:
        if st.button("Birthdays 🎂"):
            st.session_state["dashboard_selected_service"] = "birthdays"
    with col8:
        if st.button("Chat with AI 🤖"):
            st.session_state["dashboard_selected_service"] = "chatbot"

    if st.session_state["dashboard_selected_service"] is None:
        st.info("Welcome to Fit-Me System! Please select a service from the options above.")
    
    if st.session_state["dashboard_selected_service"] == "client_management":
        client_management_services()
    elif st.session_state["dashboard_selected_service"] == "add_interested_client":
        add_interested_client_page()
    elif st.session_state["dashboard_selected_service"] == "task_management":
        task_management_page()
    elif st.session_state["dashboard_selected_service"] == "group_lessons":
        group_lessons_page()
    elif st.session_state["dashboard_selected_service"] == "personal_trainings":
        personal_trainings_page()
    elif st.session_state["dashboard_selected_service"] == "gym_staff":
        gym_staff_page()
    elif st.session_state["dashboard_selected_service"] == "birthdays":
        birthday_page()
    elif st.session_state["dashboard_selected_service"] == "chatbot":
        chatbot_page()
