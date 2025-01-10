import requests
import streamlit as st
import pandas as pd

API_URL = "http://backend:8000"

# Function to display the login page
def login_page():
    st.title("Login to Manage Gym System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful! Redirecting...")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
        else:
            st.warning("Please enter both username and password.")

# Function to display the main system page
def main_system_page():
    st.title("Manage Gym System")
    st.write(f"Welcome to the system, {st.session_state['username']}!")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.experimental_rerun()

# Section: Add a New Client
st.header("Add a New Client")
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
phone_number = st.text_input("Phone Number")
id_number = st.text_input("ID Number")
membership_type = st.selectbox("Membership Type", ["monthly", "quarterly", "yearly"], key="membership_type_selectbox")
payment_method = st.selectbox("Payment Method", ["credit card", "cash"], key="payment_method_selectbox")
if st.button("Add Client"):
    response = requests.post(f"{API_URL}/clients/", json={
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "id_number": id_number,
        "membership_type": membership_type,
        "payment_method": payment_method
    })
    if response.status_code == 200:
        st.success("Client added successfully!")
    else:
        st.error("Error adding client: " + response.text)

# Section: Search for a Client
st.header("Search for a Client")
search_phone = st.text_input("Enter Phone Number to Search")
if st.button("Search Client"):
    response = requests.get(f"{API_URL}/clients/phone/{search_phone}")
    if response.status_code == 200:
        client = response.json()
        st.write(client)
    else:
        st.error("Client not found or an error occurred.")

# Section: Add an Interested Client
st.header("Add an Interested Client")
interested_first_name = st.text_input("First Name (Interested Client)")
interested_last_name = st.text_input("Last Name (Interested Client)")
interested_phone_number = st.text_input("Phone Number (Interested Client)")

if st.button("Add Interested Client"):
    if not (interested_first_name and interested_last_name and interested_phone_number):
        st.warning("All fields are required!")
    else:
        interested_data = {
            "first_name": interested_first_name,
            "last_name": interested_last_name,
            "phone_number": interested_phone_number
        }
        st.write("Sending Interested Client Data:", interested_data)  # Optional: Log the data being sent
        response = requests.post(f"{API_URL}/interested_clients/", json=interested_data)
        if response.status_code == 200:
            st.success("Interested client added successfully!")
        else:
            st.error(f"Error adding interested client: {response.text}")


# Section: Task Management
st.header("Task Management")
response = requests.get(f"{API_URL}/tasks/")
if response.status_code == 200:
    tasks = response.json()
    st.write("### Current Tasks:")
    for task in tasks:
        st.write(task)
else:
    st.error("Error fetching tasks.")

# Section: Add a Task
st.subheader("Add a Task")
task_first_name = st.text_input("Task First Name")
task_last_name = st.text_input("Task Last Name")
task_phone_number = st.text_input("Task Phone Number")
task_description = st.text_area("Task Description")
if st.button("Add Task"):
    response = requests.post(f"{API_URL}/tasks/", json={
        "first_name": task_first_name,
        "last_name": task_last_name,
        "phone_number": task_phone_number,
        "description": task_description
    })
    if response.status_code == 200:
        st.success("Task added successfully!")
    else:
        st.error("Error adding task: " + response.text)

# Section: Delete a Task
st.subheader("Delete a Task")
delete_task_phone = st.text_input("Enter Phone Number to Delete Task")
if st.button("Delete Task"):
    response = requests.delete(f"{API_URL}/tasks/{delete_task_phone}")
    if response.status_code == 204:
        st.success("Task deleted successfully!")
    else:
        st.error("Error deleting task: " + response.text)

# Section: Group Lessons Management
st.header("Group Lessons Management")
group_day = st.selectbox("Day", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="group_day_selectbox")
group_time = st.text_input("Time (e.g., 08:00-08:55)")
group_class_name = st.text_input("Class Name")
group_instructor_name = st.text_input("Instructor Name")
if st.button("Add Group Lesson"):
    response = requests.post(f"{API_URL}/group_lessons/", json={
        "day": group_day,
        "time": group_time,
        "class_name": group_class_name,
        "instructor_name": group_instructor_name
    })
    if response.status_code == 200:
        st.success("Group lesson added successfully!")
    else:
        st.error("Error adding group lesson: " + response.text)

