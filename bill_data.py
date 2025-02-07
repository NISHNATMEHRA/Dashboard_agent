import streamlit as st
import pandas as pd

# Add custom HTML for modern styling
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

def show(source_name, bill_data, data):
    source_name = source_name.lower()

    st.markdown(custom_html, unsafe_allow_html=True)
    st.markdown("<h1 class='title'>📊 Billing Dashboard</h1>", unsafe_allow_html=True)

    # Validate owner password
    if "owner_password" in data.columns and bill_data in data["owner_password"].values:
        # Filter data for the selected source name
        df_bill = data[data["Source Name"].str.lower() == source_name].copy()
        df_bill["Registration ID"] = df_bill["Registration ID"].astype(str)

        required_columns = [
            "Customer Name", "Registration ID", "City", "Service Name", "Car Name",
            "Car Odometer", "Car No", "Mobile No", "Delivered Date",
            "Amount_WO_gst", "total Gmv"
        ]

        # Ensure Delivered Date is datetime
        df_bill["Delivered Date"] = pd.to_datetime(df_bill["Delivered Date"], errors='coerce')
        data_filter = df_bill[required_columns]

        if data_filter.empty:
            st.markdown("<div class='feedback warning'>No data found for source: <b>{}</b></div>".format(source_name), unsafe_allow_html=True)
            return

        # Dropdown to select search type
        un_city = data_filter["City"].unique()
        search_type = st.selectbox(
            "Search by City",
            options=["Select an option", "All Cities"] + list(un_city),
            key="city_selector",
            help="Choose a city to filter data or select 'All Cities' for complete data."
        )

        if search_type == "All Cities":
            filtered_data = data_filter
            st.markdown("<div class='feedback success'>Showing data for all cities.</div>", unsafe_allow_html=True)
        elif search_type in un_city:
            filtered_data = data_filter[data_filter["City"] == search_type]
            st.markdown(f"<div class='feedback success'>Showing data for city: <b>{search_type}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='feedback warning'>Please select a valid search option.</div>", unsafe_allow_html=True)
            return

        # Date range filtering
        st.markdown("<p class='dropdown'><b>Select Date Range:</b></p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        # Format date input fields
        with col1:
            start_date = st.date_input("Start Date", filtered_data['Delivered Date'].min().date(), format="DD-MM-YYYY")
        with col2:
            end_date = st.date_input("End Date", filtered_data['Delivered Date'].max().date(), format="DD-MM-YYYY")

        if start_date > end_date:
            st.markdown("<div class='feedback error'>Start date must be earlier than or equal to end date.</div>",
                        unsafe_allow_html=True)
        else:
            # Filter data based on selected date range
            mask = (filtered_data['Delivered Date'] >= pd.to_datetime(start_date)) & (
                        filtered_data['Delivered Date'] <= pd.to_datetime(end_date))
            date_filtered_data = filtered_data[mask]

            if date_filtered_data.empty:
                st.markdown(
                    f"<div class='feedback warning'>No data found between {start_date.strftime('%d-%m-%Y')} and {end_date.strftime('%d-%m-%Y')}.</div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div class='feedback success'>Data from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:</div>",
                    unsafe_allow_html=True)

                # Create a copy of the filtered data and format the 'Delivered Date' column
                date_filtered_data = date_filtered_data.copy()
                date_filtered_data['Delivered Date'] = date_filtered_data['Delivered Date'].dt.strftime('%d-%m-%Y')

                # Display summary stats
                st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
                st.markdown(f"**Total Records:** {date_filtered_data.shape[0]}")
                st.markdown(f"**Total Amount (WO GST):** ₹{date_filtered_data['Amount_WO_gst'].sum():,.2f}")
                st.markdown(f"**Total GMV:** ₹{date_filtered_data['total Gmv'].sum():,.2f}")
                st.markdown("</div>", unsafe_allow_html=True)

                # Display data in an expandable section
                with st.expander("View Filtered Data"):
                    st.dataframe(date_filtered_data)
    else:
        st.markdown("<div class='feedback error'>This section is only accessible to the Owner.<br>Please log in with the Owner password!</div>", unsafe_allow_html=True)
