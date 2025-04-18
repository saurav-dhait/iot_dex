import streamlit as st
import requests

st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align:center;'>📤 Send Message to Device</h2>", unsafe_allow_html=True)
st.markdown("---")

device_options = ["Device 1", "Device 2", "Device 3"]
device = st.selectbox("Select Device:", device_options)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    message = st.text_input("Enter your message:", placeholder="Type your message here...")

    if st.button("📨 Send Message"):
        if message.strip() == "":
            st.warning("⚠️ Please enter a valid message.")
        else:
            try:
                if device == "Device 1":
                    url = "https://flask-server-pico.onrender.com/message"
                elif device == "Device 2":
                    url = "https://flask-server-pico.onrender.com/message"
                elif device == "Device 3":
                    url = "https://flask-server-pico.onrender.com/message"

                payload = {"text": message}
                res = requests.post(url, json=payload, timeout=5)

                if res.status_code == 200:
                    st.success(f"✅ Message sent successfully to {device}!")
                else:
                    st.error(f"❌ Failed to send message to {device}. Status code: {res.status_code}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
