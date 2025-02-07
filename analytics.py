import streamlit as st
import altair as alt
import pandas as pd

# Add custom HTML for style (without animations)
custom_html = """
<style>
    .stTitle {
        font-family: 'Arial Black', Gadget, sans-serif;
        text-align: center;
        padding: 15px;
        font-size: 36px;
        color: #34495e;
    }

    .stSubheader {
        color: #34495e;
        font-weight: bold;
        font-family: 'Verdana', Geneva, sans-serif;
        text-align: center;
    }

    .metric-box {
        background-color: #ecf0f1;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        color: #2c3e50;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
</style>
"""

def show(source_name, data):
    st.markdown(custom_html, unsafe_allow_html=True)
    st.markdown(f"<h1 class='stTitle'>Analytics Dashboard - {source_name}</h1>", unsafe_allow_html=True)
    source_name = source_name.lower()
    # Filter data for the logged-in source name
    data_filter = data[data["Source Name"].str.lower() == source_name]

    if data_filter.empty:
        st.warning("No data available for this user.")
        return

    # Example: Show top cities by order count
    city_data = data_filter.groupby("City")["Registration ID"].count().reset_index()
    city_data = city_data.sort_values(by="Registration ID", ascending=False)
    city_chart = alt.Chart(city_data).mark_bar().encode(
        x=alt.X('City', sort=None, axis=alt.Axis(title="City", labelAngle=0)),
        y=alt.Y('Registration ID', axis=alt.Axis(title="Total Orders")),
        color=alt.Color('City', legend=alt.Legend(title="City")),
        tooltip = ['City', 'Registration ID']
    ).properties(
        title="Top Cities by Order Count",
        width=500,
        height=400
    ).configure_title(
        fontSize=20,
        font='Verdana',
        anchor='middle',
        color='#34495e'
    )
    st.altair_chart(city_chart, use_container_width=True)

    # Example: Show top services by order count
    service_data = data_filter.groupby("Service Name")["Registration ID"].count().reset_index()
    service_data = service_data.sort_values(by="Registration ID", ascending=False)
    service_chart = alt.Chart(service_data).mark_bar().encode(
        x=alt.X('Service Name', sort=None, axis=alt.Axis(title="Service Name", labelAngle=0)),
        y=alt.Y('Registration ID', axis=alt.Axis(title="Total Orders")),
        color=alt.Color('Service Name', legend=alt.Legend(title="Service Name")),
        tooltip=['Service Name', 'Registration ID']
    ).properties(
        title="Top Services by Order Count",
        width=500,
        height=400
    ).configure_title(
        fontSize=20,
        font='Verdana',
        anchor='middle',
        color='#34495e'
    )
    st.altair_chart(service_chart, use_container_width=True)

    # Example: Show total orders and repeat orders
    total_orders = data_filter['Registration ID'].count()
    repeat_orders = data_filter['Car No'].duplicated().sum()
    repeat_percentage = (repeat_orders / total_orders) * 100 if total_orders > 0 else 0
    st.markdown(f"""
    <div class="metric-box">
        <h3>Total Orders:</h3>
        <p>{total_orders}</p>
    </div>
    <div class="metric-box">
        <h3>Repeat Orders:</h3>
        <p>{repeat_orders} ({repeat_percentage:.2f}% of total orders)</p>
    </div>
    """, unsafe_allow_html=True)
