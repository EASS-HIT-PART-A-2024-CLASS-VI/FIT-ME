import streamlit as st
import base64
import os
import requests
from app.dashboard import dashboard_page

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
            height: 100vh; /* Full viewport height */
        }}
        .label {{
            font-size: 20px;  /* Set label font size */
            font-weight: bold;  /* Set label font weight */
            color: white;  /* Set label color */
            margin-bottom: 2px; /* Reduce spacing between label and input */
        }}
        .stTextInput > div {{
            margin: 0 auto; /* Center the input fields */
            width: 50%; /* Adjust input width */
        }}
        .stButton > button {{
            margin: 20px auto; /* Center the login button */
            display: block; /* Center the button */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def login_page():
    """Render the login page."""
    add_background()
    st.markdown(
        "<h1 style='text-align: center; color: white;'>Login to Fit-Me Manage Gym System</h1>",
        unsafe_allow_html=True
    )

    # Username label and input
    st.markdown("<div class='label'>Username</div>", unsafe_allow_html=True)
    username = st.text_input(
        "Username",  # תווית לא ריקה עבור נגישות
        label_visibility="collapsed",  # מחביא את התווית המובנית
        key="login_username"
    )

    # Password label and input
    st.markdown("<div class='label'>Password</div>", unsafe_allow_html=True)
    password = st.text_input(
        "Password",  # תווית לא ריקה עבור נגישות
        label_visibility="collapsed",  # מחביא את התווית המובנית
        type="password",
        key="login_password"
    )

    # Login button
    if st.button("Login", key="login_button"):
        if username and password:
            response = requests.post(f"{API_URL}/login/", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.session_state["logged_in"] = True
                st.success("Login successful! Redirecting...")
                st.session_state["current_page"] = "dashboard"
            else:
                st.error("Invalid username or password")
        else:
            st.warning("Please enter both username and password.")
