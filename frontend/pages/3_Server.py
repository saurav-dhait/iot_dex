import streamlit as st
import psutil
import matplotlib.pyplot as plt
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.title("System Performance Metrics")
auto_refresh = st.checkbox("Auto-refresh every 2 seconds", value=True)

for metric in ["cpu", "ram", "disk_read", "disk_write", "swap_usage", "cpu_freq", "load_avg"]:
    if metric not in st.session_state:
        st.session_state[metric] = []

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
ram_percent = ram.percent
ram_used = ram.used / (1024**3)
ram_total = ram.total / (1024**3)
ram_str = f"{ram_used:.1f} / {ram_total:.1f} GB"

disk_io_counters = psutil.disk_io_counters()
read_bytes = disk_io_counters.read_bytes
write_bytes = disk_io_counters.write_bytes

if "prev_read_bytes" in st.session_state and "prev_write_bytes" in st.session_state:
    read_diff = read_bytes - st.session_state.prev_read_bytes
    write_diff = write_bytes - st.session_state.prev_write_bytes
    disk_read_speed = read_diff / (1024**2)
    disk_write_speed = write_diff / (1024**2)
else:
    disk_read_speed = 0.0
    disk_write_speed = 0.0

st.session_state.prev_read_bytes = read_bytes
st.session_state.prev_write_bytes = write_bytes

st.session_state.cpu.append(cpu)
st.session_state.ram.append(ram_percent)
st.session_state.disk_read.append(disk_read_speed)
st.session_state.disk_write.append(disk_write_speed)

swap = psutil.swap_memory()
swap_percent = swap.percent
st.session_state.swap_usage.append(swap_percent)

cpu_frequency = psutil.cpu_freq().current
st.session_state.cpu_freq.append(cpu_frequency)

try:
    load_average = psutil.getloadavg()[0]
except Exception:
    load_average = 0.0
st.session_state.load_avg.append(load_average)

max_points = 30
for metric in ["cpu", "ram", "disk_read", "disk_write", "swap_usage", "cpu_freq", "load_avg"]:
    if len(st.session_state[metric]) > max_points:
        st.session_state[metric] = st.session_state[metric][-max_points:]

def plot_usage(title, data1, data2, color1, color2, y_label, y_max=100):
    fig, ax = plt.subplots()
    x = np.arange(len(data1))
    ax.plot(x, np.array(data1), color=color1, linewidth=3, label="Primary")
    if data2:
        ax.plot(x, np.array(data2), color=color2, linewidth=3, label="Secondary")
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    ax.set_xlabel("Time (refreshes)", color="white")
    ax.set_ylabel(y_label, color="white")
    ax.set_title(title, color="white")
    ax.set_ylim(0, y_max)
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.legend(facecolor="black", edgecolor="white", fontsize=10, loc="upper left")
    st.pyplot(fig)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("CPU Usage", f"{cpu:.1f}%")
    plot_usage("CPU Usage", st.session_state.cpu, [], "#39FF14", "", "Usage (%)")
with col2:
    st.metric("RAM Usage", ram_str)
    plot_usage("RAM Usage", st.session_state.ram, [], "#FF073A", "", "Usage (%)")
with col3:
    st.metric("Disk Write", f"{disk_write_speed:.2f} MB/s")
    plot_usage("Disk I/O Speed", st.session_state.disk_read, st.session_state.disk_write, "#0BF1A0", "#F0F0F0", "Speed (MB/s)")

st.markdown("## Additional Metrics")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Swap Usage", f"{swap_percent:.1f}%")
    plot_usage("Swap Usage", st.session_state.swap_usage, [], "#FF5733", "", "Usage (%)")

with col5:
    st.metric("CPU Frequency", f"{cpu_frequency:.1f} MHz")
    max_cpu_freq = max(st.session_state.cpu_freq + [cpu_frequency])
    plot_usage("CPU Frequency", st.session_state.cpu_freq, [], "#FFD700", "", "Frequency (MHz)", y_max=max_cpu_freq * 1.1)

with col6:
    st.metric("Load Average (1-min)", f"{load_average:.2f}")
    y_max_load = max(st.session_state.load_avg + [1])
    plot_usage("Load Average", st.session_state.load_avg, [], "#98FB98", "", "Load", y_max=y_max_load * 1.1)

if auto_refresh:
    st_autorefresh(interval=2000, key="perf_refresh")
