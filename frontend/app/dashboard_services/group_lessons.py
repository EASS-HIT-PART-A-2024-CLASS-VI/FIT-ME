import streamlit as st
import requests
import pandas as pd
import io

API_URL = "http://backend:8000"

def convert_to_excel(data):
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="GroupLessons")
    processed_data = output.getvalue()
    return processed_data

def group_lessons_page():
    """Render the Group Lessons page."""
    st.header("Group Lessons")

    col1, col2, col3 = st.columns([1, 1, 1])

    # Existing schedule
    with col1:
        st.subheader("Group Lessons Schedule")
        response = requests.get(f"{API_URL}/group_lessons/schedule/")
        if response.status_code == 200:
            schedule = response.json().get("schedule", {})
            for day, lessons in schedule.items():
                st.markdown(f"<h3 style='color: white; font-weight: bold;'>{day.capitalize()}</h3>", unsafe_allow_html=True)
                for lesson in lessons:
                    st.markdown(
                        f"<h4 style='color: white; font-weight: bold;'>🏋️ {lesson['time']}: {lesson['class_name']} with {lesson['instructor_name']}</h4>",
                        unsafe_allow_html=True
                    )
        else:
           st.error("Failed to fetch group lessons schedule.")

        if st.button("Download Group Lessons 📂", key="download_group_lessons"):
            response = requests.get(f"{API_URL}/group_lessons/schedule/")
            if response.status_code == 200:
                schedule_data = [
                    {
                        "Day": day,
                        "Time": lesson["time"],
                        "Class Name": lesson["class_name"],
                        "Instructor": lesson["instructor_name"]
                    }
                    for day, lessons in response.json().get("schedule", {}).items()
                    for lesson in lessons
                ]
                excel_file = convert_to_excel(schedule_data)
                st.download_button(
                    label="Click to Download 📥",
                    data=excel_file,
                    file_name="Group_Lessons_Schedule.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Error fetching group lessons schedule")

    with col2:
        st.subheader("Add a New Group Lesson")

        st.markdown("<h4 style='font-weight: bold; color: white;'>Class Name</h4>", unsafe_allow_html=True)
        class_name = st.text_input(
            "Class Name",
            label_visibility="collapsed",
            key="class_name"
        )

        st.markdown("<h4 style='font-weight: bold; color: white;'>Instructor Name</h4>", unsafe_allow_html=True)
        instructor_name = st.text_input(
            "Instructor Name",
            label_visibility="collapsed",
            key="instructor_name"
        )

        st.markdown("<h4 style='font-weight: bold; color: white;'>Day</h4>", unsafe_allow_html=True)
        day = st.selectbox(
            "Day",
            ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            label_visibility="collapsed",
            key="day"
        )

        st.markdown("<h4 style='font-weight: bold; color: white;'>Time Slot</h4>", unsafe_allow_html=True)
        time_slots = [
            "08:00-08:55", "09:00-09:55", "10:00-10:55", "11:00-11:55",
            "12:00-12:55", "13:00-13:55", "14:00-14:55", "15:00-15:55",
            "16:00-16:55", "17:00-17:55", "18:00-18:55", "19:00-19:55",
            "20:00-20:55", "21:00-21:55"
        ]
        time = st.selectbox(
            "Time Slot",
            time_slots,
            label_visibility="collapsed",
            key="time_slot"
        )

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

    with col3:
        st.subheader("Delete a Group Lesson")

        st.markdown("<h4 style='font-weight: bold; color: white;'>Select Day to Delete</h4>", unsafe_allow_html=True)
        delete_day = st.selectbox(
            "Select Day to Delete",
            ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            label_visibility="collapsed",
            key="delete_day"
        )

        st.markdown("<h4 style='font-weight: bold; color: white;'>Select Time Slot to Delete</h4>", unsafe_allow_html=True)
        delete_time = st.selectbox(
            "Select Time Slot to Delete",
            time_slots,
            label_visibility="collapsed",
            key="delete_time"
        )

        if st.button("Delete Group Lesson", key="delete_group_lesson"):
            response = requests.delete(f"{API_URL}/group_lessons/", params={
                "day": delete_day.lower(),
                "time": delete_time
            })
            if response.status_code == 200:
                st.success("Group lesson deleted successfully!")
            else:
                st.error(f"Failed to delete group lesson: {response.text}")

