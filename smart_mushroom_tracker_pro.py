
import streamlit as st
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
import random
from PIL import Image
import io

# Page config
st.set_page_config(page_title="Smart Mushroom Growth Tracker", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "New Log Entry", "Visual Trends", "Logbook", "Export Report", "Sensor Readings", "AI Photo Check"])

# Session State Initialization
if "data" not in st.session_state:
    st.session_state.data = []

# Alert thresholds
if "temp_threshold" not in st.session_state:
    st.session_state.temp_threshold = 30
if "humidity_threshold" not in st.session_state:
    st.session_state.humidity_threshold = 80

with st.sidebar.expander("⚙️ Alert Settings"):
    st.session_state.temp_threshold = st.number_input("Max Temp (°C)", value=st.session_state.temp_threshold)
    st.session_state.humidity_threshold = st.number_input("Min Humidity (%)", value=st.session_state.humidity_threshold)

# Simulated IoT Sensor (for demo)
def get_sensor_data():
    return {
        "Temperature": round(random.uniform(25, 32), 1),
        "Humidity": round(random.uniform(75, 95), 1)
    }

# AI Image Detection Stub (Placeholder logic)
def ai_check_image(image):
    # Placeholder for AI model result
    return "✅ Healthy growth detected (simulated)."

# Dashboard
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

# New Log Entry
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

# Visual Trends
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

# Logbook
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

# Export Report
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

# Simulated IoT Sensor Readings
elif page == "Sensor Readings":
    st.title("📡 IoT Sensor Readings (Simulated)")
    sensor_data = get_sensor_data()
    st.metric("Sensor Temperature", f"{sensor_data['Temperature']}°C")
    st.metric("Sensor Humidity", f"{sensor_data['Humidity']}%")
    st.success("Simulated real-time data pulled from virtual sensor.")

# AI Image Check
elif page == "AI Photo Check":
    st.title("🧠 AI Image Detection (Demo)")
    uploaded_img = st.file_uploader("Upload a mushroom photo to analyze", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Uploaded Image", width=300)
        result = ai_check_image(uploaded_img)
        st.success(result)
