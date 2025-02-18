import streamlit as st
import pandas as pd
import random
import time

# Default login credentials
USERNAME = "admin"
PASSWORD = "password"

# Sidebar login
st.sidebar.title("Login")
username = st.sidebar.text_input("Username", value="", placeholder="Enter username")
password = st.sidebar.text_input("Password", type="password", value="", placeholder="Enter password")
login_button = st.sidebar.button("Login")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if login_button:
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = True
        st.sidebar.success("Login Successful!")
    else:
        st.sidebar.error("Invalid Credentials")

# If not logged in, stop execution
if not st.session_state.authenticated:
    st.warning("Please log in to access the dashboard.")
    st.stop()

# Main content after login
st.title("IoT Sensor Dashboard")
tabs = st.tabs(["Dashboard", "Settings", "About"])

# Generate random data for demonstration
@st.cache_data
def get_data():
    return pd.DataFrame(
        {
            "Time": pd.date_range(start=pd.Timestamp.now(), periods=10, freq="S"),
            "Temperature": [random.uniform(20, 35) for _ in range(10)],
            "Humidity": [random.uniform(40, 80) for _ in range(10)],
            "Moisture": [random.uniform(10, 50) for _ in range(10)],
        }
    )

# Tab 1: Dashboard
with tabs[0]:
    st.subheader("Live Sensor Data")
    chart_data = get_data()
    st.line_chart(chart_data.set_index("Time"))
    
    # Show last sensor data in circles
    last_data = chart_data.iloc[-1]
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Temperature", value=f"{last_data['Temperature']:.2f}°C")
    with col2:
        st.metric(label="Humidity", value=f"{last_data['Humidity']:.2f}%")
    with col3:
        st.metric(label="Moisture", value=f"{last_data['Moisture']:.2f}%")

# Tab 2: Settings
with tabs[1]:
    st.subheader("Settings")
    st.write("Configuration options go here.")

# Tab 3: About
with tabs[2]:
    st.subheader("About")
    st.write("This dashboard visualizes IoT sensor data for temperature, humidity, and moisture.")
