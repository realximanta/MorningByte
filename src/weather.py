"""
weather.py — Fetches current weather using Open-Meteo API (no API key required).
"""

import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

# WMO Weather Interpretation Codes
WMO_CODES: dict[int, str] = {
    0: "Clear Sky ☀️",
    1: "Mainly Clear 🌤",
    2: "Partly Cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫",
    48: "Icy Fog 🌫",
    51: "Light Drizzle 🌦",
    53: "Moderate Drizzle 🌦",
    55: "Heavy Drizzle 🌧",
    61: "Slight Rain 🌧",
    63: "Moderate Rain 🌧",
    65: "Heavy Rain 🌧",
    71: "Slight Snow 🌨",
    73: "Moderate Snow 🌨",
    75: "Heavy Snow ❄️",
    77: "Snow Grains ❄️",
    80: "Slight Showers 🌦",
    81: "Moderate Showers 🌧",
    82: "Violent Showers ⛈",
    85: "Slight Snow Showers 🌨",
    86: "Heavy Snow Showers 🌨",
    95: "Thunderstorm ⛈",
    96: "Thunderstorm + Hail ⛈",
    99: "Thunderstorm + Heavy Hail ⛈",
}


def get_weather(
    latitude: float,
    longitude: float,
    city_name: str,
) -> Optional[dict]:
    """
    Fetch current weather from Open-Meteo.

    Args:
        latitude: Location latitude.
        longitude: Location longitude.
        city_name: Human-readable city label for display.

    Returns:
        Dict with keys: city, temperature, condition
        or None on failure.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "weathercode"],
        "temperature_unit": "celsius",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        temp = round(current["temperature_2m"])
        code = int(current["weathercode"])
        condition = WMO_CODES.get(code, "Unknown 🌡")

        logger.info("Weather fetched: %d°C, %s", temp, condition)
        return {
            "city": city_name,
            "temperature": temp,
            "condition": condition,
        }

    except requests.RequestException as e:
        logger.error("Failed to fetch weather: %s", e)
        return None
