# dashboard.py
import streamlit as st
import time
import math
import random

# Page configuration
st.set_page_config(page_title="Health Dashboard", page_icon="🏥", layout="wide")

# Title and description
st.title("🏥 Virtual Health Monitoring Dashboard")
st.markdown("""
This dashboard simulates real-time health sensor data including heart rate, body temperature, 
and oxygen saturation. The data includes realistic variations and medical alert systems.
""")
st.markdown("---")

# Initialize session state to store our data
if 'heart_rate' not in st.session_state:
    st.session_state.heart_rate = []
if 'temperature' not in st.session_state:
    st.session_state.temperature = []
if 'oxygen' not in st.session_state:
    st.session_state.oxygen = []
if 'ai_report' not in st.session_state:
    st.session_state.ai_report = "Waiting for data to generate health summary..."
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'x' not in st.session_state:
    st.session_state.x = 0

# Sidebar with controls
with st.sidebar:
    st.header("🕹️ Controls")
    st.markdown("---")
    
    if not st.session_state.simulation_running:
        if st.button("▶️ Start Simulation", type="primary", use_container_width=True):
            st.session_state.simulation_running = True
            st.rerun()
    else:
        if st.button("⏹️ Stop Simulation", type="secondary", use_container_width=True):
            st.session_state.simulation_running = False
            st.rerun()
    
    st.markdown("---")
    st.subheader("ℹ️ Normal Ranges")
    st.info("""
    - **Heart Rate**: 60-100 bpm
    - **Temperature**: 36.1-37.8 °C  
    - **Oxygen (SpO2)**: 95-100%
    """)

# Medical alert logic (from Fatima's specifications)
def check_vital_status(hr, temp, oxy):
    """Check if vitals are normal, warning, or critical"""
    status = {"hr": "normal", "temp": "normal", "oxy": "normal"}
    
    # Heart rate checks
    if hr < 60:
        status["hr"] = "critical"
    elif hr < 65:
        status["hr"] = "warning"
    elif hr > 100:
        status["hr"] = "critical"
    elif hr > 95:
        status["hr"] = "warning"
    
    # Temperature checks
    if temp < 36.0:
        status["temp"] = "critical"
    elif temp < 36.1:
        status["temp"] = "warning"
    elif temp > 37.8:
        status["temp"] = "critical"
    elif temp > 37.5:
        status["temp"] = "warning"
    
    # Oxygen checks
    if oxy < 90:
        status["oxy"] = "critical"
    elif oxy < 95:
        status["oxy"] = "warning"
    
    return status

# Generate realistic sensor data with slight variations
def generate_sensor_data():
    """Generate realistic health sensor data with smooth variations"""
    st.session_state.x += 1
    
    # Heart Rate: Sine wave pattern around 72 bpm ± 15 bpm
    base_hr = 72
    variation = math.sin(st.session_state.x / 6) * 8 + random.uniform(-3, 3)
    heart_rate = int(base_hr + variation)
    
    # Temperature: Very slow drift around 36.6°C ± 0.3°C
    base_temp = 36.6
    temp_drift = math.sin(st.session_state.x / 30) * 0.2 + random.uniform(-0.1, 0.1)
    temperature = round(base_temp + temp_drift, 1)
    
    # Oxygen: Mostly stable with occasional small variations
    oxygen = 97 + random.randint(-2, 2)
    oxygen = max(90, min(100, oxygen))  # Keep between 90-100%
    
    return heart_rate, temperature, oxygen

# Main dashboard layout
header = st.container()
charts_col1, charts_col2 = st.columns(2)
report_section = st.container()

