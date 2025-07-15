from chatbot import WeatherChatbot

def test_help_intent_shortcut():
    bot = WeatherChatbot()
    response = bot.handle_input("What can you do?")
    assert "I can give you weather info" in response

def test_no_city_provided():
    bot = WeatherChatbot()
    response = bot.handle_input("Will it rain tomorrow?")
    assert "Please include a city" in response
