import streamlit as st
from app.dashboard_services.client_management import client_management_services

def dashboard_page():
    """Main dashboard page with navigation buttons."""
    st.title("Fit-Me System")

    st.subheader("Choose a Service")

    # Button: Client Management
    if st.button("Client Management"):
        client_management_services()

    # Add additional buttons for other services here...
 
