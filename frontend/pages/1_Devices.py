import streamlit as st
import requests
import time
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit_autorefresh import st_autorefresh
import math
st.set_page_config(layout="wide")

DEVICE_1_API_URL = "https://flask-server-pico.onrender.com/metrics"
DEVICE_2_API_URL = "https://flask-server-pico.onrender.com/metrics/zero"
LOTTIE_URL = "https://lottie.host/5dfa764d-70fd-47eb-b024-75c379223348/adZWz7gTjl.json"

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def fetch_device1_metrics():
    try:
        res = requests.get(DEVICE_1_API_URL, timeout=3)
        if res.status_code == 200:
            data = res.json()
            return {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": data["temperature"],
                "voltage": data["voltage"],
                "uptime_sec": data["uptime_sec"],
                "cpu_freq_hz": data["cpu_freq_hz"],
                "free_memory_bytes": data["free_memory_bytes"],
            }
        else:
            st.warning("⚠️ Failed to fetch Device 1 metrics.")
    except Exception as e:
        st.warning(f"⚠️ Device 1 request failed: {e}")
    return None

def fetch_device2_metrics():
    try:
        res = requests.get(DEVICE_2_API_URL, timeout=5)
        if res.status_code == 200:
            return res.json()
        else:
            st.warning("⚠️ Failed to fetch Device 2 metrics.")
    except Exception as e:
        st.warning(f"⚠️ Device 2 request failed: {e}")
    return None

if "metrics_data" not in st.session_state:
    st.session_state.metrics_data = pd.DataFrame(columns=[
        "timestamp", "temperature", "voltage", "uptime_sec", "cpu_freq_hz", "free_memory_bytes"
    ])
if "device2_history" not in st.session_state:
    st.session_state.device2_history = []

tab1, tab2, tab3 = st.tabs(["📟 Device 1", "🧭 Device 2", "🔌 Device 3"])

with tab1:
    st.markdown("<h2 style='text-align:center;'>📟 Device 1 Dashboard</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st_lottie(load_lottie_url(LOTTIE_URL), height=250)
    colA, colB, colC = st.columns([1, 2, 1])
    with colA:
        if st.button("🔄 Refresh Now"):
            new_data = fetch_device1_metrics()
            if new_data:
                st.session_state.metrics_data = pd.concat(
                    [st.session_state.metrics_data, pd.DataFrame([new_data])],
                    ignore_index=True
                )
    with colC:
        auto = st.checkbox("Auto-update every 2s", value=True)

    if auto:
        new_data = fetch_device1_metrics()
        if new_data:
            st.session_state.metrics_data = pd.concat(
                [st.session_state.metrics_data, pd.DataFrame([new_data])],
                ignore_index=True
            )
        st_autorefresh(interval=2000, key="refresh_interval")

    st.markdown("### 📊 Live Metrics")
    if not st.session_state.metrics_data.empty:
        latest = st.session_state.metrics_data.iloc[-1]
        st.info(f"""
        • Temperature: {latest.temperature} °C  
        • Voltage: {latest.voltage} V  
        • Uptime: {latest.uptime_sec} s  
        • CPU Frequency: {latest.cpu_freq_hz / 1_000_000:.2f} MHz  
        • Free Memory: {latest.free_memory_bytes / 1024:.2f} KB  
        """)

        df = st.session_state.metrics_data.set_index("timestamp")

        st.markdown("#### 🌡️ Temperature (°C)")
        st.line_chart(df["temperature"], use_container_width=True)

        st.markdown("#### ⚡ Voltage (V)")
        st.line_chart(df["voltage"], use_container_width=True)

        st.markdown("#### ⏱️ Uptime (Seconds)")
        st.line_chart(df["uptime_sec"], use_container_width=True)

        st.markdown("#### 🧠 Free Memory (Bytes)")
        st.line_chart(df["free_memory_bytes"], use_container_width=True)

        st.markdown("#### 🧮 CPU Frequency (Hz)")
        st.line_chart(df["cpu_freq_hz"], use_container_width=True)
    else:
        st.warning("No data available. Try clicking 'Refresh Now'.")

with tab2:
    st.markdown("<h2 style='text-align:center;'>🧭 Device 2 Dashboard</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st_lottie(load_lottie_url(LOTTIE_URL), height=250)
    colA, colB, colC = st.columns([1, 2, 1])
    with colA:
        if st.button("🔄 Refresh Device 2"):
            device2_data = fetch_device2_metrics()
            if device2_data:
                st.session_state.device2_history.append(device2_data)
    with colC:
        auto2 = st.checkbox("Auto-update every 10s", value=True)

    if auto2:
        device2_data = fetch_device2_metrics()
        if device2_data:
            st.session_state.device2_history.append(device2_data)
        st_autorefresh(interval=2000, key="refresh_device2")

    if st.session_state.device2_history:
        latest2 = st.session_state.device2_history[-1]
        memory_percent = [d["memory"]["percent"] for d in st.session_state.device2_history]
        disk_percent = [d["disk"]["percent"] for d in st.session_state.device2_history]
        st.markdown("### 🧾 Latest Metrics")
        st.info(f"""
        • Hostname: `{latest2['hostname']}`  
        • Platform: `{latest2['platform']}`  
        • CPU Temp: `{latest2['cpu_temp']} °C`  
        • CPU Load: `{latest2['cpu_percent']}%` on {latest2['cpu_cores']} cores  
        • Uptime: `{int(latest2['uptime_seconds'])} s`  
        • Load Avg (1/5/15 min): `{latest2['load_avg']}`
        • Memory Percent: `{memory_percent}%`
        """)


        st.markdown("#### 🧠 Memory Usage (%)")
        st.line_chart(memory_percent)

        st.markdown("#### 💽 Disk Usage (%)")
        st.line_chart(disk_percent)

        st.markdown("#### 📡 Network Bytes Sent / Received")
        net_df = pd.DataFrame({
            "Sent": [n["network"]["bytes_sent"] for n in st.session_state.device2_history],
            "Received": [n["network"]["bytes_recv"] for n in st.session_state.device2_history],
        })
        st.line_chart(net_df)
    else:
        st.warning("No Device 2 data yet. Click refresh or wait for auto-update.")

with tab3:
    st.markdown("<h2 style='text-align:center;'>🔌 Device 3 Dashboard</h2>", unsafe_allow_html=True)
    st.write("Coming soon...")
