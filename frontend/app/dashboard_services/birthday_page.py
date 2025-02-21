import streamlit as st
import requests
from datetime import datetime,date

API_URL = "http://backend:8000"

def get_current_month():
    return datetime.now().month

def fetch_birthdays(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}")
    if response.status_code == 200:
        return response.json()
    return []

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d-%m-%Y")
    except ValueError:
        return date_str

def days_diff_this_year(birthdate_str):
    today = date.today()
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    this_year_bday = date(year=today.year, month=birthdate.month, day=birthdate.day)
    return (this_year_bday - today).days

def birthday_page():
    st.markdown(
        """
        <style>
            .big-title {
                font-size: 60px;
                font-weight: bold;
                color: white;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                font-size: 35px;
                font-weight: bold;
                color: white;
                text-align: center;
                margin-bottom: 35px;
            }
            .section-header {
                font-size: 35px;
                font-weight: bold;
                color: white;
                margin-top: 35px;
                text-align: center;
            }
            .checkbox-label {
                font-size: 30px;
                color: white;
                text-align: center;
            }
            .birthday-entry {
                font-size: 33px !important;
                font-weight: bold;
                color: white;
                margin-top: 10px;
                text-align: center;
            }
            div[data-testid="stCheckbox"] label div[data-testid="stMarkdownContainer"] p {
            font-size: 33px !important;
            font-weight: bold !important;
            color: white !important;
            }

            div[data-testid="stCheckbox"] input[type="checkbox"] {
            width: 25px !important;
            height: 25px !important;
            transform: scale(1.5) !important;
            margin-right: 10px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='big-title'>🎂 Birthdays 🎂</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>View this month's birthdays!</div>", unsafe_allow_html=True)

    col1, col2, col_center, col4, col5 = st.columns([1, 2.8, 3.5, 1.5, 1])
    with col_center:
        show_employees = st.checkbox("Show Employees Birthdays 🎉", key="show_employees")
        show_clients = st.checkbox("Show Clients Birthdays 🎈", key="show_clients")

    current_month = get_current_month()

    if show_employees and not show_clients:
        st.markdown("<div class='section-header'> Employees Birthdays This Month</div>", unsafe_allow_html=True)
        employees = fetch_birthdays("gym_staff")
        employees_with_birthday = [e for e in employees if int(e["date_of_birth"].split("-")[1]) == current_month]

        if employees_with_birthday:
            for employee in employees_with_birthday:
                diff = days_diff_this_year(employee['date_of_birth'])
                if diff is None:
                    extra_text = ""
                elif diff > 0:
                    extra_text = f" - {diff} days left"
                elif diff == 0:
                    extra_text = " - Today!"
                else:
                    extra_text = f" - Passed {abs(diff)} days ago"

                st.markdown(
                    f"<p class='birthday-entry'>🎉 {employee['first_name']} {employee['last_name']} - {format_date(employee['date_of_birth'])}{extra_text}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No employees have birthdays this month.")

    elif show_clients and not show_employees:
        st.markdown("<div class='section-header'> Clients Birthdays This Month</div>", unsafe_allow_html=True)
        clients = fetch_birthdays("clients")
        clients_with_birthday = [c for c in clients if int(c["date_of_birth"].split("-")[1]) == current_month]

        if clients_with_birthday:
            for client in clients_with_birthday:
                diff = days_diff_this_year(client['date_of_birth'])
                if diff is None:
                    extra_text = ""
                elif diff > 0:
                    extra_text = f" - {diff} days left"
                elif diff == 0:
                    extra_text = " - Today!"
                else:
                    extra_text = f" - Passed {abs(diff)} days ago"
                st.markdown(
                    f"<p class='birthday-entry'>🎈 {client['first_name']} {client['last_name']} - {format_date(client['date_of_birth'])}{extra_text}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No clients have birthdays this month.")

    elif show_clients and show_employees:
        st.warning("Please select only one option at a time.")

