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
                        f"<h4 style='color: white; font-weight: bold;'>📝 {task['first_name']} {task['last_name']} - {task['description']} (Phone: {task['phone_number']})</h4>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No tasks available.")
        else:
            st.error("Failed to fetch tasks.")

    with col2:
        st.subheader("Add a New Task")

        st.markdown("<h4 style='font-weight: bold; color: white;'>First Name</h4>", unsafe_allow_html=True)
        first_name = st.text_input("First Name", label_visibility="collapsed", key="task_first_name")

        st.markdown("<h4 style='font-weight: bold; color: white;'>Last Name</h4>", unsafe_allow_html=True)
        last_name = st.text_input("Last Name", label_visibility="collapsed", key="task_last_name")

        st.markdown("<h4 style='font-weight: bold; color: white;'>Phone Number</h4>", unsafe_allow_html=True)
        phone_number = st.text_input("Phone Number", label_visibility="collapsed", key="task_phone_number")

        st.markdown("<h4 style='font-weight: bold; color: white;'>Task Description</h4>", unsafe_allow_html=True)
        description = st.text_area("Task Description", label_visibility="collapsed", key="task_description")

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

        st.markdown("<h4 style='font-weight: bold; color: white;'>Enter Phone Number of the Task to Delete</h4>", unsafe_allow_html=True)
        delete_phone_number = st.text_input("Enter Phone Number of the Task to Delete", label_visibility="collapsed", key="task_delete_phone_number")

        if st.button("Delete Task", key="delete_task"):
            response = requests.delete(f"{API_URL}/tasks/{delete_phone_number}")
            if response.status_code == 204:
                st.success("Task deleted successfully!")
            elif response.status_code == 404:
                st.warning("Task not found.")
            else:
                st.error("Failed to delete task.")
