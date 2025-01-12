import streamlit as st
from app.dashboard_services.client_management import client_management_services

def dashboard_page():
    """Main dashboard page with navigation buttons."""
    st.title("Fit-Me System")

    # Check the session state to see if a button is already selected
    if "dashboard_selected_service" not in st.session_state:
        # Initialize the session state variable for the selected service
        st.session_state["dashboard_selected_service"] = None

    # Display the service selection buttons
    st.subheader("Choose a Service")

    # Button for "Client Management"
    if st.button("Client Management"):
        # Update session state to indicate that the "Client Management" service is selected
        st.session_state["dashboard_selected_service"] = "client_management"

    # Perform actions based on the selected button
    if st.session_state["dashboard_selected_service"] == "client_management":
        # Call the client management services function
        client_management_services() 
