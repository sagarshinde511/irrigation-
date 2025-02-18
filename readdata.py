import streamlit as st
import pandas as pd
import mysql.connector
import random
import time

# Database credentials
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1"
}

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

# Function to fetch latest sensor data
def fetch_latest_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, time, dateTemp, humi, moi FROM Irrigation ORDER BY id DESC LIMIT 1")
        latest_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return latest_data
    except mysql.connector.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Main content after login
st.title("IoT Sensor Dashboard")
tabs = st.tabs(["Dashboard", "Settings", "About"])

# Tab 1: Dashboard
with tabs[0]:
    st.subheader("Live Sensor Data")
    latest_data = fetch_latest_data()
    
    if latest_data:
        st.write(f"**Latest Data Timestamp:** {latest_data['time']}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Temperature", value=f"{latest_data['temp']}°C")
        with col2:
            st.metric(label="Humidity", value=f"{latest_data['humi']}%")
        with col3:
            st.metric(label="Moisture", value=f"{latest_data['moi']}%")
    else:
        st.error("Failed to fetch latest sensor data.")

# Tab 2: Settings
with tabs[1]:
    st.subheader("Settings")
    st.write("Configuration options go here.")

# Tab 3: About
with tabs[2]:
    st.subheader("About")
    st.write("This dashboard visualizes IoT sensor data for temperature, humidity, and moisture.")
