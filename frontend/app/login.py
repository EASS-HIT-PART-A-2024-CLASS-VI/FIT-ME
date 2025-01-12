import streamlit as st
import base64
import os
import requests
from app.dashboard import dashboard_page  # Import the dashboard page function

# URL of the backend API
API_URL = "http://backend:8000"

def add_background():
    """Set the background image for the page."""
    image_path = "/app/app/assets/LoginPhoto.jpg"
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



def login_page():
    """Render the login page."""
    # Add the background
    add_background()
    # Title for the login page
    st.markdown(
        "<h1 style='text-align: center; color: white;'>Login to Fit-Me Manage Gym System</h1>",
        unsafe_allow_html=True
    )

    # Use session state to manage username and password
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "password" not in st.session_state:
        st.session_state["password"] = ""

    # Input fields for username and password
    st.session_state["username"] = st.text_input("Username", key=f"login_username_{id(st.session_state)}")
    st.session_state["password"] = st.text_input("Password", type="password", key=f"login_password_{id(st.session_state)}")

    if st.button("Login", key=f"login_button_{id(st.session_state)}"):
        if st.session_state["username"] and st.session_state["password"]:
            # Send login request to the backend
            response = requests.post(f"{API_URL}/login/", json={
                "username": st.session_state["username"],
                "password": st.session_state["password"]
            })
            if response.status_code == 200:
                st.session_state["logged_in"] = True
                st.success("Login successful! Redirecting...")
                st.session_state["current_page"] = "dashboard"
            else:
                st.error("Invalid username or password")
        else:
            st.warning("Please enter both username and password.")

