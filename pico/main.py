import network
import urequests
import utime
import machine
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import gc

I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

SSID = 'S20FE'
PASSWORD = 'ypme18900'

FLASK_API_URL = "https://flask-server-pico.onrender.com/message"

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)


def get_metrics():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    voltage = reading
    uptime = utime.ticks_ms() // 1000
    free_mem = gc.mem_free()
    cpu_freq = machine.freq()

    return {
        "temperature": round(temperature, 2),
        "voltage": round(voltage, 2),
        "uptime_sec": uptime,
        "free_memory_bytes": free_mem,
        "cpu_freq_hz": cpu_freq
    }


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    lcd.clear()
    lcd.putstr("Connecting WiFi")
    while not wlan.isconnected():
        utime.sleep(0.5)
        lcd.putstr(".")

    lcd.clear()
    lcd.putstr("WiFi Connected")
    utime.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())


previous_text = ""


def fetch_and_display():
    global previous_text
    try:
        response = urequests.get(FLASK_API_URL)
        data = response.json()
        response.close()

        text = data.get("text", "")
        if text != previous_text:
            lcd.clear()
            lcd.putstr(text[:16])
            if len(text) > 16:
                lcd.move_to(0, 1)
                lcd.putstr(text[16:32])
            previous_text = text
    except Exception as e:
        print("Error:", e)
        lcd.clear()
        lcd.putstr("Request Failed")


def send_metrics():
    metrics = get_metrics()
    payload = {
        "text": previous_text,
        "metrics": metrics
    }
    try:
        response = urequests.post(FLASK_API_URL, json=payload)
        response.close()
    except Exception as e:
        print("Failed to send metrics:", e)


lcd.clear()
connect_to_wifi()
while True:
    fetch_and_display()
    send_metrics()
    utime.sleep(1)

