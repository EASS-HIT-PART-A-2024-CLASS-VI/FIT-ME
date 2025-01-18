import streamlit as st
import requests

API_URL = "http://backend:8000"

def client_management_services():
    """Render the Client Management services."""
    st.header("Client Management")

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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Search Client by ID")
        search_id = st.text_input("Enter ID Number to Search")
        if st.button("Search by ID"):
            response = requests.get(f"{API_URL}/clients/id/{search_id}")
            if response.status_code == 200:
                client = response.json()
                st.markdown(f"""
                ### Client Details
                - **Name:** {client['first_name']} {client['last_name']} 👤
                - **Phone:** {client['phone_number']} 📞
                - **ID Number:** {client['id_number']} 🔑
                - **Membership:** {client['membership_type']} 🗓️
                - **Payment Method:** {client['payment_method']} 💳
                """)
            else:
                st.error("Client not found or an error occurred.")

    with col2:
        st.subheader("Search Client by Phone Number")
        search_phone = st.text_input("Enter Phone Number to Search")
        if st.button("Search by Phone"):
            response = requests.get(f"{API_URL}/clients/phone/{search_phone}")
            if response.status_code == 200:
                client = response.json()
                st.markdown(f"""
                ### Client Details
                - **Name:** {client['first_name']} {client['last_name']} 👤
                - **Phone:** {client['phone_number']} 📞
                - **ID Number:** {client['id_number']} 🔑
                - **Membership:** {client['membership_type']} 🗓️
                - **Payment Method:** {client['payment_method']} 💳
                """)
            else:
                st.error("Client not found or an error occurred.")

    col3, col4 = st.columns(2)

    col3, col4 = st.columns(2)


    with col3:
        st.subheader("Move Client to Past Clients")
        past_phone_number = st.text_input("Enter Phone Number to Move")
        past_id_number = st.text_input("Enter ID Number to Move")
        if st.button("Move to Past Clients"):
            response = requests.post(
                f"{API_URL}/clients/move_to_past/",
                params={
                     "phone_number": past_phone_number,
                     "id_number": past_id_number,
                }
            )
            if response.status_code == 200:
                st.success("Client moved to past clients successfully!")
            else:
                st.error(f"Error: {response.text}")

    with col4:
        st.subheader("Past Customer Archive")
        search_past_phone = st.text_input("Enter Phone Number to Search Past Customer")
        if st.button("Search Past Customer"):
            response = requests.get(f"{API_URL}/past_clients/")
            if response.status_code == 200:
                past_clients = response.json()
                found = False
                for client in past_clients:
                    if client["phone_number"] == search_past_phone:
                        st.markdown(f"""
                        ### Past Client Details
                        - **Name:** {client['first_name']} {client['last_name']} 🧑‍💼
                        - **Phone:** {client['phone_number']} 📞
                        - **ID Number:** {client['id_number']} 🔑
                        - **Membership:** {client['membership_type']} 🗓️
                        - **Payment Method:** {client['payment_method']} 💳
                        """)
                        found = True
                        break
                if not found:
                    st.warning("Past customer not found.")
            else:
                st.error(f"Error: {response.text}")



