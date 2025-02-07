import streamlit as st
import pandas as pd
from datetime import datetime

# Function to get the current time of day
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

# Enhanced Home Page
def show_home():
    # Styled GoMechanic branding
    styled_header = '''
        <div style="display: flex; justify-content: center; align-items: center; background-color: #2c3e50; padding: 20px; border-radius: 10px; position: relative;">
            <h1 style="margin: 0; display: flex; justify-content: center; color: white;">
                <span style="color: red; font-size: 40px; font-weight: bold;">Go</span>
                <span style="color: white; font-size: 40px;">Mechanic🚗</span>
            </h1>
            <p style="font-size: 15px; color: #ecf0f1; font-style: italic; position: absolute; right: 15px;">Your Trusted Car Care Partner</p>
        </div>
    '''
    st.markdown(styled_header, unsafe_allow_html=True)

    # Greeting with dynamic time of day
    st.markdown(f"""
    <div style='background-color: #f1c40f; padding: 15px; border-radius: 10px; text-align: center;'>
        <h2 style='color: #34495e; font-size: 20px;'>{get_greeting()}! Welcome to the 
        <span style='color: red;'>Go</span><span style='color: black;'>Mechanic</span> Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

    # Motivational tagline
    st.markdown(
        "<blockquote style='font-size: 18px; color: #7f8c8d;'>"
        "🚘 'Transforming car service and repair for the better, one vehicle at a time!'</blockquote>",
        unsafe_allow_html=True,
    )

    # Achievements section
    st.markdown("<h2 style='color: #e67e22;'>🌟 Achievements</h2>", unsafe_allow_html=True)
    achievements = [
        "Over <span style='color: #2ecc71; font-weight: bold;'>20 million+</span> satisfied customers across India.",
        "Over <span style='color: #9b59b6; font-weight: bold;'>5 million+</span> Playstore app download across India.",
        "Partnered with <span style='color: #3498db; font-weight: bold;'>2100+ certified garages</span> nationwide.",
        "Rated <span style='color: #f1c40f; font-weight: bold;'>4.5/5</span> by customers on major platforms.",
        "Save Upto <span style='color: #e74c3c; font-weight: bold;'>₹17500</span> Annually on Gomechanic membership.",
        "<span style='color: #9b59b6; font-weight: bold;'>18388</span> users have joined Miles last month.",
        "Save Upto <span style='color: #f1c40f; font-weight: bold;'>40%</span> for authorized car service.",

    ]
    for achievement in achievements:
        st.markdown(f"- {achievement}", unsafe_allow_html=True)

    # Key Metrics
    st.markdown("<h2 style='color: #2980b9;'>📈 Key Metrics</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <span style='color: #16a085; font-size: 20px; font-weight: bold;'>Total Customers</span><br>
            <span style='color: #34495e; font-size: 24px;'>20M+</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <span style='color: #e67e22; font-size: 20px; font-weight: bold;'>Certified Garages</span><br>
            <span style='color: #34495e; font-size: 24px;'>2100+</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <span style='color: #f39c12; font-size: 20px; font-weight: bold;'>Average Rating</span><br>
            <span style='color: #34495e; font-size: 24px;'>4.5/5</span>
        </div>
        """, unsafe_allow_html=True)

    # Contact Information
    st.markdown("<h2 style='color: #8e44ad;'>📞 Contact Us</h2>", unsafe_allow_html=True)
    contact_info = '''
    <div style="background-color: #ecf0f1; padding: 20px; border-radius: 10px;">
        <p style="color: #34495e; font-size: 18px;">For support or inquiries, reach out to us at:</p>
        <ul style="color: #7f8c8d;">
            <li>Email: <a href="mailto:support@gomechanic.com" style="color: #3498db;">support@gomechanic.com</a></li>
            <li>Phone: <span style="color: #e74c3c;">+91-999-999-9999</span></li>
        </ul>
    </div>
    '''
    st.markdown(contact_info, unsafe_allow_html=True)
