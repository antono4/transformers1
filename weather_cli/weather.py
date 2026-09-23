import requests
import csv
import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

console = Console()

def get_coords(city):
    """Convert city name to latitude and longitude using Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        response = requests.get(url).json()
        if "results" in response:
            return response["results"][0]["latitude"], response["results"][0]["longitude"], response["results"][0]["name"]
    except Exception as e:
        console.print(f"[red]Error connecting to geocoding service: {e}[/red]")
    return None, None, None

def get_current_weather(lat, lon, unit="celsius"):
    """Fetch current weather for given coordinates."""
    u_param = "celsius" if unit == "C" else "fahrenheit"
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit={u_param}"
    response = requests.get(url).json()
    return response["current_weather"]

def get_forecast(lat, lon, unit="celsius"):
    """Fetch 7-day forecast for given coordinates."""
    u_param = "celsius" if unit == "C" else "fahrenheit"
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&temperature_unit={u_param}"
    response = requests.get(url).json()
    return response["daily"]

def save_history(city, temp, unit):
    """Save search result to a CSV file."""
    file_path = "weather_history.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now, city, temp, unit])

def show_history():
    """Read and display search history in a rich table."""
    try:
        with open("weather_history.csv", mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            
        if not data:
            console.print("[yellow]No history found yet![/yellow]")
            return

        table = Table(title="Weather Search History", show_header=True, header_style="bold magenta")
        table.add_column("Timestamp", style="dim")
        table.add_column("City")
        table.add_column("Temp")
        table.add_column("Unit")

        for row in data:
            table.add_row(*row)
        
        console.print(table)
    except FileNotFoundError:
        console.print("[red]No history file found. Search for a city first![/red]")

def main():
    parser = argparse.ArgumentParser(description="Professional Weather CLI Tool")
    parser.add_argument("city", nargs="?", help="Name of the city to check weather for")
    parser.add_argument("-f", "--forecast", action="store_true", help="Show 7-day forecast")
    parser.add_argument("-u", "--unit", choices=["C", "F"], default="C", help="Temperature unit (C for Celsius, F for Fahrenheit)")
    parser.add_argument("-s", "--history", action="store_true", help="Show search history")

    args = parser.parse_args()

    if args.history:
        show_history()
        return

    if not args.city:
        args.city = input("Enter city name: ")

    lat, lon, full_name = get_coords(args.city)

    if lat is None:
        console.print(f"[bold red]Error:[/bold red] City '{args.city}' not found.")
        return

    # Current Weather
    weather = get_current_weather(lat, lon, args.unit)
    temp = weather["temperature"]
    wind = weather["windspeed"]
    unit_symbol = "°C" if args.unit == "C" else "°F"

    console.print(Panel(
        f"[bold blue]{full_name}[/bold blue]\n"
        f"Temperature: [bold yellow]{temp}{unit_symbol}[/bold yellow]\n"
        f"Wind Speed: {wind} km/h",
        title="Current Weather", expand=False
    ))

    save_history(full_name, temp, args.unit)

    # Forecast Logic
    if args.forecast:
        console.print("\n[bold magenta]Fetching 7-day forecast...[/bold magenta]")
        forecast_data = get_forecast(lat, lon, args.unit)
        
        forecast_table = Table(title=f"7-Day Forecast for {full_name}", show_header=True, header_style="bold cyan")
        forecast_table.add_column("Date")
        forecast_table.add_column("Max Temp", justify="right")
        forecast_table.add_column("Min Temp", justify="right")

        for i in range(len(forecast_data["time"])):
            forecast_table.add_row(
                forecast_data["time"][i],
                f"{forecast_data['temperature_2m_max'][i]}{unit_symbol}",
                f"{forecast_data['temperature_2m_min'][i]}{unit_symbol}"
            )
        
        console.print(forecast_table)

if __name__ == "__main__":
    main()
