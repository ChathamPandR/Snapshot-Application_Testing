import requests
from bs4 import BeautifulSoup
from datetime import datetime

# === Config ===
latitude = 35.7202
longitude = -79.1772
usgs_site = "02096960"

# === Load template HTML ===
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# === Get current time ===
now = datetime.now()
timestamp = now.strftime("%b %d, %Y, %-I:%M %p")

# === Get weather data from Open-Meteo ===
weather = "N/A"
try:
    res = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
        "timezone": "America/New_York"
    })
    data = res.json()
    weather = f"{data['current']['temperature_2m']}°F"
except Exception as e:
    print("Weather error:", e)

# === Get river data from USGS ===
river_level = "N/A"
try:
    usgs_url = f"https://waterservices.usgs.gov/nwis/iv/?sites={usgs_site}&parameterCd=00065&format=json"
    r = requests.get(usgs_url)
    j = r.json()
    value = j['value']['timeSeries'][0]['values'][0]['value'][0]['value']
    river_level = f"{value} ft"
except Exception as e:
    print("River level error:", e)

# === Replace placeholders in HTML ===
html = html.replace("{{weather_temp}}", weather)
html = html.replace("{{river_level}}", river_level)
html = html.replace("{{last_updated}}", f"Last updated: {timestamp}")

# === Save output ===
with open("snapshot.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ snapshot.html updated with live weather and river data")
