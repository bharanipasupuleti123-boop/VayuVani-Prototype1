import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="VayuVani",
    page_icon="🌦️",
    layout="wide"
)

# -----------------------------
# Weather descriptions
# -----------------------------

def weather_description(code):
    data = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail"
    }

    return data.get(code, "Unknown")


# -----------------------------
# Find location
# -----------------------------

def find_location(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]

    return {
        "name": result["name"],
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


# -----------------------------
# Get weather
# -----------------------------

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "weather_code"
        ),
        "forecast_days": 3,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        return None

    return response.json()


# -----------------------------
# Query routing
# -----------------------------

def route_question(question):

    question = question.lower()

    advisory_words = [
        "safe",
        "safety",
        "advice",
        "advisory",
        "warning",
        "should i",
        "what should",
        "farmer",
        "farming",
        "crop",
        "rain",
        "flood",
        "storm"
    ]

    for word in advisory_words:

        if word in question:
            return "Advisory"

    return "Weather"


# -----------------------------
# Advisory
# -----------------------------

def get_advisory(weather):

    rain = weather["daily"]["precipitation_probability_max"][0]
    code = weather["current"]["weather_code"]

    if code in [95, 96, 99]:

        return (
            "Thunderstorm conditions are possible. "
            "Avoid unnecessary outdoor activity and "
            "monitor local weather updates."
        )

    if rain >= 70:

        return (
            "High chance of rain. "
            "Plan outdoor activities carefully "
            "and keep rain protection ready."
        )

    if rain >= 40:

        return (
            "Rain is possible. "
            "Keep necessary rain protection ready."
        )

    return (
        "No major weather warning is detected "
        "for the selected location."
    )


# -----------------------------
# Farmer response
# -----------------------------

def farmer_advisory(weather):

    rain = weather["daily"]["precipitation_probability_max"][0]

    if rain >= 60:

        return (
            "వర్షం వచ్చే అవకాశం ఎక్కువగా ఉంది. "
            "వ్యవసాయ పనులను వాతావరణ పరిస్థితులకు "
            "అనుగుణంగా ప్లాన్ చేయండి."
        )

    if rain >= 30:

        return (
            "వర్షం వచ్చే అవకాశం ఉంది. "
            "వ్యవసాయ పనులను జాగ్రత్తగా ప్లాన్ చేయండి."
        )

    return (
        "వర్షం వచ్చే అవకాశం తక్కువగా ఉంది. "
        "వ్యవసాయ పనులను సాధారణంగా ప్లాన్ చేయవచ్చు."
    )


# -----------------------------
# Header
# -----------------------------

st.title("🌦️ VayuVani")
st.write("Conversational Weather & Climate Information")

st.divider()


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Location")

city = st.sidebar.text_input(
    "Enter a city",
    value="Hyderabad"
)

st.sidebar.header("User")

persona = st.sidebar.selectbox(
    "Select user",
    [
        "General",
        "Farmer"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Weather data: Open-Meteo"
)


# -----------------------------
# Get location
# -----------------------------

location = find_location(city)

if location is None:

    st.error(
        "Location not found. Please enter a valid city."
    )

    st.stop()


weather = get_weather(
    location["latitude"],
    location["longitude"]
)

if weather is None:

    st.error(
        "Weather data could not be retrieved."
    )

    st.stop()


# -----------------------------
# Current weather
# -----------------------------

st.subheader(
    f"📍 {location['name']}, {location['country']}"
)

current = weather["current"]

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Temperature",
        f"{current['temperature_2m']} °C"
    )

with col2:

    st.metric(
        "Humidity",
        f"{current['relative_humidity_2m']}%"
    )

with col3:

    st.metric(
        "Wind",
        f"{current['wind_speed_10m']} km/h"
    )

with col4:

    rain = weather["daily"]["precipitation_probability_max"][0]

    st.metric(
        "Rain Chance",
        f"{rain}%"
    )


st.write(
    f"**Current condition:** "
    f"{weather_description(current['weather_code'])}"
)


# -----------------------------
# Forecast
# -----------------------------

st.subheader("3-Day Forecast")

daily = weather["daily"]

forecast_cols = st.columns(3)

for i in range(3):

    date = datetime.fromisoformat(
        daily["time"][i]
    ).strftime("%d %b")

    with forecast_cols[i]:

        st.write(f"### {date}")

        st.write(
            weather_description(
                daily["weather_code"][i]
            )
        )

        st.write(
            f"🌡️ {daily['temperature_2m_min'][i]}°C - "
            f"{daily['temperature_2m_max'][i]}°C"
        )

        st.write(
            f"🌧️ "
            f"{daily['precipitation_probability_max'][i]}% rain chance"
        )


st.divider()


# -----------------------------
# Question
# -----------------------------

st.subheader("💬 Ask VayuVani")

question = st.text_input(
    "Ask a weather question",
    placeholder="Example: Will it rain tomorrow?"
)

if st.button("Get Answer"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        route = route_question(question)

        st.write("### Query Route")

        if route == "Weather":

            st.success(
                "LIVE WEATHER DATA"
            )

        else:

            st.info(
                "WEATHER ADVISORY"
            )


        # ---------------------
        # Weather response
        # ---------------------

        if route == "Weather":

            st.write("### Weather Information")

            st.write(
                f"The current weather in "
                f"**{location['name']}** is "
                f"**{weather_description(current['weather_code'])}** "
                f"with a temperature of "
                f"**{current['temperature_2m']} °C**."
            )

            st.write(
                f"Today's rain probability is "
                f"**{rain}%**."
            )


        # ---------------------
        # Advisory response
        # ---------------------

        else:

            st.write("### 🚨 Advisory")

            st.info(
                get_advisory(weather)
            )


        # ---------------------
        # Farmer mode
        # ---------------------

        if persona == "Farmer":

            st.write("### 🌾 Farmer View")

            st.success(
                farmer_advisory(weather)
            )


# -----------------------------
# Example questions
# -----------------------------

st.divider()

st.subheader("Try these questions")

examples = [
    "What is the weather today?",
    "Will it rain tomorrow?",
    "What should I do if heavy rain is expected?"
]

for example in examples:

    st.write(f"• {example}")