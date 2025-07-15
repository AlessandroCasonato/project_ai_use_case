from datetime import datetime

class ResponseBuilder:
    def build(self, intent, city, date, current, forecast):
        if intent == "help":
            return (
                "I can give you weather info! Try:\n"
                "- What's the weather like in Paris?\n"
                "- Will it rain in Rome tomorrow?\n"
                "- What's the humidity in Milan next Monday?\n"
            )

        use_forecast = date is not None
        if use_forecast and not forecast:
            return f"Sorry, I couldn't get forecast data for {city}."
        if not use_forecast and not current:
            return f"Sorry, I couldn't find weather info for '{city}'."

        if use_forecast:
            slot = next((e for e in forecast["list"]
                         if datetime.strptime(e["dt_txt"], "%Y-%m-%d %H:%M:%S").date() == date.date()), None)
            if not slot:
                return f"Sorry, no forecast data for {city} on that date."
            main = slot["main"]
            weather_desc = slot["weather"][0]["description"]
            wind = slot["wind"]["speed"]

            return self._format_response(intent, city, date, main, weather_desc, wind)

        weather_desc = current["weather"][0]["description"]
        temp = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        wind = current["wind"]["speed"]

        return self._format_response(intent, city, None, current["main"], weather_desc, wind, humidity)

    def _format_response(self, intent, city, date, main, weather_desc, wind, humidity=None):
        date_str = f" on {date.strftime('%A, %B %d')}" if date else ""
        if intent == "weather":
            return f"Forecast for {city}{date_str}: {weather_desc}, {main['temp']}°C."
        if intent == "temperature":
            return f"The temperature in {city}{date_str} is {main['temp']}°C."
        if intent == "rain":
            return ("Yes, rain is expected." if "rain" in weather_desc.lower()
                    else "No rain is expected.") + f" ({weather_desc})"
        if intent == "wind":
            return f"The wind speed in {city}{date_str} is {wind} m/s."
        if intent == "humidity":
            return f"The humidity in {city}{date_str} is {main['humidity']}%."
        return "I'm not sure how to help with that."
