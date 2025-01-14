import streamlit as st
import requests

API_URL = "http://backend:8000"

def add_interested_client_page():
    """Page to add a new interested client."""
    st.title("Add an Interested Client")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    phone_number = st.text_input("Phone Number")

    if st.button("Add Interested Client"):
        if first_name and last_name and phone_number:
            response = requests.post(f"{API_URL}/interested_clients/", json={
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number
            })

            if response.status_code == 200:
                st.success("Interested client added successfully!")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please fill in all fields.")
