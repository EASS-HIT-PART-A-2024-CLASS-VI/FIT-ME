import streamlit as st
import base64
import os
import requests
from app.dashboard import dashboard_page

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
            height: 100vh;
        }}
        .input-container {{
            width: 300px;
            margin: 0 auto 15px auto;
            text-align: left;
        }}

        .label {{
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 5px;
        }}
        .stTextInput > div {{
            width: 100%; /* התאמה לרוחב הקונטיינר */
        }}
        .stButton > button {{
            margin: 20px auto;
            display: block;
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

    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    st.markdown("<label class='label'>Username</label>", unsafe_allow_html=True)
    username = st.text_input(
        "Username",
        label_visibility="collapsed",
        key="login_username"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    st.markdown("<label class='label'>Password</label>", unsafe_allow_html=True)
    password = st.text_input(
        "Password",
        label_visibility="collapsed",
        type="password",
        key="login_password"
    )
    st.markdown("</div>", unsafe_allow_html=True)
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