# Display current metrics
with header:
    st.subheader("📊 Current Vital Signs")
    
    if st.session_state.heart_rate:
        latest_hr = st.session_state.heart_rate[-1]
        latest_temp = st.session_state.temperature[-1]
        latest_oxy = st.session_state.oxygen[-1]
        
        vital_status = check_vital_status(latest_hr, latest_temp, latest_oxy)
        
        col1, col2, col3 = st.columns(3)
        
        # Heart Rate metric with color coding
        with col1:
            if vital_status["hr"] == "critical":
                st.error(f"❤️ Heart Rate: {latest_hr} bpm")
            elif vital_status["hr"] == "warning":
                st.warning(f"❤️ Heart Rate: {latest_hr} bpm")
            else:
                st.success(f"❤️ Heart Rate: {latest_hr} bpm")
        
        # Temperature metric with color coding
        with col2:
            if vital_status["temp"] == "critical":
                st.error(f"🌡️ Temperature: {latest_temp} °C")
            elif vital_status["temp"] == "warning":
                st.warning(f"🌡️ Temperature: {latest_temp} °C")
            else:
                st.success(f"🌡️ Temperature: {latest_temp} °C")
        
        # Oxygen metric with color coding
        with col3:
            if vital_status["oxy"] == "critical":
                st.error(f"💨 SpO2: {latest_oxy}%")
            elif vital_status["oxy"] == "warning":
                st.warning(f"💨 SpO2: {latest_oxy}%")
            else:
                st.success(f"💨 SpO2: {latest_oxy}%")
    else:
        st.info("No data yet. Start the simulation to begin monitoring.")

# Display charts
with charts_col1:
    if st.session_state.heart_rate:
        st.subheader("❤️ Heart Rate Trend")
        st.line_chart(st.session_state.heart_rate)
    
    if st.session_state.temperature:
        st.subheader("🌡️ Temperature Trend")
        st.line_chart(st.session_state.temperature)

with charts_col2:
    if st.session_state.oxygen:
        st.subheader("💨 Oxygen Saturation Trend")
        st.line_chart(st.session_state.oxygen)
        
    # Data table
    if st.session_state.heart_rate:
        st.subheader("📋 Recent Readings")
        recent_data = list(zip(
            st.session_state.heart_rate[-10:],
            st.session_state.temperature[-10:],
            st.session_state.oxygen[-10:]
        ))
        st.table(recent_data)

# AI Report section
with report_section:
    st.markdown("---")
    st.subheader("🤖 AI Health Summary")
    
    if st.session_state.heart_rate:
        # Simple rule-based report until AI integration
        latest_hr = st.session_state.heart_rate[-1]
        latest_temp = st.session_state.temperature[-1]
        latest_oxy = st.session_state.oxygen[-1]
        
        status = check_vital_status(latest_hr, latest_temp, latest_oxy)
        
        if all(s == "normal" for s in status.values()):
            report = "All vital signs are within normal ranges. Your health metrics look excellent! Maintain your current routine."
        else:
            alerts = []
            if status["hr"] != "normal":
                alerts.append(f"Heart rate is {'too low' if latest_hr < 60 else 'too high'}")
            if status["temp"] != "normal":
                alerts.append(f"Temperature is {'too low' if latest_temp < 36.1 else 'too high'}")
            if status["oxy"] != "normal":
                alerts.append(f"Oxygen level is low")
            
            report = f"Note: {', '.join(alerts)}. Please monitor these values closely."
        
        st.session_state.ai_report = report
    
    st.info(st.session_state.ai_report)

# Main simulation loop
if st.session_state.simulation_running:
    # Generate new data
    new_hr, new_temp, new_oxy = generate_sensor_data()
    
    # Add to history (keep last 50 readings)
    st.session_state.heart_rate.append(new_hr)
    st.session_state.temperature.append(new_temp)
    st.session_state.oxygen.append(new_oxy)
    
    if len(st.session_state.heart_rate) > 50:
        st.session_state.heart_rate = st.session_state.heart_rate[-50:]
        st.session_state.temperature = st.session_state.temperature[-50:]
        st.session_state.oxygen = st.session_state.oxygen[-50:]
    
    # Wait a bit before next update
    time.sleep(1.5)
    st.rerun()

# Footer
st.markdown("---")
st.caption(" Virtual Health Monitoring System ")
