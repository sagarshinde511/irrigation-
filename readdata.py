import streamlit as st
import pandas as pd
import mysql.connector
import time
import plotly.express as px

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
        cursor.execute("SELECT id, dateTime, temp, humi, moi FROM Irrigation ORDER BY id DESC LIMIT 1")
        latest_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return latest_data
    except mysql.connector.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Function to fetch all sensor data
def fetch_all_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT dateTime, temp, humi, moi FROM Irrigation ORDER BY dateTime ASC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data)
    except mysql.connector.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Main content after login
st.title("IoT Sensor Dashboard")
tabs = st.tabs(["Dashboard", "All Data", "About"])

# Tab 1: Dashboard
with tabs[0]:
    st.subheader("Live Sensor Data")
    latest_data = fetch_latest_data()
    
    if latest_data:
        st.write(f"**Latest Data Timestamp:** {latest_data['dateTime']}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Temperature", value=f"{latest_data['temp']}°C")
        with col2:
            st.metric(label="Humidity", value=f"{latest_data['humi']}%")
        with col3:
            st.metric(label="Moisture", value=f"{latest_data['moi']}%")
    else:
        st.error("Failed to fetch latest sensor data.")

# Tab 2: All Data
with tabs[1]:
    st.subheader("Past Sensor Data Visualization")
    data = fetch_all_data()
    
    if data is not None and not data.empty:
        st.write("### Raw Data")
        st.dataframe(data)
        
        st.write("### Sensor Data Trends")
        fig_temp = px.line(data, x='dateTime', y='temp', title='Temperature Over Time', labels={'temp': 'Temperature (°C)', 'dateTime': 'Timestamp'})
        st.plotly_chart(fig_temp, use_container_width=True)
        
        fig_humi = px.line(data, x='dateTime', y='humi', title='Humidity Over Time', labels={'humi': 'Humidity (%)', 'dateTime': 'Timestamp'})
        st.plotly_chart(fig_humi, use_container_width=True)
        
        fig_moi = px.line(data, x='dateTime', y='moi', title='Moisture Over Time', labels={'moi': 'Moisture (%)', 'dateTime': 'Timestamp'})
        st.plotly_chart(fig_moi, use_container_width=True)
    else:
        st.error("No data available to display.")

# Tab 3: About
with tabs[2]:
    st.subheader("About")
    st.write("This dashboard visualizes IoT sensor data for temperature, humidity, and moisture.")
