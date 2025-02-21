import streamlit as st
import requests
import pandas as pd
import io
from datetime import date,datetime

API_URL = "http://backend:8000"

def get_payment_emoji(payment_method: str) -> str:
    return "💵" if payment_method.lower() == "cash" else "💳"

def calculate_age(date_of_birth: str) -> str:
    if not date_of_birth:
        return "Unknown"

    try:
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return f"{age:.0f}"
    except ValueError:
        return "Invalid Date"

def convert_to_excel(data, sheet_name="Clients"):
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

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

    min_year = 1948
    max_year = date.today().year

    st.markdown("<h4 style='font-weight: bold; color: white;'>Date of Birth</h4>", unsafe_allow_html=True)
    date_of_birth = st.date_input(
        "Date of Birth",
        min_value=date(min_year, 1, 1),
        max_value=date(max_year, 12, 31),
        key="dashboard_dob"
)

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
            "date_of_birth": str(date_of_birth),
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
                if client.get('date_of_birth'):
                   try:
                       dob_formatted = datetime.strptime(client['date_of_birth'], "%Y-%m-%d").strftime("%d/%m/%Y")
                       age = calculate_age(client['date_of_birth'])
                   except ValueError:
                       dob_formatted = "Invalid Date"
                       age = "Invalid Age"
                else:
                    dob_formatted = "Not Provided"
                payment_emoji = get_payment_emoji(client['payment_method'])
                st.markdown(f"""
                <h3 style='font-weight: bold; color: white;'>Client Details</h3>
                <ul>
                    <li><h4 style='font-weight: bold; color: white;'>Name: {client['first_name']} {client['last_name']} 👤</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Phone: {client['phone_number']} 📞</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>ID Number: {client['id_number']} 🔑</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Date of Birth: {dob_formatted} 🎂 (Age: {age} 🕰️)</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Membership: {client['membership_type']} 🗓️</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Payment Method: {client['payment_method']} {payment_emoji}</h4></li>
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
                if client.get('date_of_birth'):
                   try:
                       dob_formatted = datetime.strptime(client['date_of_birth'], "%Y-%m-%d").strftime("%d/%m/%Y")
                       age = calculate_age(client['date_of_birth'])
                   except ValueError:
                       dob_formatted = "Invalid Date"
                       age = "Invalid Age"
                else:
                    dob_formatted = "Not Provided"
                payment_emoji = get_payment_emoji(client['payment_method'])
                st.markdown(f"""
                <h3 style='font-weight: bold; color: white;'>Client Details</h3>
                <ul>
                    <li><h4 style='font-weight: bold; color: white;'>Name: {client['first_name']} {client['last_name']} 👤</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Phone: {client['phone_number']} 📞</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>ID Number: {client['id_number']} 🔑</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Date of Birth: {dob_formatted}🎂 (Age: {age} 🕰️)</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Membership: {client['membership_type']} 🗓️</h4></li>
                    <li><h4 style='font-weight: bold; color: white;'>Payment Method: {client['payment_method']} {payment_emoji}</h4></li>
                </ul>
                """, unsafe_allow_html=True)
            else:
                st.error("Client not found or an error occurred.")

        if st.button("Download Active Clients 📂"):
            response = requests.get(f"{API_URL}/clients/")
            if response.status_code == 200:
                client_data = response.json()
                excel_file = convert_to_excel(client_data)
                st.download_button(label="📥 Click to Download Active Clients to Excel",
                                   data=excel_file,
                                   file_name="Active_Clients.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.error("Error fetching client data")

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
        st.subheader("Past Clients Archive")
        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter Phone Number to Search Past Customer</h4>", unsafe_allow_html=True)
        search_past_phone = st.text_input("Enter Phone Number to Search Past Customer", label_visibility="collapsed")

        if st.button("Search Past Customer"):
            response = requests.get(f"{API_URL}/past_clients/")
            if response.status_code == 200:
                past_clients = response.json()
                found = False
                for client in past_clients:
                    if client["phone_number"] == search_past_phone:
                        if client.get('date_of_birth'):
                            try:
                                dob_formatted = datetime.strptime(client['date_of_birth'], "%Y-%m-%d").strftime("%d/%m/%Y")
                                age = calculate_age(client['date_of_birth'])
                            except ValueError:
                                dob_formatted = "Invalid Date"
                                age = "Invalid Age"
                        else:
                            dob_formatted = "Not Provided"
                        payment_emoji = get_payment_emoji(client['payment_method'])
                        st.markdown(f"""
                        <h3 style='font-weight: bold; color: white;'>Client Details</h3>
                        <ul>
                            <li><h4 style='font-weight: bold; color: white;'>Name: {client['first_name']} {client['last_name']} 👤</h4></li>
                            <li><h4 style='font-weight: bold; color: white;'>Phone: {client['phone_number']} 📞</h4></li>
                            <li><h4 style='font-weight: bold; color: white;'>ID Number: {client['id_number']} 🔑</h4></li>
                            <li><h4 style='font-weight: bold; color: white;'>Date of Birth: {dob_formatted} 🎂 (Age: {age} 🕰️)</h4></li>
                            <li><h4 style='font-weight: bold; color: white;'>Membership: {client['membership_type']} 🗓️</h4></li>
                            <li><h4 style='font-weight: bold; color: white;'>Payment Method: {client['payment_method']} {payment_emoji}</h4></li>
                        </ul>
                        """, unsafe_allow_html=True)
                        found = True
                        break
                if not found:
                    st.warning("Past customer not found.")
            else:
                st.error(f"Error: {response.text}")

        if st.button("Download Past Clients Archive 📂", key="download_past_clients"):
            response = requests.get(f"{API_URL}/past_clients/")
            if response.status_code == 200:
                past_client_data = response.json()
                if past_client_data:
                    excel_file = convert_to_excel(past_client_data, sheet_name="Past Clients")
                    st.download_button(
                        label="📥 Click to Download Archive to Excel",
                        data=excel_file,
                        file_name="past_clients.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("No past clients found.")
            else:
                st.error("Error fetching past client data")
