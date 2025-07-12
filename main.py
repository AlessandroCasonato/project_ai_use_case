from transformers import pipeline
import requests
import re
from datetime import datetime
from dateparser.search import search_dates
import string

# OpenWeatherMap key
API_KEY = "5ebfaae5335ce790b0cb60f2d1dfd0e9"  

# Bart model for zero-shot classification
# This model is used to classify user intents based on their input.
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = [
    "What's the weather like?",
    "What's the temperature?",
    "Will it rain?",
    "Is it windy?",
    "What's the humidity?",
    "What can you do?"
]

label_to_intent = {
    "What's the weather like?": "weather",
    "What's the temperature?": "temperature",
    "Will it rain?": "rain",
    "Is it windy?": "wind",
    "What's the humidity?": "humidity",
    "What can you do?": "help"
}

def extract_city_and_date(user_input):
    """Extract city and date from user input. If date is not specified, it will be considered as the current date."""
    date = None
    found_date_text = None

    parsed = search_dates(user_input, settings={'PREFER_DATES_FROM': 'future'})
    if parsed:
        found_date_text, date = parsed[0]
        cleaned_input = user_input.replace(found_date_text, "")
    else:
        cleaned_input = user_input

    city_match = re.search(r"\b(?:in|at)\s+([A-ZÀ-Ùa-zà-ù\s]+)", cleaned_input)
    if city_match:
        city = city_match.group(1).strip()
    else:
        words = cleaned_input.split()
        stopwords = {"what", "is", "the", "weather", "like", "will", "it", "be", "going", "to", "rain", "tomorrow", "humidity", "temperature", "forecast", "in", "at", "on", "and", "of", "for"}
        candidates = [w for w in words if w.lower() not in stopwords]
        city = candidates[-1] if candidates else None

    if city:
        city = city.strip(string.punctuation)

    return city, date


def classify_intent(text: str):
    result = classifier(text, labels)
    best = result['labels'][0]; score = result['scores'][0]
    return label_to_intent[best] if score > 0.3 else None

def get_current(city):
    """API call that returns weather data based on current date and time."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    return data if data.get("cod") == 200 else None

def get_forecast(city):
    """API call that returns weather data based on current date and time."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    print(url)
    data = requests.get(url).json()
    return data if data.get("cod") == "200" else None

def build_response(intent, city, date, current, forecast):
    if intent == "help":
        return (
            "I can give you weather info! Try:\n"
            "- What's the weather like in Paris?\n"
            "- Will it rain in Rome tomorrow?\n"
            "- What's the humidity in Milan next Monday?\n"
        )
    # Choose data source
    use_forecast = date is not None
    if use_forecast and not forecast:
        return f"Sorry, I couldn't get forecast data for {city}."
    if not use_forecast and not current:
        return f"Sorry, I couldn't find weather info for '{city}'."

    # ---------- From forecast ---------- #
    if use_forecast:
        # pick the first slot of the requested day
        slot = next((e for e in forecast["list"]
                     if datetime.strptime(e["dt_txt"], "%Y-%m-%d %H:%M:%S").date() == date.date()), None)
        if not slot:
            return f"Sorry, no forecast data for {city} on that date."
        main = slot["main"]; weather_desc = slot["weather"][0]["description"]; wind = slot["wind"]["speed"]
        if intent == "weather":
            return f"Forecast for {city} on {date.strftime('%A, %B %d')}: {weather_desc}, {main['temp']}°C."
        if intent == "temperature":
            return f"The forecasted temperature in {city} on {date.strftime('%A, %B %d')} is {main['temp']}°C."
        if intent == "rain":
            return ("Yes, rain is expected." if "rain" in weather_desc.lower()
                    else "No rain is expected.") + f" ({weather_desc})"
        if intent == "wind":
            return f"The forecasted wind speed in {city} on {date.strftime('%A, %B %d')} is {wind} m/s."
        if intent == "humidity":
            return f"The forecasted humidity in {city} on {date.strftime('%A, %B %d')} is {main['humidity']}%."

    # ---------- From current ---------- #
    weather_desc = current["weather"][0]["description"]; temp = current["main"]["temp"]
    humidity = current["main"]["humidity"]; wind = current["wind"]["speed"]

    if intent == "weather":
        return f"In {city} it's currently {weather_desc} with {temp}°C."
    if intent == "temperature":
        return f"The temperature in {city} is {temp}°C."
    if intent == "rain":
        return ("Yes, it's raining." if "rain" in weather_desc.lower()
                else "No rain right now.") + f" ({weather_desc})"
    if intent == "wind":
        return f"The wind speed in {city} is {wind} m/s."
    if intent == "humidity":
        return f"The humidity in {city} is {humidity}%."
    return "I'm not sure how to help with that."

# ---------- Chat loop ---------- #
def chatbot(user_input):
    intent = classify_intent(user_input)
    if not intent:
        return "I'm not sure how to help with that."
    city, date = extract_city_and_date(user_input)
    if not city:
        return "Please include a city in your question (e.g., 'What's the weather like in London?')."

    current = get_current(city) if date is None else None
    forecast = get_forecast(city) if date is not None else None
    return build_response(intent, city, date, current, forecast)

if __name__ == "__main__":
    print("🌦️  Weather Chatbot — type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break
        print("Bot:", chatbot(user_input))
