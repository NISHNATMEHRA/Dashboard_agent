import streamlit as st
from streamlit_option_menu import option_menu
from google_sheets import connect_to_sheet
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="GoMechanic Dashboard",
    page_icon="🚗",
    layout="wide",
)

# Load Google Sheets data
json_keyfile = 'agents_keys'
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1nN11gQ_F38CdjC7Wd0X0tj8ZRY6qgU-cGB9PZ24twc0/edit?gid=0#gid=0"
sheet_name = "test sheet"

# Fetch data from Google Sheets
try:
    data = connect_to_sheet(json_keyfile, spreadsheet_url, sheet_name)
except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")
    data = pd.DataFrame()

# Session state for login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "source_name" not in st.session_state:
    st.session_state["source_name"] = ""

# Background image styling
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("file:///<absolute-path-to-your-image>");
    background-size: cover;
    background-position: center;
}}
[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Login form for users
if not st.session_state["logged_in"]:
    st.title("🔒 Login")
    st.subheader("Welcome to GoMechanic Dashboard")

    # Streamlit Login Form
    with st.form("login_form"):
        source_name = st.text_input("Enter Source Name")
        password = st.text_input("Enter Password", type="password")
        submit_button = st.form_submit_button("Login")

        source_name = source_name.lower()
        password = password.lower()


    if submit_button:
        if data.empty:
            st.error("User data is not properly loaded or missing required columns.")
        else:
            # Validate user credentials
            is_valid_user = (data[(data["Source Name"].str.lower() == source_name) & (data["Password"].str.lower() == password)].any()).any()

            # Validate owner credentials (if applicable)
            is_owner = (
                data[(data["Source Name"].str.lower() == source_name) & (data["owner_password"].str.lower() == password)].any()).any()

            if is_valid_user:
                st.session_state["logged_in"] = True
                st.session_state["source_name"] = source_name
                st.session_state["Password"] = password
                st.success("Login Successful! Redirecting...")
                st.rerun()
            elif is_owner:
                st.session_state["logged_in"] = True
                st.session_state["source_name"] = source_name
                st.session_state["owner_password"] = password
                st.success("Owner Login Successful! Redirecting...")
                st.rerun()
            else:
                st.error("Incorrect Source Name or Password. Please try again.")

# Menu logic based on login type
if st.session_state.get("logged_in"):
    with st.sidebar:
        # Styled title for the sidebar
        st.markdown(
            '''<h1><span style="color:red; font-size: 40px; font-weight: bold;">Go</span><span style="font-size: 40px;">Mechanic</span> 🚗</h1>''',
            unsafe_allow_html=True
        )

        # Menu options based on user type (owner or regular user)
        if "owner_password" in st.session_state:
            menu_options = ["Home", "Dashboard", "Analytics", "Show Data", "Bill Data", "Logout"]
        elif "Password" in st.session_state:
            menu_options = ["Home", "Dashboard", "Analytics", "Show Data", "Logout"]
        else:
            menu_options = []

        # Streamlit option menu
        app = option_menu(
            menu_title="GoMechanic",
            options=menu_options,
            icons=["house-fill", "person-circle", "trophy-fill", "chat-fill", "sign-out"],
            menu_icon="chat-text-fill",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color": "white", "font-size": "23px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "blue",
                },
                "nav-link-selected": {"background-color": "#02ab21"},
                "menu-title": {
                    "color": "white",
                    "font-size": "30px",
                    "font-weight": "bold",
                },
            },
        )

    # Define menu pages
    if app == "Home":
        import show_home
        show_home.show_home()

    elif app == "Dashboard":
        import dashboard
        dashboard.show(st.session_state["source_name"], data)

    elif app == "Analytics":
        import analytics
        analytics.show(st.session_state["source_name"], data)

    elif app == "Show Data":
        import show_data
        show_data.show(st.session_state["source_name"], data)

    elif app == "Bill Data" and "owner_password" in st.session_state:
        import bill_data
        bill_data.show(st.session_state["source_name"], st.session_state["owner_password"], data)


    elif app == "Logout":
        # Reset session state
        st.session_state["logged_in"] = False
        st.session_state["source_name"] = ""
        st.session_state.pop("owner_password", None)
        st.rerun()
