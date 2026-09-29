"""
VayuVani - Weather Advice Engine
Generates tailored weather advice and answers based on demo weather data.
"""

def get_user_type_advice(city_data: dict, user_type: str) -> dict:
    """
    Returns tailored baseline weather advice based on the selected location and user type.
    """
    current = city_data["current"]
    tomorrow = city_data["forecast"][1]
    city_name = city_data["city"]
    city_type = city_data.get("type", "Inland")
    
    rain_today = current["rain_probability"]
    rain_tomorrow = tomorrow["rain_probability"]
    wind_current = current["wind_speed"]
    wind_tomorrow = tomorrow["wind_speed"]
    condition = current["condition"]
    temp = current["temperature"]

    if user_type == "Farmer":
        if rain_tomorrow >= 60:
            return {
                "title": "Irrigation & Spraying Advice",
                "message": f"Rain chance is high tomorrow ({rain_tomorrow}%) in {city_name}. Consider postponing irrigation and pesticide spraying to prevent runoff.",
                "type": "warning"
            }
        elif wind_current >= 25 or wind_tomorrow >= 25:
            return {
                "title": "Wind & Spraying Advice",
                "message": f"Wind speeds are reaching {max(wind_current, wind_tomorrow)} km/h. Avoid foliar or chemical spraying today to reduce drift loss.",
                "type": "warning"
            }
        elif rain_today <= 30 and rain_tomorrow <= 30:
            return {
                "title": "Favorable Field Conditions",
                "message": f"Conditions are clear to mild with low rain chance ({rain_today}%). Suitable for routine irrigation, weeding, and field operations.",
                "type": "success"
            }
        else:
            return {
                "title": "Moderate Rain Watch",
                "message": f"Scattered showers possible (rain chance {rain_tomorrow}% tomorrow). Check soil moisture before irrigating.",
                "type": "info"
            }

    elif user_type == "Fisherman":
        if city_type == "Inland":
            return {
                "title": "Inland Waterways Notice",
                "message": f"{city_name} is an inland area. For local lakes or rivers, wind speed is {wind_current} km/h with a {rain_today}% rain chance.",
                "type": "info"
            }
        max_wind = max(wind_current, wind_tomorrow)
        if max_wind >= 30:
            return {
                "title": "Rough Sea Caution",
                "message": f"Coastal wind speeds are strong ({max_wind} km/h). Choppy water conditions expected along the {city_name} coast. Small boats should exercise caution.",
                "type": "warning"
            }
        elif rain_tomorrow >= 70:
            return {
                "title": "Low Visibility Warning",
                "message": f"Heavy rain showers expected tomorrow ({rain_tomorrow}% chance). Expect reduced visibility at sea.",
                "type": "warning"
            }
        else:
            return {
                "title": "Calm Sea Conditions",
                "message": f"Winds are at {wind_current} km/h and within normal operational limits. Safe for regular coastal fishing.",
                "type": "success"
            }

    elif user_type == "Disaster Response":
        if rain_today >= 70 or rain_tomorrow >= 70 or "Thunderstorm" in condition:
            return {
                "title": "Waterlogging & Rain Advisory",
                "message": f"Elevated rain probability ({max(rain_today, rain_tomorrow)}%) and {condition.lower()} observed. Low-lying areas may experience temporary waterlogging.",
                "type": "warning"
            }
        elif wind_current >= 30:
            return {
                "title": "High Wind Advisory",
                "message": f"Wind speeds are currently {wind_current} km/h. Monitor outdoor signage, loose structures, and power lines.",
                "type": "warning"
            }
        else:
            return {
                "title": "Normal Weather Conditions",
                "message": f"Weather metrics are currently normal across {city_name}. No weather warnings active.",
                "type": "success"
            }

    else:  # General User
        if rain_today >= 60 or rain_tomorrow >= 60:
            return {
                "title": "Rain Notice",
                "message": f"High chance of rain ({max(rain_today, rain_tomorrow)}%). Carrying an umbrella or raincoat is recommended.",
                "type": "info"
            }
        elif temp >= 35:
            return {
                "title": "Warm Weather Notice",
                "message": f"Temperature is around {temp}°C. Stay hydrated and limit direct afternoon sun exposure.",
                "type": "info"
            }
        else:
            return {
                "title": "Pleasant Weather",
                "message": f"{condition} with a comfortable temperature of {temp}°C. Good for outdoor activities and travel.",
                "type": "success"
            }


