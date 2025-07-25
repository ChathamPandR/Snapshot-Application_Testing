# generate_snapshot.py
from bs4 import BeautifulSoup
from datetime import datetime

# Load existing HTML template
with open("template.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Update timestamp
timestamp = datetime.now().strftime("%b %d, %Y, %-I:%M %p")
for elem in soup.find_all("div", class_="card-timestamp"):
    elem.string = f"Last updated: {timestamp}"

# Save updated file
with open("snapshot.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
