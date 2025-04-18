import psutil
import os
import time
import socket
import requests
import platform
import json

API_URL = "https://flask-server-pico.onrender.com/message"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0
        return temp
    except:
        return None

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

def get_metrics():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_temp": get_cpu_temp(),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent,
        },
        "network": psutil.net_io_counters(pernic=False)._asdict(),
        "uptime_seconds": get_uptime(),
        "load_avg": os.getloadavg()
    }

def send_metrics():
    metrics = {"metrics_zero": get_metrics()}
    print(metrics)
    try:
        response = requests.post(API_URL, json=metrics, timeout=10)
        print(f"[+] Sent metrics. Status: {response.status_code}")
    except Exception as e:
        print(f"[!] Error sending metrics: {e}")

if __name__ == "__main__":
    while True:
        send_metrics()
        time.sleep(5)
