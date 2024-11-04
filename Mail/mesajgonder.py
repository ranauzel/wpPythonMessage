import time
import pywhatkit as kit
import requests
from flask import Flask, request, render_template, redirect, url_for
from admin_panel import load_settings, admin_panel_logic

app = Flask(__name__)

# Thingspeak API'den sıcaklık verisini çekme fonksiyonu
import pywhatkit as kit
import requests
from datetime import datetime
import time

def get_temperature():
    try:
        THINGSPEAK_CHANNEL_ID = '2626920'  # Your Thingspeak channel ID
        THINGSPEAK_READ_API_KEY = '**************'  # Your API key
        THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds/last.json?api_key={THINGSPEAK_READ_API_KEY}'

        response = requests.get(THINGSPEAK_URL)
        if response.status_code == 200:
            data = response.json()
            temperature = float(data['field1'])  # Assumes temperature data is under 'field1'
            return temperature
        else:
            print('Thingspeak API çağrısında bir hata oluştu.')
            return None
    except Exception as e:
        print(f"Sıcaklık verisi çekilirken bir hata oluştu: {e}")
        return None

def send_message():
    phone_number = '+9053453863432'
    waiting_time_to_send = 15
    close_tab = True
    waiting_time_to_close = 2

    # Get the current temperature
    temperature = get_temperature()
    if temperature is None:
        print("Sıcaklık verisi alınamadı.")
        return

    # Create message
    message = f"Sıcaklık şu anda {temperature}°C."

    # Get the current time
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    # Set the time for sending the message
    time_hour = current_hour
    time_minute = current_minute + 1  # Set the message to be sent 1 minute later

    # Adjust time if minutes exceed 60
    if time_minute >= 60:
        time_minute -= 60
        time_hour += 1

    # Send a WhatsApp message
    try:
        kit.sendwhatmsg(phone_number, message, time_hour, time_minute, waiting_time_to_send, close_tab, waiting_time_to_close)
        print(f"Message scheduled to be sent at {time_hour}:{time_minute}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Call the function to schedule the message
send_message()



def run_temperature_check():
    while True:
        check_temperature()
        time.sleep(300)  # 5 dakika bekle ve tekrar kontrol et

if __name__ == "__main__":
    # Admin panelini çalıştır
    app.run(debug=True, use_reloader=False)
    # Sıcaklık kontrol fonksiyonunu çalıştır
    run_temperature_check()
