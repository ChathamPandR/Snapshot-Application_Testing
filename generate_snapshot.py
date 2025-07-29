import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# === Config ===
latitude = 35.7202
longitude = -79.1772
usgs_site = "02096960"
nws_zone = "NCZ041"  # NWS zone for Chatham County
swimguide_url = "https://www.theswimguide.org/api/locations?region=haw-river-assembly"

# === Load template HTML ===
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# === Get current time in Eastern Time ===
eastern = pytz.timezone("US/Eastern")
now = datetime.now(eastern)
timestamp = now.strftime("%b %d, %Y, %I:%M %p")

# === Weather ===
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

# === River Level (USGS) ===
river_level = "N/A"
try:
    usgs_url = f"https://waterservices.usgs.gov/nwis/iv/?sites={usgs_site}&parameterCd=00065&format=json"
    r = requests.get(usgs_url)
    j = r.json()
    value = j['value']['timeSerie]()

