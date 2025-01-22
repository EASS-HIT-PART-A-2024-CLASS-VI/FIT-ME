import streamlit as st
import requests

API_URL = "http://backend:8000"

def client_management_services():
    """Render the Client Management services."""
    st.header("Client Management")

    st.subheader("Register New Client")
    st.markdown("<h4 style='font-weight: bold; color: white;'>First Name</h4>", unsafe_allow_html=True)
    first_name = st.text_input("First Name", label_visibility="collapsed", key="dashboard_first_name")

    st.markdown("<h4 style='font-weight: bold; color: white;'>Last Name</h4>", unsafe_allow_html=True)
    last_name = st.text_input("Last Name", label_visibility="collapsed", key="dashboard_last_name")

    st.markdown("<h4 style='font-weight: bold; color: white;'>Phone Number</h4>", unsafe_allow_html=True)
    phone_number = st.text_input("Phone Number", label_visibility="collapsed", key="dashboard_phone_number")

    st.markdown("<h4 style='font-weight: bold; color: white;'>ID Number</h4>", unsafe_allow_html=True)
    id_number = st.text_input("ID Number", label_visibility="collapsed", key="dashboard_id_number")

    st.markdown("<h4 style='font-weight: bold; color: white;'>Membership Type</h4>", unsafe_allow_html=True)
    membership_type = st.selectbox("Membership Type", ["monthly", "quarterly", "yearly"], label_visibility="collapsed", key="dashboard_membership_type")

    st.markdown("<h4 style='font-weight: bold; color: white;'>Payment Method</h4>", unsafe_allow_html=True)
    payment_method = st.selectbox("Payment Method", ["credit card", "cash"], label_visibility="collapsed", key="dashboard_payment_method")

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
        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter ID Number to Search</h4>", unsafe_allow_html=True)
        search_id = st.text_input("Enter ID Number to Search", label_visibility="collapsed")
        if st.button("Search by ID"):
            response = requests.get(f"{API_URL}/clients/id/{search_id}")
            if response.status_code == 200:
                client = response.json()
                st.markdown(f"""
                <h3 style='font-weight: bold; color: white;'>Client Details</h3>
                <ul>
                    <li><h4 style='font-weight: bold; color: white;'>Name: {client['first_name']} {client['last_name']} 👤</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Phone: {client['phone_number']} 📞</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>ID Number: {client['id_number']} 🔑</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Membership: {client['membership_type']} 🗓️</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Payment Method: {client['payment_method']} 💳</h4></li>
                </ul>
                """, unsafe_allow_html=True)
            else:
                st.error("Client not found or an error occurred.")

    with col2:
        st.subheader("Search Client by Phone Number")
        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter Phone Number to Search</h4>", unsafe_allow_html=True)
        search_phone = st.text_input("Enter Phone Number to Search", label_visibility="collapsed")
        if st.button("Search by Phone"):
            response = requests.get(f"{API_URL}/clients/phone/{search_phone}")
            if response.status_code == 200:
                client = response.json()
                st.markdown(f"""
                <h3 style='font-weight: bold; color: white;'>Client Details</h3>
                <ul>
                    <li><h4 style='font-weight: bold; color: white;'>Name: {client['first_name']} {client['last_name']} 👤</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Phone: {client['phone_number']} 📞</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>ID Number: {client['id_number']} 🔑</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Membership: {client['membership_type']} 🗓️</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Payment Method: {client['payment_method']} 💳</h4></li>
                </ul>
                """, unsafe_allow_html=True)
            else:
                st.error("Client not found or an error occurred.")

    col3, col4 = st.columns(2)

    col3, col4 = st.columns(2)


    with col3:
        st.subheader("Move Client to Past Clients")
        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter Phone Number to Move</h4>", unsafe_allow_html=True)
        past_phone_number = st.text_input("Enter Phone Number to Move", label_visibility="collapsed")

        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter ID Number to Move</h4>", unsafe_allow_html=True)
        past_id_number = st.text_input("Enter ID Number to Move", label_visibility="collapsed")

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
        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter Phone Number to Search Past Customer</h4>", unsafe_allow_html=True)
        search_past_phone = st.text_input("Enter Phone Number to Search Past Customer", label_visibility="collapsed")

        if st.button("Search Past Customer"):
            response = requests.get(f"{API_URL}/past_clients/")
            if response.status_code == 200:
                past_clients = response.json()
                found = False
                for client in past_clients:
                    if client["phone_number"] == search_past_phone:
                        st.markdown(f"""
                        ### Past Client Details
                        - **Name:** {client['first_name']} {client['last_name']} 👤
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
