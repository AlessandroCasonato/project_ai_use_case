from intent_classifier import IntentClassifier
from entity_extraction import EntityExtractor
from weather_api import WeatherAPI
from response_builder import ResponseBuilder

class WeatherChatbot:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.extractor = EntityExtractor()
        self.weather_api = WeatherAPI()
        self.responder = ResponseBuilder()

    def handle_input(self, user_input):
        intent = self.classifier.classify(user_input)
        if not intent:
            return "I'm not sure how to help with that."

        if intent == "help":
            return self.responder.build(intent, None, None, None, None)

        city, date = self.extractor.extract(user_input)
        if not city:
            return "Please include a city in your question (e.g., 'What's the weather like in London?')."

        current = self.weather_api.get_current(city) if date is None else None
        forecast = self.weather_api.get_forecast(city) if date is not None else None

        return self.responder.build(intent, city, date, current, forecast)

