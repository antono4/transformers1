import requests
import csv
from datetime import datetime
import sys

def get_coords(city):
    """Convert city name to latitude and longitude using Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    response = requests.get(url).json()
    if "results" in response:
        return response["results"][0]["latitude"], response["results"][0]["longitude"], response["results"][0]["name"]
    return None, None, None

def get_weather(lat, lon):
    """Fetch current weather for given coordinates."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url).json()
    return response["current_weather"]

def save_history(city, temp, windspeed):
    """Save search result to a CSV file."""
    file_path = "weather_history.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now, city, temp, windspeed])

def main():
    if len(sys.argv) < 2:
        city = input("Enter city name: ")
    else:
        city = " ".join(sys.argv[1:])

    print(f"Searching for weather in {city}...")
    lat, lon, full_name = get_coords(city)

    if lat is None:
        print("City not found. Please try again.")
        return

    weather = get_weather(lat, lon)
    temp = weather["temperature"]
    wind = weather["windspeed"]

    print("\n" + "="*30)
    print(f" CURRENT WEATHER: {full_name}")
    print("="*30)
    print(f" Temperature: {temp}°C")
    print(f" Wind Speed:   {wind} km/h")
    print("="*30)

    save_history(full_name, temp, wind)
    print("\nResult saved to weather_history.csv")

if __name__ == "__main__":
    main()
