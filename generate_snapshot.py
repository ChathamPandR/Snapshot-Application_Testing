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
    value = j['value']['timeSeries'][0]['values'][0]['value'][0]['value']
    river_level = f"{value} ft"
except Exception as e:
    print("River level error:", e)

# === Swim Guide Status for US 64 ===
swim_status = "N/A"
try:
    resp = requests.get(swimguide_url)
    data = resp.json()
    us64 = next((site for site in data if "US 64" in site["name"]), None)
    if us64:
        status = us64["latest_classification"]
        if "safe" in status.lower():
            swim_status = "Safe to swim"
        elif "caution" in status.lower():
            swim_status = "Swim with caution"
        elif "unsafe" in status.lower():
            swim_status = "Unsafe to swim"
        else:
            swim_status = status.capitalize()
except Exception as e:
    print("Swim Guide error:", e)

# === NWS Alerts ===
alerts = "None"
try:
    nws_url = f"https://api.weather.gov/alerts/active/zone/{nws_zone}"
    headers = {"User-Agent": "haw-river-sign/1.0 contact@example.com"}
    r = requests.get(nws_url, headers=headers)
    j = r.json()
    if j.get("features"):
        alerts = "; ".join([f["properties"]["event"] for f in j["features"]])
except Exception as e:
    print("NWS Alerts error:", e)

# === Air Quality ===
aqi = "N/A"
try:
    res = requests.get("https://air-quality-api.open-meteo.com/v1/air-quality", params={
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "America/New_York"
    })
    data = res.json()
    aqi_value = data["current"]["us_aqi"]
    aqi = f"AQI: {aqi_value}"
except Exception as e:
    print("Air quality error:", e)

# === Replace placeholders in HTML ===
html = html.replace("{{weather_temp}}", weather)
html = html.replace("{{river_level}}", river_level)
html = html.replace("{{swim_status_us64}}", swim_status)
html = html.replace("{{nws_alerts}}", alerts)
html = html.replace("{{air_quality}}", aqi)
html = html.replace("{{last_updated}}", f"Last updated: {timestamp}")

# === Save output ===
with open("snapshot.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ snapshot.html updated with live environmental data (Eastern Time)")
