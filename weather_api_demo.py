import os
import requests

api_key = os.getenv("OPENWEATHER_API_KEY")

city = "Hamilton"

if not api_key:
    print("API key not set")
    exit()

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": api_key,
    "units": "metric"
}

response = requests.get(url, params=params)

data = response.json()

print("City:", data["name"])
print("Temperature:", data["main"]["temp"], "C")
print("Condition:", data["weather"][0]["main"])
print("Description:", data["weather"][0]["description"])
print("Wind Speed:", data["wind"]["speed"])