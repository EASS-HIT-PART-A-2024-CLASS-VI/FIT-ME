import streamlit as st
import pandas as pd
import io
import requests
from datetime import datetime,date

API_URL = "http://backend:8000"

def convert_to_excel(data, sheet_name="Gym_Staff"):
    """Convert JSON data to an Excel file."""
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

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
                st.markdown(
                    f"<h4 style='color: white; font-weight: bold;'>{emoji} {member['first_name']} {member['last_name']} ({member['role']}) - Phone: {member['phone_number']}</h4>",
                    unsafe_allow_html=True
                )
            if st.button("Download Gym Staff 📂"):
                excel_file = convert_to_excel(staff_members)
                st.download_button(label="📥 Click to Download Gym Staff List to Excel",
                                   data=excel_file,
                                   file_name="Gym_Staff.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.error("Failed to fetch staff members.")

    with col2:
        col21, col22, col23, col24 = st.columns([1, 1, 1, 1])

        with col21:
            st.subheader("Add a New Staff Member")

            st.markdown("<h4 style='font-weight: bold; color: white;'>First Name</h4>", unsafe_allow_html=True)
            first_name = st.text_input("First Name", label_visibility="collapsed", key="staff_first_name")

            st.markdown("<h4 style='font-weight: bold; color: white;'>Last Name</h4>", unsafe_allow_html=True)
            last_name = st.text_input("Last Name", label_visibility="collapsed", key="staff_last_name")

            st.markdown("<h4 style='font-weight: bold; color: white;'>Role</h4>", unsafe_allow_html=True)
            role = st.selectbox("Role", ["Receptionist", "Trainer", "Manager"], label_visibility="collapsed", key="staff_role")

            st.markdown("<h4 style='font-weight: bold; color: white;'>Phone Number</h4>", unsafe_allow_html=True)
            phone_number = st.text_input("Phone Number", label_visibility="collapsed", key="staff_phone_number")

            st.markdown("<h4 style='font-weight: bold; color: white;'>Date of Birth</h4>", unsafe_allow_html=True)
            min_year = 1948
            max_year = date.today().year
            date_of_birth = st.date_input(
                "Date of Birth", 
                min_value=date(min_year, 1, 1), 
                max_value=date(max_year, 12, 31), 
                key="staff_dob"
            )

            if st.button("Add Staff Member", key="add_staff_member"):
                response = requests.post(f"{API_URL}/gym_staff/", json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role,
                    "phone_number": phone_number,
                    "date_of_birth": date_of_birth.strftime("%Y-%m-%d")
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

            st.markdown("<h4 style='font-weight: bold; color: white;'>Username</h4>", unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed", key="user_username")

            st.markdown("<h4 style='font-weight: bold; color: white;'>Password</h4>", unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed", key="user_password")

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

        with col24:
            st.subheader("Delete User")
            response = requests.get(f"{API_URL}/users/")
            if response.status_code == 200:
                users = response.json()
                for user in users:
                    if st.button(f"Delete {user['username']}", key=f"delete_user_{user['username']}"):
                        delete_response = requests.delete(f"{API_URL}/users/{user['username']}")
                        if delete_response.status_code == 204:
                            st.success(f"User {user['username']} deleted successfully!")
                        elif delete_response.status_code == 404:
                            st.error(f"User {user['username']} not found.")
                        else:
                            st.error(f"Failed to delete user {user['username']}.")
            else:
                st.error("Failed to fetch users.")
