import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")

st.title("🛰️ Welcome to IOT DEX — Control. Connect. Create.")
st.subheader("Welcome User!")
st.markdown("---")

header_col1, header_col2, header_col3 = st.columns(3, gap="large")

with header_col1:
    st.markdown("### ✨ **One Place for IoT** ✨")

with header_col2:
    st.markdown("### 📱 **Access From All Devices** 📱")

with header_col3:
    st.markdown("### 📊 **Intuitive Smart Charts** 📊")

st.markdown("---")

anim_col1, anim_col2, anim_col3 = st.columns(3, gap="large")

with anim_col1:
    url = requests.get("https://lottie.host/742ebad6-ab23-403e-af13-a9db72fb3d45/QSxrjG5Wjh.json")
    if url.status_code == 200:
        st_lottie(url.json(), height=300)
    else:
        st.error("Error loading animation")

with anim_col2:
    url = requests.get("https://lottie.host/a3b1bc59-fca4-40e9-8756-2538e51615b8/kk0rt4sMGv.json")
    if url.status_code == 200:
        st_lottie(url.json(), height=300)
    else:
        st.error("Error loading animation")

with anim_col3:
    url = requests.get("https://lottie.host/cbed841b-c317-4fec-b00c-784bd386707b/0BoUw1ujo9.json")
    if url.status_code == 200:
        st_lottie(url.json(), height=300)
    else:
        st.error("Error loading animation")
