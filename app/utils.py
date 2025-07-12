import requests

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        print("utils data : ", data)
        loc = data.get("loc", "")
        if loc:
            lat, lon = loc.split(",")
            return float(lat), float(lon), data.get("city", "Unknown")
    except Exception as e:
        print("Location error:", e)
    return 0.0, 0.0, "Unknown"

def get_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        res = requests.get(url)
        data = res.json()
        return data.get("current_weather", {})
    except Exception as e:
        print("Weather error:", e)
    return {}
