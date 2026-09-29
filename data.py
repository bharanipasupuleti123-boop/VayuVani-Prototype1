"""
VayuVani - Demo Weather Data
Contains demonstration weather data for 4 locations:
- Hyderabad
- Visakhapatnam
- Vijayawada
- Chennai

Note: Demo weather data only.
"""

from datetime import datetime, timedelta

def get_demo_dates():
    today = datetime.now()
    d1 = today.strftime("%d %b (Today)")
    d2 = (today + timedelta(days=1)).strftime("%d %b (Tomorrow)")
    d3 = (today + timedelta(days=2)).strftime("%d %b (Day 3)")
    return [d1, d2, d3]

dates = get_demo_dates()

DEMO_WEATHER_DATA = {
    "Hyderabad": {
        "city": "Hyderabad",
        "state": "Telangana",
        "type": "Inland",
        "current": {
            "temperature": 29,
            "humidity": 78,
            "wind_speed": 14,
            "rain_probability": 75,
            "condition": "Scattered Thunderstorms",
            "condition_code": "thunderstorm",
            "last_updated": "Local Demo Snapshot"
        },
        "forecast": [
            {
                "day_label": dates[0],
                "condition": "Scattered Thunderstorms",
                "temp_min": 24,
                "temp_max": 31,
                "rain_probability": 75,
                "wind_speed": 14,
                "condition_code": "thunderstorm"
            },
            {
                "day_label": dates[1],
                "condition": "Moderate to Heavy Rain",
                "temp_min": 23,
                "temp_max": 28,
                "rain_probability": 85,
                "wind_speed": 18,
                "condition_code": "heavy_rain"
            },
            {
                "day_label": dates[2],
                "condition": "Light Passing Showers",
                "temp_min": 22,
                "temp_max": 29,
                "rain_probability": 40,
                "wind_speed": 12,
                "condition_code": "light_rain"
            }
        ],
        "advisory_notes": {
            "flood_susceptibility": "Moderate in low-lying urban catchment areas.",
            "crop_context": "Paddy and vegetable crops in vegetative growth phase.",
            "marine_context": "Not applicable (Inland)."
        }
    },
    "Visakhapatnam": {
        "city": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "type": "Coastal",
        "current": {
            "temperature": 32,
            "humidity": 82,
            "wind_speed": 34,
            "rain_probability": 60,
            "condition": "Squally Winds & Overcast",
            "condition_code": "windy_rain",
            "last_updated": "Local Demo Snapshot"
        },
        "forecast": [
            {
                "day_label": dates[0],
                "condition": "Gusty Winds & Rain Showers",
                "temp_min": 26,
                "temp_max": 32,
                "rain_probability": 60,
                "wind_speed": 34,
                "condition_code": "windy_rain"
            },
            {
                "day_label": dates[1],
                "condition": "High Wind & Sea Squall",
                "temp_min": 25,
                "temp_max": 31,
                "rain_probability": 70,
                "wind_speed": 38,
                "condition_code": "squall"
            },
            {
                "day_label": dates[2],
                "condition": "Breezy with Partly Cloudy Skies",
                "temp_min": 26,
                "temp_max": 33,
                "rain_probability": 30,
                "wind_speed": 22,
                "condition_code": "partly_cloudy"
            }
        ],
        "advisory_notes": {
            "flood_susceptibility": "Localized waterlogging near beach corridors.",
            "crop_context": "Horticulture and cashews - risk of branch snapping in high wind.",
            "marine_context": "Rough to very rough sea conditions along North AP coast."
        }
    },
    "Vijayawada": {
        "city": "Vijayawada",
        "state": "Andhra Pradesh",
        "type": "Inland",
        "current": {
            "temperature": 34,
            "humidity": 62,
            "wind_speed": 15,
            "rain_probability": 25,
            "condition": "Warm with Periodic Clouds",
            "condition_code": "partly_cloudy",
            "last_updated": "Local Demo Snapshot"
        },
        "forecast": [
            {
                "day_label": dates[0],
                "condition": "Partly Cloudy & Warm",
                "temp_min": 26,
                "temp_max": 35,
                "rain_probability": 25,
                "wind_speed": 15,
                "condition_code": "partly_cloudy"
            },
            {
                "day_label": dates[1],
                "condition": "Isolated Light Drizzle",
                "temp_min": 25,
                "temp_max": 34,
                "rain_probability": 35,
                "wind_speed": 14,
                "condition_code": "light_rain"
            },
            {
                "day_label": dates[2],
                "condition": "Clear and Sunny",
                "temp_min": 24,
                "temp_max": 36,
                "rain_probability": 15,
                "wind_speed": 12,
                "condition_code": "clear"
            }
        ],
        "advisory_notes": {
            "flood_susceptibility": "Low - Krishna river levels within normal seasonal flow.",
            "crop_context": "Suitable for regular field irrigation, harvesting and spraying.",
            "marine_context": "Not applicable (Inland)."
        }
    },
    "Chennai": {
        "city": "Chennai",
        "state": "Tamil Nadu",
        "type": "Coastal",
        "current": {
            "temperature": 30,
            "humidity": 80,
            "wind_speed": 22,
            "rain_probability": 50,
            "condition": "Humid & Passing Clouds",
            "condition_code": "cloudy",
            "last_updated": "Local Demo Snapshot"
        },
        "forecast": [
            {
                "day_label": dates[0],
                "condition": "Cloudy with Light Evening Rains",
                "temp_min": 25,
                "temp_max": 31,
                "rain_probability": 50,
                "wind_speed": 22,
                "condition_code": "cloudy_rain"
            },
            {
                "day_label": dates[1],
                "condition": "Moderate Coastal Showers",
                "temp_min": 25,
                "temp_max": 30,
                "rain_probability": 65,
                "wind_speed": 25,
                "condition_code": "rain"
            },
            {
                "day_label": dates[2],
                "condition": "Partly Sunny & Humid",
                "temp_min": 26,
                "temp_max": 32,
                "rain_probability": 30,
                "wind_speed": 18,
                "condition_code": "partly_cloudy"
            }
        ],
        "advisory_notes": {
            "flood_susceptibility": "Moderate watch on storm drains in coastal lowlands.",
            "crop_context": "Normal coastal agricultural operations.",
            "marine_context": "Moderate wave action. Artisanal boats advise basic safety precautions."
        }
    }
}
