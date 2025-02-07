import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


# Function to connect to Google Sheet and fetch data
def connect_to_sheet(json_keyfile, spreadsheet_url, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(spreadsheet_url).worksheet(sheet_name)
    data = pd.DataFrame(sheet.get_all_records())  # Fetch all records into a DataFrame
    return sheet, data


# Function to insert new data into Google Sheet
def insert_data_to_sheet(sheet, new_data):
    sheet.append_row(new_data)


# Function to run the Streamlit app
def run():
    st.title("Google Sheets Data Integration")

    # Add custom HTML styling
    st.markdown(
        """
        <style>
            .title {
                font-size: 36px;
                font-weight: bold;
                color: #4CAF50;
                text-align: center;
            }
            .subheader {
                font-size: 24px;
                color: #2196F3;
                margin-top: 20px;
            }
            .form-input {
                margin-bottom: 10px;
            }
            .success-message {
                color: green;
                font-weight: bold;
                text-align: center;
            }
            .error-message {
                color: red;
                font-weight: bold;
                text-align: center;
            }
            .loading {
                text-align: center;
                font-size: 18px;
                color: #FF5722;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    json_keyfile = "deshboard-agent_key.env"
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1nN11gQ_F38CdjC7Wd0X0tj8ZRY6qgU-cGB9PZ24twc0/edit?gid=0#gid=0"
    sheet_name = "Complained"

    try:
        # Show loading indicator while connecting
        with st.spinner('Connecting to Google Sheets...'):
            sheet, data = connect_to_sheet(json_keyfile, spreadsheet_url, sheet_name)

        # Form to add new data
        st.markdown('<div class="subheader">Add New Data</div>', unsafe_allow_html=True)
        with st.form("add_data_form"):
            car_number = st.text_input("Car Number", key="car_number", placeholder="Enter the car number")
            remark = st.text_area("Remark of the Problem", key="remark", placeholder="Describe the issue")
            additional_field = st.text_input("Additional Information", key="additional_info",
                                             placeholder="Provide any extra details")
            complain_date = st.date_input("Date of Complaint", key="complain_date", min_value=datetime.today().date())
            submit_button = st.form_submit_button("Add Data")

            if submit_button:
                # Basic form validation
                if car_number and remark:
                    with st.spinner('Submitting your data...'):
                        # Format date for JSON serialization
                        date_of_complain = complain_date.isoformat()  # Convert date to ISO format
                        new_data = [car_number, date_of_complain, remark, additional_field]
                        insert_data_to_sheet(sheet, new_data)
                        st.markdown('<div class="success-message">Data added successfully!</div>',
                                    unsafe_allow_html=True)
                        # Refresh the app after adding new data
                        st.rerun()
                else:
                    st.markdown('<div class="error-message">Please fill in all required fields!</div>',
                                unsafe_allow_html=True)

        # Button to refresh data manually
        if st.button("Refresh Data"):
            with st.spinner('Refreshing data...'):
                sheet, data = connect_to_sheet(json_keyfile, spreadsheet_url, sheet_name)
                if data.empty:
                    st.markdown('<div class="error-message">No data found in the sheet.</div>', unsafe_allow_html=True)
                else:
                    st.dataframe(data)

    except Exception as e:
        st.markdown(f'<div class="error-message">Error: {e}</div>', unsafe_allow_html=True)


# Automatically run the app
if __name__ == "__main__":
    run()
