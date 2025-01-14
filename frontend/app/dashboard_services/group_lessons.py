import streamlit as st
import requests

API_URL = "http://backend:8000"

def group_lessons_page():
    """Render the Group Lessons page."""
    st.header("Group Lessons")

    # Section 1: Display existing schedule
    st.subheader("Group Lessons Schedule")
    response = requests.get(f"{API_URL}/group_lessons/schedule/")
    if response.status_code == 200:
        schedule = response.json().get("schedule", {})
        for day, lessons in schedule.items():
            st.markdown(f"### {day.capitalize()}")
            # Display lessons directly (already sorted from backend)
            for lesson in lessons:
                st.write(f"- {lesson['time']}: {lesson['class_name']} with {lesson['instructor_name']}")
    else:
        st.error("Failed to fetch group lessons schedule.")

    # Section 2: Add a new group lesson
    st.subheader("Add a New Group Lesson")
    class_name = st.text_input("Class Name", key="class_name")
    instructor_name = st.text_input("Instructor Name", key="instructor_name")
    day = st.selectbox("Day", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="day")
    time_slots = [
        "08:00-08:55", "09:00-09:55", "10:00-10:55", "11:00-11:55",
        "12:00-12:55", "13:00-13:55", "14:00-14:55", "15:00-15:55",
        "16:00-16:55", "17:00-17:55", "18:00-18:55", "19:00-19:55",
        "20:00-20:55", "21:00-21:55"
    ]
    time = st.selectbox("Time Slot", time_slots, key="time_slot")

    if st.button("Add Group Lesson", key="add_group_lesson"):
        response = requests.post(f"{API_URL}/group_lessons/", json={
            "class_name": class_name,
            "instructor_name": instructor_name,
            "day": day.lower(),
            "time": time
        })
        if response.status_code == 200:
            st.success("Group lesson added successfully!")
        else:
            st.error(f"Failed to add group lesson: {response.text}")

    # Section 3: Delete a group lesson
    st.subheader("Delete a Group Lesson")
    delete_day = st.selectbox("Select Day to Delete", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="delete_day")
    delete_time = st.selectbox("Select Time Slot to Delete", [
        "08:00-08:55", "09:00-09:55", "10:00-10:55", "11:00-11:55",
        "12:00-12:55", "13:00-13:55", "14:00-14:55", "15:00-15:55",
        "16:00-16:55", "17:00-17:55", "18:00-18:55", "19:00-19:55",
        "20:00-20:55", "21:00-21:55"
    ], key="delete_time")

    if st.button("Delete Group Lesson", key="delete_group_lesson"):
        response = requests.delete(f"{API_URL}/group_lessons/", params={
            "day": delete_day.lower(),
            "time": delete_time
        })
        if response.status_code == 200:
            st.success("Group lesson deleted successfully!")
        else:
            st.error(f"Failed to delete group lesson: {response.text}")
