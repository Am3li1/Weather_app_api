import tkinter as tk
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weather(event=None): # Added event=None to handle both button click and <Return> key press
    city = textfield.get()
    # Retrieve API key from environment variable
    api_key = os.getenv("API_KEY") # Assuming your .env has API_KEY="your_api_key_here"

    if not api_key:
        label1.config(text="Error: API Key not found.")
        label2.config(text="Please set API_KEY in your .env file.")
        return

    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        json_data = requests.get(api).json()

        if json_data.get("cod") == "404":
            label1.config(text="City Not Found 🏙️")
            label2.config(text="")
            return
        elif json_data.get("cod") != 200:
            label1.config(text=f"Error: {json_data.get('message', 'Unknown error')}")
            label2.config(text="")
            return

        condition = json_data["weather"][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        
        # OpenWeatherMap provides UTC timestamps, convert to local time.
        # The offset for India (IST) is UTC+5:30.
        # time.gmtime returns struct_time in UTC. Adding 19800 seconds (5.5 hours) converts it to IST.
        # This assumes the system's timezone is not set to IST or handles it correctly.
        # For simplicity and to directly get IST, adding the offset is a straightforward way.
        sunrise_utc_timestamp = json_data['sys']['sunrise']
        sunset_utc_timestamp = json_data['sys']['sunset']
        
        # Convert to IST (UTC + 5 hours 30 minutes = 19800 seconds)
        sunrise_ist = time.strftime("%I:%M:%S %p", time.gmtime(sunrise_utc_timestamp + 19800))
        sunset_ist = time.strftime("%I:%M:%S %p", time.gmtime(sunset_utc_timestamp + 19800))


        final_info = f"{condition} \n{temp}°C"
        final_data = (f"\nMax Temp: {max_temp}°C\nMin Temp: {min_temp}°C"
                      f"\nPressure: {pressure} hPa\nHumidity: {humidity}%"
                      f"\nWind Speed: {wind} m/s\nSunrise: {sunrise_ist}\nSunset: {sunset_ist}")
        
        label1.config(text=final_info)
        label2.config(text=final_data)

    except requests.exceptions.ConnectionError:
        label1.config(text="Network Error 🌐")
        label2.config(text="Please check your internet connection.")
    except Exception as e:
        label1.config(text="An Error Occurred 🐛")
        label2.config(text=f"Details: {e}")


canvas = tk.Tk()
canvas.geometry("600x500")
canvas.title("Weather App ☀️")

f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")

textfield = tk.Entry(canvas, font = t)
textfield.pack(pady = 20)
textfield.focus()
textfield.bind('<Return>', get_weather)

label1 = tk.Label(canvas, font = t)
label1.pack()
label2 = tk.Label(canvas, font = f)
label2.pack()

canvas.mainloop()