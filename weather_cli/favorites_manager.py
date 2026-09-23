import json
import os

FAVORITES_FILE = "weather_favorites.json"

def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return {}
    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)

def save_favorite(city_name, lat, lon):
    favorites = load_favorites()
    favorites[city_name] = {"lat": lat, "lon": lon}
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)

def remove_favorite(city_name):
    favorites = load_favorites()
    if city_name in favorites:
        del favorites[city_name]
        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=4)

def get_all_favorites():
    return load_favorites()
