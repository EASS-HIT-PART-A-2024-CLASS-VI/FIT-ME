import streamlit as st
import requests

API_URL = "http://backend:8000"

def gym_staff_page():
    """Render the Gym Staff page."""
    st.header("Gym Staff Management")

    col1, col2 = st.columns([1.2, 1.8])

    with col1:
        st.subheader("All Gym Staff Members")
        response = requests.get(f"{API_URL}/gym_staff/")
        if response.status_code == 200:
            staff_members = response.json()
            for member in staff_members:
                emoji = "🧑‍💼" if member["role"] == "Manager" else "🏋️" if member["role"] == "Trainer" else "🖥️"
                st.write(f"- {emoji} **{member['first_name']} {member['last_name']}** ({member['role']}) - Phone: {member['phone_number']}")
        else:
            st.error("Failed to fetch staff members.")

    with col2:
        col21, col22, col23 = st.columns([1, 1, 1])

        with col21:
            st.subheader("Add a New Staff Member")
            first_name = st.text_input("First Name", key="staff_first_name")
            last_name = st.text_input("Last Name", key="staff_last_name")
            role = st.selectbox("Role", ["Receptionist", "Trainer", "Manager"], key="staff_role")
            phone_number = st.text_input("Phone Number", key="staff_phone_number")
            if st.button("Add Staff Member", key="add_staff_member"):
                response = requests.post(f"{API_URL}/gym_staff/", json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role,
                    "phone_number": phone_number
                })
                if response.status_code == 200:
                    st.success("Staff member added successfully!")
                else:
                    st.error(f"Failed to add staff member: {response.text}")

        with col22:
            st.subheader("Delete Staff Member")
            if response.status_code == 200:
                for member in staff_members:
                    if st.button(f"Delete {member['first_name']} {member['last_name']}", key=f"delete_{member['id']}"):
                        delete_response = requests.delete(f"{API_URL}/gym_staff/{member['id']}")
                        if delete_response.status_code == 200:
                            st.success(f"{member['first_name']} {member['last_name']} deleted successfully!")
                        else:
                            st.error(f"Failed to delete {member['first_name']} {member['last_name']}")

        with col23:
            st.subheader("Add a New User")
            username = st.text_input("Username", key="user_username")
            password = st.text_input("Password", key="user_password", type="password")
            if st.button("Add User", key="add_user"):
                response = requests.post(f"{API_URL}/users/", json={
                    "username": username,
                    "password": password
                })
                if response.status_code == 200:
                    st.success("User added successfully!")
                elif response.status_code == 400:
                    st.error("Username already exists.")
                else:
                    st.error("Failed to add user.")

