import streamlit as st
import requests

API_URL = "http://backend:8000"

def task_management_page():
    """Render the Task Management page."""
    st.header("Tasks Management")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.subheader("Existing Tasks")
        response = requests.get(f"{API_URL}/tasks/")
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                for task in tasks:
                    st.markdown(
                        f"📝 **{task['first_name']} {task['last_name']} - {task['description']} (Phone: {task['phone_number']}**)"
                    )
            else:
                st.info("No tasks available.")
        else:
            st.error("Failed to fetch tasks.")

    with col2:
        st.subheader("Add a New Task")
        first_name = st.text_input("First Name", key="task_first_name")
        last_name = st.text_input("Last Name", key="task_last_name")
        phone_number = st.text_input("Phone Number", key="task_phone_number")
        description = st.text_area("Task Description", key="task_description")
        if st.button("Add Task", key="add_task"):
            response = requests.post(f"{API_URL}/tasks/", json={
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "description": description
            })
            if response.status_code == 200:
                st.success("Task added successfully!")
            else:
                st.error(f"Failed to add task: {response.text}")

    with col3:
        st.subheader("Delete a Task")
        delete_phone_number = st.text_input(
            "Enter Phone Number of the Task to Delete", key="task_delete_phone_number"
        )
        if st.button("Delete Task", key="delete_task"):
            response = requests.delete(f"{API_URL}/tasks/{delete_phone_number}")
            if response.status_code == 204:
                st.success("Task deleted successfully!")
            elif response.status_code == 404:
                st.warning("Task not found.")
            else:
                st.error("Failed to delete task.")

