from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Label, DataTable, Button
from textual.containers import Container, Horizontal, Vertical
from textual.binding import Binding
import requests
import csv
from datetime import datetime
from favorites_manager import load_favorites, save_favorite, remove_favorite, get_all_favorites

class WeatherTUI(App):
    CSS = """
    Screen {
        align: center middle;
        background: #1e293b;
    }
    #main-container {
        width: 95%;
        height: 95%;
        border: round #60a5fa;
        padding: 1;
    }
    #sidebar {
        width: 35;
        border-right: solid #60a5fa;
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
    }
    #search-bar {
        margin-bottom: 1;
    }
    .fav-btn {
        margin-top: 1;
        width: 100%;
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
                    yield Label("[bold cyan]⭐ Favorites[/bold cyan]")
                    yield DataTable(id="fav-table")
                    yield Label("[bold cyan]🕒 Recent[/bold cyan]")
                    yield DataTable(id="history-table")
                with Vertical(id="content"):
                    yield Input(placeholder="Enter city name and press Enter...", id="search-bar")
                    yield Static("Search for a city to see the advanced weather data!", id="weather-display")
                    yield Button("⭐ Add to Favorites", id="add-fav", classes="fav-btn")
                    yield DataTable(id="forecast-table")
        yield Footer()

    def on_mount(self) -> None:
        self.update_history_table()
        self.update_favorites_table()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        city = event.value
        self.query_one("#weather-display").update(f"Fetching advanced data for {city}...")
        
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        try:
            geo_res = requests.get(geo_url).json()
            if "results" not in geo_res:
                self.query_one("#weather-display").update("[red]City not found![/red]")
                return
            
            res = geo_res["results"][0]
            self.current_city_data = {
                "lat": res["latitude"], 
                "lon": res["longitude"], 
                "name": res["name"]
            }

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={res['latitude']}&longitude={res['longitude']}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,wind_speed_10m&daily=uv_index_max&timezone=auto"
            w_res = requests.get(weather_url).json()
            
            current = w_res["current"]
            uv_index = w_res["daily"]["uv_index_max"][0]
            
            self.query_one("#weather-display").update(
                f"""
                <div class="weather-box">
                    [bold white]{res['name']}[/bold white]
                    <br/>
                    <span class="stat-label">Temperature:</span> [bold yellow]{current['temperature_2m']}°C[/bold yellow] | [dim]Feels like: {current['apparent_temperature']}°C[/dim]
                    <br/>
                    <span class="stat-label">Humidity:</span> [bold white]{current['relative_humidity_2m']}%[/bold white] | [bold white]Wind: {current['wind_speed_10m']} km/h[/bold white]
                    <br/>
                    <span class="stat-label">UV Index:</span> [bold magenta]{uv_index}[/bold magenta] | [dim]Precip: {current['precipitation']}mm[/dim]
                </div>
                """
            )

            with open("weather_history.csv", mode='a', newline='') as file:
                csv.writer(file).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), res['name'], current['temperature_2m']])

            self.update_history_table()
            self.update_forecast_table(res['latitude'], res['longitude'], res['name'])

        except Exception as e:
            self.query_one("#weather-display").update(f"[red]Error: {str(e)}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-fav":
            if hasattr(self, 'current_city_data'):
                data = self.current_city_data
                save_favorite(data['name'], data['lat'], data['lon'])
                self.update_favorites_table()
                self.notify(f"Added {data['name']} to favorites!")

    def update_favorites_table(self):
        table = self.query_one("#fav-table", DataTable)
        table.clear()
        table.add_columns("City")
        favs = get_all_favorites()
        for city in favs:
            table.add_row(city)

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