def answer_question(city_data: dict, user_type: str, question: str) -> dict:
    """
    Answers user questions using the location's weather data and user context.
    """
    q = question.lower().strip()
    current = city_data["current"]
    forecast = city_data["forecast"]
    tomorrow = forecast[1]
    city_name = city_data["city"]
    city_type = city_data.get("type", "Inland")

    is_tomorrow = any(w in q for w in ["tomorrow", "next day"])
    
    if is_tomorrow:
        target = tomorrow
        time_text = "tomorrow"
    else:
        target = current
        time_text = "today"

    rain_val = target["rain_probability"]
    wind_val = target["wind_speed"]
    temp_val = target.get("temperature", target.get("temp_max"))
    condition_val = target["condition"]

    # Crop & Farming queries
    if any(w in q for w in ["water", "crop", "irrigate", "irrigation", "farm", "harvest", "field", "plant"]):
        if rain_val >= 60:
            ans = f"Rain chance is high {time_text} ({rain_val}%) with {condition_val.lower()}. It is recommended to hold off on watering crops to prevent waterlogging."
            status = "warning"
        elif rain_val <= 30:
            ans = f"Rain chance is low {time_text} ({rain_val}%) and conditions are {condition_val.lower()}. You can safely irrigate your crops."
            status = "success"
        else:
            ans = f"There is a moderate chance of rain {time_text} ({rain_val}%). Check your local soil moisture before full irrigation."
            status = "info"

    # Spraying & Pesticide queries
    elif any(w in q for w in ["spray", "spraying", "pesticide", "fertilizer", "chemical"]):
        if wind_val >= 25:
            ans = f"Wind speed is {wind_val} km/h {time_text}, which is higher than the recommended limit. Delay spraying to prevent spray drift."
            status = "warning"
        elif rain_val >= 50:
            ans = f"Rain chance is {rain_val}% {time_text}. Delay chemical spraying so it does not wash away."
            status = "warning"
        else:
            ans = f"Wind speed ({wind_val} km/h) and rain chance ({rain_val}%) are moderate {time_text}. Suitable conditions for spraying."
            status = "success"

    # Fishing & Marine queries
    elif any(w in q for w in ["fish", "fishing", "boat", "sea", "sail", "safe to go", "ocean", "marine", "coast", "shore"]):
        if city_type == "Inland":
            ans = f"{city_name} is an inland area. For local rivers or lakes, wind is {wind_val} km/h with a {rain_val}% rain chance {time_text}."
            status = "info"
        elif wind_val >= 30:
            ans = f"Wind speeds are elevated ({wind_val} km/h) and conditions are {condition_val.lower()}. It is advisable to avoid going out to sea {time_text}."
            status = "warning"
        elif rain_val >= 70:
            ans = f"Heavy rain probability ({rain_val}%) and low visibility are expected {time_text}. Exercise extra caution near open water."
            status = "warning"
        else:
            ans = f"Marine conditions appear favorable {time_text} with winds at {wind_val} km/h. Suitable for coastal fishing."
            status = "success"

    # Flood & Disaster queries
    elif any(w in q for w in ["flood", "danger", "hazard", "risk", "warning", "storm", "cyclone", "disaster", "emergency", "alert"]):
        if rain_val >= 70 or "Thunderstorm" in condition_val:
            ans = f"High rain chance ({rain_val}%) and {condition_val.lower()} in {city_name} {time_text}. Watch for localized waterlogging in low-lying roads."
            status = "warning"
        elif wind_val >= 30:
            ans = f"Strong winds ({wind_val} km/h) expected {time_text}. Check for fallen tree branches or unsecured outdoor items."
            status = "warning"
        else:
            ans = f"No severe weather or flood alerts detected for {city_name} {time_text}. Weather conditions are within normal limits."
            status = "success"

    # Rain & Umbrella queries
    elif any(w in q for w in ["rain", "raining", "rainy", "umbrella", "shower", "precipitation", "drizzle"]):
        if rain_val >= 60:
            ans = f"Yes, rain is likely {time_text} in {city_name} with a {rain_val}% chance ({condition_val}). An umbrella or raincoat is advised."
            status = "info"
        elif rain_val >= 30:
            ans = f"There is a moderate chance of light or passing rain {time_text} ({rain_val}%). Keep an umbrella handy just in case."
            status = "info"
        else:
            ans = f"Rain is unlikely {time_text} in {city_name} (only {rain_val}% chance). Expected condition: {condition_val}."
            status = "success"

    # Temperature & Heat queries
    elif any(w in q for w in ["temp", "temperature", "hot", "warm", "cold", "heat"]):
        ans = f"Expected temperature {time_text} in {city_name} is around {temp_val}°C with {condition_val.lower()}."
        status = "info"

    # Wind queries
    elif any(w in q for w in ["wind", "breeze", "gust"]):
        ans = f"Wind speed {time_text} in {city_name} is around {wind_val} km/h."
        status = "info"

    # General weather question
    else:
        ans = f"Weather in {city_name} {time_text} is {condition_val.lower()} with a temperature of {temp_val}°C, wind of {wind_val} km/h, and a rain chance of {rain_val}%."
        status = "info"

    return {
        "question": question,
        "answer": ans,
        "status": status,
        "location": city_name,
        "user_type": user_type
    }
