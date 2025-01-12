import streamlit as st
import requests

API_URL = "http://backend:8000"

def client_management_services():
    """Render the Client Management services."""
    st.header("Client Management")

    # Button 1: Register New Client
    st.subheader("Register New Client")
    first_name = st.text_input("First Name", key="dashboard_first_name")
    last_name = st.text_input("Last Name", key="dashboard_last_name")
    phone_number = st.text_input("Phone Number", key="dashboard_phone_number")
    id_number = st.text_input("ID Number", key="dashboard_id_number")
    membership_type = st.selectbox("Membership Type", ["monthly", "quarterly", "yearly"], key="dashboard_membership_type")
    payment_method = st.selectbox("Payment Method", ["credit card", "cash"], key="dashboard_payment_method")
    if st.button("Register Client", key="dashboard_register_client"):
        response = requests.post(f"{API_URL}/clients/", json={
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "id_number": id_number,
            "membership_type": membership_type,
            "payment_method": payment_method
        })
        if response.status_code == 200:
            st.success("Client registered successfully!")
        else:
            st.error(f"Error: {response.text}")

    # Button 2: Search Client by ID
    st.subheader("Search Client by ID")
    search_id = st.text_input("Enter ID Number to Search")
    if st.button("Search by ID"):
        response = requests.get(f"{API_URL}/clients/id/{search_id}")
        if response.status_code == 200:
            client = response.json()
            st.json(client)
        else:
            st.error("Client not found or an error occurred.")

    # Button 3: Search Client by Phone Number
    st.subheader("Search Client by Phone Number")
    search_phone = st.text_input("Enter Phone Number to Search")
    if st.button("Search by Phone"):
        response = requests.get(f"{API_URL}/clients/phone/{search_phone}")
        if response.status_code == 200:
            client = response.json()
            st.json(client)
        else:
            st.error("Client not found or an error occurred.")
