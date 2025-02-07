import streamlit as st
import pandas as pd

# Add custom HTML for styling
custom_html = """
<style>
    .dashboard-title {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 20px;
        font-size: 36px;
        animation: fadeIn 2s ease-in-out;
    }
    .order-stats {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
        padding: 20px;
        border-radius: 10px;
        animation: slideIn 2s ease-in-out;
        border: 2px solid black;
        background-color: red; /* Fill background with red color */
    }
    .stat-box {
        background: linear-gradient(135deg, #6dd5ed, #2193b0);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: white;
        font-weight: bold;
        width: 30%;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
    }
    .stat-box:hover {
        transform: scale(1.1);
    }
    .search-box {
        margin: 20px 0;
        text-align: center;
    }
    .order-details {
        background: linear-gradient(135deg, #f7f9f9, #dff9fb);
        border-left: 5px solid #e74c3c;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        animation: fadeIn 1.5s ease-in-out;
    }
    .order-details h4 {
        color: #e74c3c;
        font-size: 24px;
        animation: colorChange 3s infinite;
    }
    .order-details p {
        color: #34495e;
        font-size: 18px;
        margin: 5px 0;
    }
    .order-details .highlight {
        color: #e74c3c;
        font-weight: bold;
    }
    .error {
        color: #e74c3c;
        font-weight: bold;
        font-size: 18px;
        animation: shake 0.5s ease-in-out;
    }
    .warning {
        color: #f39c12;
        font-weight: bold;
        font-size: 18px;
    }
    .yellow-bar {
        width: 100%;
        height: 20px;
        background-color: yellow;
        position: relative;
        margin: 20px 0;
        overflow: hidden;
    }

    .car-icon {
        width: 40px;
        height: 20px;
        background: url('https://th.bing.com/th/id/R.7d976b82d25e6cf935a66cfca36bc1d4?rik=O6vGeLXrScKKfw&riu=http%3a%2f%2fclipart-library.com%2fimages_k%2fcar-clipart-transparent-background%2fcar-clipart-transparent-background-18.png&ehk=G2qF2jCCSdgZ9WxDKriGloJl14wESAawFrgpnf2GxvI%3d&risl=&pid=ImgRaw&r=0') no-repeat center;
        background-size: contain;
        position: absolute;
        animation: drive 8s linear infinite;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }

    @keyframes colorChange {
        0% { color: #e74c3c; }
        50% { color: #2ecc71; }
        100% { color: #e74c3c; }
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    @keyframes drive {
        0% { left: 0; }
        100% { left: 100%; }
    }
</style>
"""

def show(source_name, data):
    source_name = source_name.lower()

    st.markdown(custom_html, unsafe_allow_html=True)
    st.markdown(
        f"<h1 class='dashboard-title'>"
        f"<span style='color: red;'>Go</span>"
        f"Mechanic Dashboard - <span style='color: black;'>{source_name}</span>"
        f"</h1>",
        unsafe_allow_html=True
    )

    # Yellow bar with the car icon
    st.markdown("""
    <div class='yellow-bar'>
        <div class='car-icon'></div>
    </div>
    """, unsafe_allow_html=True)


    # Check if the necessary columns exist in the data
    required_columns = ["Source Name", "Registration ID", "City", "Service Name", "Car Name", "Customer Name", "Car Model",
                        "Car Odometer", "Car No", "Mobile No", "Invoice Link", "Delivered Date"]
    if not all(col in data.columns for col in required_columns):
        st.markdown("<p class='error'>Some required columns are missing in the data.</p>", unsafe_allow_html=True)
        return

    # Filter data for the logged-in source name
    data_filter = data[data["Source Name"].str.lower() == source_name]

    if data_filter.empty:
        st.markdown("<p class='warning'>No data available for this user.</p>", unsafe_allow_html=True)
        return

    # Display basic stats
    st.markdown("<div class='order-stats'>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-box'>Total Orders: {data_filter['Registration ID'].count()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-box'>Total Repeat Orders: {data_filter['Car No'].duplicated().sum()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-box'>Working Cities: {data_filter['City'].nunique()}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Search for an Order ID
    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    order_ids = data_filter["Car No"].unique()
    order_id_search = st.selectbox("Search Registration No", options=["Select a Registration No"] + list(order_ids))
    st.markdown("</div>", unsafe_allow_html=True)

    if order_id_search != "Select a Registration No":
        # Check if the entered Order ID exists
        order_details = data_filter[data_filter["Car No"] == order_id_search]

        if not order_details.empty:
            st.subheader(f"Order Details for Registration No: {order_id_search}")
            for index, row in order_details.iterrows():
                st.markdown(f"""
                <div class='order-details'>
                    <h4>Car Name: <span class='highlight'>{row['Car Name']}</span></h4>
                    <p><b>Customer Name:</b> {row['Customer Name']}</p>
                    <p><b>Delivered Date:</b> <span class='highlight'>{row['Delivered Date']}</span></p>
                    <p><b>Car Odometer:</b> {row['Car Odometer']} KM</p>
                    <p><b>Car No:</b> {row['Car No']}</p>
                    <p><b>Mobile No:</b> {row['Mobile No']}</p>
                    <p><b>Service Name:</b> {row['Service Name']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Display the Invoice Download Button
                if pd.notna(row['Invoice Link']):
                    st.download_button(
                        label="Download Invoice",
                        data=row['Invoice Link'],  # Assuming this is a file link
                        file_name=f"Invoice_{order_id_search}.pdf",  # Adjust the file extension based on the file type
                        mime="application/pdf",  # Change MIME type based on file format
                        key=f"download_button_{order_id_search}_{index}"  # Unique key for each button
                    )
        else:
            st.markdown(f"<p class='warning'>No details found for Registration ID: {order_id_search}</p>", unsafe_allow_html=True)
