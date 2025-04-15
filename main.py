from transformers import pipeline
import requests
import re
from datetime import datetime
import dateparser

API_KEY = "5ebfaae5335ce790b0cb60f2d1dfd0e9"  # Replace with your OpenWeatherMap API key

# Load zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Labels for intent classification
label_to_intent = {
    "What's the current weather?": "get_current_weather",
    "What's the temperature?": "get_temperature",
    "Will it rain?": "get_rain_info",
    "Is it windy?": "get_wind_info",
    "What's the humidity?": "get_humidity",
    "What will the weather be like later?": "get_forecast",
    "What can you do?": "get_help"
}
labels = list(label_to_intent.keys())

# ----- Utility Functions ----- #

def extract_city_and_date(user_input):
    """Extracts the city and date (if any) from the user input."""
    # Try to parse the date using the dateparser library
    date = dateparser.parse(user_input, settings={'PREFER_DATES_FROM': 'future'})
    
    # Extract city using regex pattern for cities after 'in'
    city_match = re.search(r"in ([A-ZÀ-Ùa-zà-ù\s]+)", user_input)
    city = city_match.group(1).strip() if city_match else None
    return city, date

def classify_intent(user_input):
    """Returns the matched intent from user input."""
    result = classifier(user_input, labels)
    top_label = result['labels'][0]
    score = result['scores'][0]
    print(f"Intent Match: {top_label} ({score:.2f})")
    return label_to_intent[top_label] if score > 0.5 else None

def get_weather(city):
    """Gets current weather for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()
    return data if data.get("cod") == 200 else None

def get_forecast(city):
    """Gets 5-day weather forecast for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()
    print(data)
    return data if data.get("cod") == "200" else None

def generate_response(intent, city=None, date=None, weather_data=None, forecast_data=None):
    if intent == "get_help":
        return (
            "I can help you with weather information! Try asking:\n"
            "- What's the weather like in Paris?\n"
            "- Will it rain in Rome tomorrow?\n"
            "- What's the temperature in Berlin?\n"
            "- How windy is it in Madrid?\n"
            "- What's the humidity in Tokyo?\n"
            "- What can you do?\n"
        )
    print(date)

    if intent == "get_forecast":
        # If no date is provided, fallback to current weather
        if not date:
            intent = "get_current_weather"
            weather_data = get_weather(city)

        else:
            if not forecast_data:
                return f"Sorry, I couldn't get forecast data for {city}."

            response = f"Here's the forecast for {city} on {date.strftime('%A, %B %d')}:\n"
            found = False

            for entry in forecast_data["list"]:
                dt = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
                if dt.date() == date.date():
                    temp = entry["main"]["temp"]
                    desc = entry["weather"][0]["description"]
                    response += f"- {dt.strftime('%H:%M')}: {desc}, {temp}°C\n"
                    found = True

            return response if found else f"Sorry, I couldn't find forecast data for {city} on that date."

    if not weather_data:
        return f"Sorry, I couldn't find weather info for '{city}'."

    desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind = weather_data["wind"]["speed"]

    if intent == "get_current_weather":
        return f"In {city}, it's currently {desc} with a temperature of {temp}°C."
    elif intent == "get_temperature":
        return f"The temperature in {city} is {temp}°C."
    elif intent == "get_rain_info":
        if "rain" in desc.lower():
            return f"Yes, rain is expected in {city}: {desc}."
        return f"No rain is expected in {city} right now: {desc}."
    elif intent == "get_wind_info":
        return f"The wind speed in {city} is {wind} m/s."
    elif intent == "get_humidity":
        return f"The humidity in {city} is {humidity}%."
    else:
        return "I'm not sure how to help with that."

# ----- Main Chat Function ----- #

def chatbot(user_input):
    intent = classify_intent(user_input)

    if intent == "get_help":
        return generate_response(intent)

    city, date = extract_city_and_date(user_input)

    if not city:
        return "Please include a city in your question (e.g., 'What's the weather like in London?')."

    print(f"City: {city} | Date: {date} | Intent: {intent}")

    if intent == "get_forecast" and date:
        forecast_data = get_forecast(city)
        return generate_response(intent, city=city, date=date, forecast_data=forecast_data)
    else:
        weather_data = get_weather(city)
        return generate_response(intent, city=city, weather_data=weather_data)

# ----- Run Chat Loop ----- #

if __name__ == "__main__":
    print("🌦️  Weather Chatbot — type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        response = chatbot(user_input)
        print("Bot:", response)
