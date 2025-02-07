import streamlit as st
import pandas as pd
from datetime import datetime

# Custom HTML for styling
custom_html = """
<style>
    .title {
        font-family: 'Arial Black', sans-serif;
        background-color: #000000; /* Changed to black */
        color: white; /* Text color changed to white for contrast */
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        font-size: 36px;
        font-weight: bold;
    }
    .feedback {
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning {
        background-color: #f39c12;
        color: white;
    }
    .error {
        background-color: #e74c3c;
        color: white;
    }
    .success {
        background-color: #27ae60;
        color: white;
    }
    .stats-box {
        background-color: #ecf0f1;
        padding: 15px;
        margin: 20px 0;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .dropdown {
        margin-bottom: 15px;
    }
    .search-box {
        padding: 10px;
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
"""

def show(source_name, data):
    source_name = source_name.lower()

    st.markdown(custom_html, unsafe_allow_html=True)  # Apply custom styles
    st.markdown("<div class='title'>📊 Show Data</div>", unsafe_allow_html=True)  # Custom title header

    # Filter data for the selected source name
    data_filter = data[data["Source Name"].str.lower() == source_name].copy()
    data_filter["Registration ID"] = data_filter["Registration ID"].astype(str)

    required_columns = [
        "Source Name", "Registration ID", "City", "Service Name", "Car Name",
        "Customer Name", "Car Odometer", "Car No", "Mobile No", "Delivered Date"
    ]

    # Ensure Delivered Date is datetime
    data_filter["Delivered Date"] = pd.to_datetime(data_filter["Delivered Date"], errors='coerce')
    data_filter = data_filter[required_columns]

    if data_filter.empty:
        st.markdown("<div class='warning'>No data found for source: **{source_name}**</div>", unsafe_allow_html=True)
        return

    # Display the search options label with HTML styling
    st.markdown("<h4 style='color: blue;'>Search Options:</h4>", unsafe_allow_html=True)

    # Dropdown to select search type
    un_city = data_filter["City"].unique()
    search_type = st.selectbox(
        "Select an option",
        options=["Select an option", "All Cities"] + list(un_city),
        format_func=lambda x: "🔍 " + x if x != "Select an option" else x,
        key="search_type",
        help="Select a city or 'All Cities' to view data from all cities"
    )

    if search_type == "All Cities":
        filtered_data = data_filter
        st.markdown("<p style='color: green;'>Showing data for all cities.</p>", unsafe_allow_html=True)
    elif search_type in un_city:
        filtered_data = data_filter[data_filter["City"] == search_type]
        st.markdown(f"<p style='color: green;'>Showing data for city: <b>{search_type}</b></p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: red;'>Please select a valid search option.</p>", unsafe_allow_html=True)
        return

    # Date range filtering
    st.markdown("<h4 style='color: blue;'>Filter by Date Range:</h4>", unsafe_allow_html=True)
    start_date, end_date = st.columns(2)

    with start_date:
        start_date_value = st.date_input("Start Date", filtered_data['Delivered Date'].min().date(), format="DD-MM-YYYY")
    with end_date:
        end_date_value = st.date_input("End Date", filtered_data['Delivered Date'].max().date(), format="DD-MM-YYYY")

    if start_date_value > end_date_value:
        st.markdown("<div class='error'>Start date must be earlier than or equal to end date.</div>", unsafe_allow_html=True)
    else:
        mask = (filtered_data['Delivered Date'] >= pd.to_datetime(start_date_value)) & \
               (filtered_data['Delivered Date'] <= pd.to_datetime(end_date_value))
        date_filtered_data = filtered_data[mask]

        if date_filtered_data.empty:
            st.markdown(f"<div class='warning'>No data found between {start_date_value.strftime('%d-%m-%Y')} and {end_date_value.strftime('%d-%m-%Y')}.</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<h5 style='color: green;'>Displaying 📋 {len(date_filtered_data)} records from {start_date_value.strftime('%d-%m-%Y')} to {end_date_value.strftime('%d-%m-%Y')}:</h5>",
                unsafe_allow_html=True
            )

            st.dataframe(date_filtered_data, use_container_width=True)

            # Download Button
            csv = date_filtered_data.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data as Excel",
                data=csv,
                file_name=f"filtered_data_{datetime.now().strftime('%d%m%y')}.csv",
                mime="text/csv",
                help="Click to download the filtered data."
            )

