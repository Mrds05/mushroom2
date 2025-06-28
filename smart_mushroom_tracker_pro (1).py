
# Smart Mushroom Growth Tracker Pro with IoT integration and remote sensor support

import streamlit as st
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
import random
from PIL import Image
import io
import json

st.set_page_config(page_title="Smart Mushroom Growth Tracker", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard", "New Log Entry", "Visual Trends",
    "Logbook", "Export Report", "Sensor Readings", "AI Photo Check"
])

if "data" not in st.session_state:
    st.session_state.data = []

if "temp_threshold" not in st.session_state:
    st.session_state.temp_threshold = 30
if "humidity_threshold" not in st.session_state:
    st.session_state.humidity_threshold = 80

with st.sidebar.expander("⚙️ Alert Settings"):
    st.session_state.temp_threshold = st.number_input("Max Temp (°C)", value=st.session_state.temp_threshold)
    st.session_state.humidity_threshold = st.number_input("Min Humidity (%)", value=st.session_state.humidity_threshold)

# EXTRA: IoT data source selector
st.sidebar.subheader("🔌 IoT Sensor Data Source")
data_source = st.sidebar.radio("Choose data source:", ["Manual Entry", "Local File", "Remote URL"])

sensor_data = {"Temperature": None, "Humidity": None}

if data_source == "Local File":
    local_path = st.sidebar.text_input("📁 Local JSON path", "sensor_data.json")
    try:
        with open(local_path, "r") as f:
            json_data = json.load(f)
            if isinstance(json_data, list) and len(json_data) > 0:
               latest = json_data[-1]  # Get most recent day's data
               sensor_data["Temperature"] = latest.get("temperature")
               sensor_data["Humidity"] = latest.get("humidity")
            elif isinstance(json_data, dict):
               sensor_data["Temperature"] = json_data.get("temperature")
               sensor_data["Humidity"] = json_data.get("humidity")

    except Exception as e:
        st.sidebar.error(f"Error reading local file: {e}")

elif data_source == "Remote URL":
    import requests
    remote_url = st.sidebar.text_input("🌐 Remote API URL", "https://your-device-url/data.json")
    try:
        response = requests.get(remote_url, timeout=5)
        if response.status_code == 200:
            json_data = response.json()
            sensor_data["Temperature"] = json_data.get("temperature")
            sensor_data["Humidity"] = json_data.get("humidity")
        else:
            st.sidebar.error(f"HTTP {response.status_code}: Unable to fetch data")
    except Exception as e:
        st.sidebar.error(f"Connection error: {e}")

def get_sensor_data():
    return {
        "Temperature": round(random.uniform(25, 32), 1),
        "Humidity": round(random.uniform(75, 95), 1)
    }

def ai_check_image(image):
    return "✅ Healthy growth detected (simulated)."

if page == "Dashboard":
    st.title("📊 Smart Mushroom Growth Tracker")
    if st.session_state.data:
        latest = st.session_state.data[-1]
        st.metric("🌡️ Temperature", f"{latest['Temperature']}°C")
        st.metric("💧 Humidity", f"{latest['Humidity']}%")
        st.write(f"**Stage:** {latest['Growth Stage']}")
        st.write(f"**Notes:** {latest['Notes']}")
    else:
        st.info("No logs yet.")

elif page == "New Log Entry":
    st.title("📝 New Growth Log")
    with st.form("log_form"):
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", value=date.today())
            temp = st.number_input("Temperature (°C)", step=0.1)
        with col2:
            humidity = st.number_input("Humidity (%)", step=0.1)
            stage = st.selectbox("Growth Stage", ["Mycelium", "Pinhead", "Fruiting", "Mature", "Harvested"])
        notes = st.text_area("Notes")
        photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Submit")
        if submit:
            st.session_state.data.append({
                "Date": entry_date,
                "Temperature": temp,
                "Humidity": humidity,
                "Growth Stage": stage,
                "Notes": notes,
                "Photo": photo
            })
            st.success("Log added successfully.")
            if temp > st.session_state.temp_threshold:
                st.error("⚠️ High temperature!")
            if humidity < st.session_state.humidity_threshold:
                st.warning("⚠️ Low humidity!")

elif page == "Visual Trends":
    st.title("📈 Growth Analytics")
    if not st.session_state.data:
        st.warning("No data to visualize.")
    else:
        df = pd.DataFrame(st.session_state.data)
        df["Date"] = pd.to_datetime(df["Date"])
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Temperature"], label="Temperature (°C)", marker="o")
        ax.plot(df["Date"], df["Humidity"], label="Humidity (%)", marker="x")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

elif page == "Logbook":
    st.title("📚 Growth Logbook")
    if st.session_state.data:
        for log in st.session_state.data:
            st.markdown(f"**Date:** {log['Date']} | **Stage:** {log['Growth Stage']} | **Temp:** {log['Temperature']}°C | **Humidity:** {log['Humidity']}%")
            st.markdown(f"_Notes: {log['Notes']}_")
            if log["Photo"]:
                st.image(log["Photo"], width=300)
            st.markdown("---")
    else:
        st.info("No entries yet.")

elif page == "Export Report":
    st.title("📤 Export Logs")
    if st.session_state.data:
        df_export = pd.DataFrame([{
            "Date": d["Date"],
            "Temperature": d["Temperature"],
            "Humidity": d["Humidity"],
            "Growth Stage": d["Growth Stage"],
            "Notes": d["Notes"]
        } for d in st.session_state.data])
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="growth_log.csv", mime="text/csv")
    else:
        st.warning("No data available to export.")

elif page == "Sensor Readings":
    st.title("📡 IoT Sensor Readings")
    if data_source == "Manual Entry":
        sensor_data = get_sensor_data()
    if sensor_data["Temperature"] is not None and sensor_data["Humidity"] is not None:
        st.metric("Sensor Temperature", f"{sensor_data['Temperature']}°C")
        st.metric("Sensor Humidity", f"{sensor_data['Humidity']}%")
    else:
        st.warning("Sensor data not available.")

elif page == "AI Photo Check":
    st.title("🧠 AI Image Detection (Demo)")
    uploaded_img = st.file_uploader("Upload a mushroom photo to analyze", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Uploaded Image", width=300)
        result = ai_check_image(uploaded_img)
        st.success(result)
