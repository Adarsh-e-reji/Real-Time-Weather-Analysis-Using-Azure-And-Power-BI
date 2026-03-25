import os
import requests
import pandas as pd
from datetime import datetime

# Setup folder structure
output_dir = "raw"
os.makedirs(output_dir, exist_ok=True)

# API Configuration
cities = {
    "Dublin": (53.3498, -6.2603),
    "London": (51.5072, -0.1276),
    "New York": (40.7128, -74.0060),
    "Dubai": (25.2048, 55.2708)
}

rows = []

# Fetch Data
for city, (lat, lon) in cities.items():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        data = requests.get(url).json()
        rows.append({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "city": city,
            "temperature": data["current_weather"]["temperature"],
            "windspeed": data["current_weather"]["windspeed"]
        })
    except Exception as e:
        print(f"Failed to fetch {city}: {e}")

# Create DataFrame and Save
df = pd.DataFrame(rows)
filename = f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
file_path = os.path.join(output_dir, filename)

df.to_csv(file_path, index=False)
print(f"Successfully saved: {file_path}")