import streamlit as st
import requests
from datetime import datetime

API_URL = "http://backend:8000"

def personal_trainings_page():
    """Render the Personal Trainings page."""
    st.header("Personal Trainings")

    col1, col2, col3 = st.columns([1, 1, 1])

    # Display existing schedule
    with col1:
        st.subheader("Current Personal Training Schedule")
        response = requests.get(f"{API_URL}/personal_trainings/schedule/")
        if response.status_code == 200:
            schedule = response.json().get("schedule", {})
            for day, trainings in schedule.items():
                st.markdown(f"### {day.capitalize()}")
                sorted_trainings = sorted(
                    trainings, key=lambda x: datetime.strptime(x["time"].split("-")[0], "%H:%M")
                )
                for training in sorted_trainings:
                    st.markdown(
                        f"💪 **{training['time']}**: {training['trainee_name']} with {training['trainer_name']}"
                    )
        else:
            st.error("Failed to fetch personal training schedule.")

    # Add a new personal training session
    with col2:
        st.subheader("Add a New Personal Training Session")
        trainee_name = st.text_input("Trainee Name", key="trainee_name")
        trainer_name = st.text_input("Trainer Name", key="trainer_name")
        day = st.selectbox("Day", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="day")
        time_slots = [
            "07:00-07:55", "08:00-08:55", "09:00-09:55", "10:00-10:55", "11:00-11:55",
            "12:00-12:55", "13:00-13:55", "14:00-14:55", "15:00-15:55",
            "16:00-16:55", "17:00-17:55", "18:00-18:55", "19:00-19:55",
            "20:00-20:55", "21:00-21:55"
        ]
        time = st.selectbox("Time Slot", time_slots, key="time_slot")
        if st.button("Add Personal Training", key="add_personal_training"):
            response = requests.post(f"{API_URL}/personal_trainings/", json={
                "trainee_name": trainee_name,
                "trainer_name": trainer_name,
                "day": day.lower(),
                "time": time
            })
            if response.status_code == 200:
                st.success("Personal training session added successfully!")
            else:
                st.error(f"Failed to add personal training session: {response.text}")

    # Delete a personal training session
    with col3:
        st.subheader("Delete a Personal Training Session")
        delete_trainer_name = st.text_input("Trainer Name to Delete", key="delete_trainer_name")
        delete_day = st.selectbox("Day to Delete", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="delete_day")
        delete_time = st.selectbox("Time Slot to Delete", time_slots, key="delete_time_slot")

        if st.button("Delete Personal Training", key="delete_personal_training"):
            response = requests.delete(f"{API_URL}/personal_trainings/", params={
                "trainer_name": delete_trainer_name,
                "day": delete_day.lower(),
                "time": delete_time
            })
            if response.status_code == 204:
                st.success("Personal training session deleted successfully!")
            else:
                st.error(f"Failed to delete personal training session: {response.text}")