# Section: View Group Lessons Schedule
st.subheader("View Group Lessons Schedule")

# Function to define the order of days
days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Function to sort and merge the schedule
def display_merged_schedule(schedule):
    # Sort schedule by day and time
    sorted_schedule = {}
    for day in days_order:
        if day in schedule:
            sorted_schedule[day] = sorted(schedule[day], key=lambda x: x['time'])

    # Create a DataFrame
    data = []
    for day, lessons in sorted_schedule.items():
        for idx, lesson in enumerate(lessons):
            if idx == 0:
                # Add the day only once for the first lesson of the day
                data.append([day, lesson['time'], lesson['class_name'], lesson['instructor_name']])
            else:
                # Leave the day column empty for subsequent lessons of the same day
                data.append(["", lesson['time'], lesson['class_name'], lesson['instructor_name']])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Day", "Time", "Class Name", "Instructor"])

    # Display the table in a properly formatted style
    st.write(
            df.style.set_table_styles(
        [
            {"selector": "th", "props": [("text-align", "center"), ("border", "1px solid black")]},
            {"selector": "td", "props": [("text-align", "center"), ("border", "1px solid black")]},
        ]
        ).hide(axis="index").to_html(),
        unsafe_allow_html=True,
    )

# Fetch and display the schedule with merged Day column
if st.button("View Schedule"):
    response = requests.get(f"{API_URL}/group_lessons/schedule/")
    if response.status_code == 200:
        schedule = response.json().get("schedule", {})
        display_merged_schedule(schedule)
    else:
        st.error("Error fetching group lessons schedule.")

# Section: Personal Training Management
st.header("Personal Training Management")
personal_day = st.selectbox("Day", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="personal_day_selectbox")
personal_time = st.text_input("Time (e.g., 10:00-11:00)")
personal_trainee_name = st.text_input("Trainee Name")
personal_trainer_name = st.text_input("Trainer Name")
if st.button("Add Personal Training Session"):
    response = requests.post(f"{API_URL}/personal_trainings/", json={
        "day": personal_day,
        "time": personal_time,
        "trainee_name": personal_trainee_name,
        "trainer_name": personal_trainer_name
    })
    if response.status_code == 200:
        st.success("Personal training session added successfully!")
    else:
        st.error("Error adding personal training session: " + response.text)

# Section: View Personal Training Schedule
st.subheader("View Personal Training Schedule")
if st.button("View Personal Training Schedule"):
    response = requests.get(f"{API_URL}/personal_trainings/schedule/")
    if response.status_code == 200:
        schedule = response.json()
        st.write(schedule)
    else:
        st.error("Error fetching personal training schedule.")

# Section: Gym Staff Management
st.header("Gym Staff Management")
staff_first_name = st.text_input("Staff First Name")
staff_last_name = st.text_input("Staff Last Name")
staff_role = st.selectbox("Role", ["trainer", "manager", "secretary"], key="staff_role_selectbox")
staff_phone_number = st.text_input("Staff Phone Number")
if st.button("Add Gym Staff"):
    response = requests.post(f"{API_URL}/gym_staff/", json={
        "first_name": staff_first_name,
        "last_name": staff_last_name,
        "role": staff_role,
        "phone_number": staff_phone_number
    })
    if response.status_code == 200:
        st.success("Gym staff member added successfully!")
    else:
        st.error("Error adding gym staff member: " + response.text)

# Section: View Gym Staff
st.subheader("View Gym Staff")
if st.button("View All Staff"):
    response = requests.get(f"{API_URL}/gym_staff/")
    if response.status_code == 200:
        staff = response.json()
        st.write(staff)
    else:
        st.error("Error fetching gym staff.")

# Main application logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_system_page()
else:
    login_page()

