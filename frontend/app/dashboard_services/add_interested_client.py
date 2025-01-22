import streamlit as st
import requests

API_URL = "http://backend:8000"

def add_interested_client_page():
    st.title("Add an Interested Client")

    st.markdown("<h4 style='font-weight: bold; color: white;'>First Name</h4>", unsafe_allow_html=True)
    first_name = st.text_input(
        "First Name",
        label_visibility="collapsed",
        key="first_name"
    )

    st.markdown("<h4 style='font-weight: bold; color: white;'>Last Name</h4>", unsafe_allow_html=True)
    last_name = st.text_input(
        "Last Name",
        label_visibility="collapsed",
        key="last_name"
    )

    st.markdown("<h4 style='font-weight: bold; color: white;'>Phone Number</h4>", unsafe_allow_html=True)
    phone_number = st.text_input(
        "Phone Number",
        label_visibility="collapsed",
        key="phone_number"
    )

    if st.button("Add Interested Client"):
        if first_name and last_name and phone_number:
            response = requests.post(
                f"{API_URL}/interested_clients/",
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone_number
                }
            )

            if response.status_code == 200:
                st.success("Interested client added successfully!")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please fill in all fields.")

