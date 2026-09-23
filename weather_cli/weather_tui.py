from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Label, DataTable
from textual.containers import Container, Horizontal, Vertical
from textual.binding import Binding
import requests
import csv
from datetime import datetime

class WeatherTUI(App):
    CSS = """
    Screen {
        align: center middle;
        background: #1e293b;
    }
    #main-container {
        width: 80%;
        height: 80%;
        border: round #60a5fa;
        padding: 1;
    }
    #sidebar {
        width: 30;
        border-right: vline #60a5fa;
        padding: 1;
    }
    #content {
        padding: 1;
    }
    .weather-box {
        background: #334155;
        border: round #93c5fd;
        padding: 1;
        margin-bottom: 1;
        text-align: center;
    }
    .stat-label {
        color: #94a3b8;
        text-style: italic;
    }
    .stat-value {
        color: #f8fafc;
        text-style: bold;
        font-size: 120%;
    }
    #search-bar {
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("h", "show_history", "History"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-container"):
            with Horizontal():
                with Vertical(id="sidebar"):
                    yield Label("[bold cyan]Recent Searches[/bold cyan]")
                    yield DataTable(id="history-table")
                with Vertical(id="content"):
                    yield Input(placeholder="Enter city name and press Enter...", id="search-bar")
                    yield Static("Search for a city to see the weather!", id="weather-display")
                    yield DataTable(id="forecast-table")
        yield Footer()

    def on_mount(self) -> None:
        self.update_history_table()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        city = event.value
        self.query_one("#weather-display").update(f"Searching for {city}...")
        
        # Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        try:
            geo_res = requests.get(geo_url).json()
            if "results" not in geo_res:
                self.query_one("#weather-display").update("[red]City not found![/red]")
                return
            
            res = geo_res["results"][0]
            lat, lon, full_name = res["latitude"], res["longitude"], res["name"]

            # Current Weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            w_res = requests.get(weather_url).json()["current_weather"]
            
            # Format display
            self.query_one("#weather-display").update(
                f"""
                <div class="weather-box">
                    [bold white]{full_name}[/bold white]
                    <br/>
                    <span class="stat-label">Temperature:</span> [bold yellow]{w_res['temperature']}°C[/bold yellow]
                    <br/>
                    <span class="stat-label">Wind Speed:</span> [bold white]{w_res['windspeed']} km/h[/bold white]
                </div>
                """
            )

            # Save to CSV
            with open("weather_history.csv", mode='a', newline='') as file:
                csv.writer(file).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), full_name, w_res['temperature']])

            self.update_history_table()
            self.update_forecast_table(lat, lon, full_name)

        except Exception as e:
            self.query_one("#weather-display").update(f"[red]Error: {str(e)}[/red]")

    def update_history_table(self):
        table = self.query_one("#history-table", DataTable)
        table.clear()
        table.add_columns("City", "Temp")
        try:
            with open("weather_history.csv", mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row: table.add_row(row[1], f"{row[2]}°C")
        except FileNotFoundError:
            pass

    def update_forecast_table(self, lat, lon, city):
        table = self.query_one("#forecast-table", DataTable)
        table.clear()
        table.add_columns("Date", "Max Temp", "Min Temp")
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        data = requests.get(url).json()["daily"]
        
        for i in range(len(data["time"])):
            table.add_row(data["time"][i], f"{data['temperature_2m_max'][i]}°C", f"{data['temperature_2m_min'][i]}°C")

if __name__ == "__main__":
    app = WeatherTUI()
    app.run()
