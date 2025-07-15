from intent_classifier import IntentClassifier

def test_intent_classification_weather():
    classifier = IntentClassifier()
    intent = classifier.classify("What's the weather like in Rome?")
    assert intent == "weather"

def test_intent_classification_temperature():
    classifier = IntentClassifier()
    intent = classifier.classify("What temperature there will in London tomorrow?")
    assert intent == "temperature"

def test_intent_classification_windy():
    classifier = IntentClassifier()
    intent = classifier.classify("How strong will be the wind on Friday in New York?")
    assert intent == "wind"

def test_intent_classification_rain():
    classifier = IntentClassifier()
    intent = classifier.classify("Is it raining in Florence?")
    assert intent == "rain"

def test_intent_classification_humidity():
    classifier = IntentClassifier()
    intent = classifier.classify("Can you tell me what's the current humidity in Paris?")
    assert intent == "humidity"

def test_intent_classification_help():
    classifier = IntentClassifier()
    intent = classifier.classify("What can you do?")
    assert intent == "help"

def test_intent_unknown():
    classifier = IntentClassifier()
    intent = classifier.classify("This is a random string for test purposes.")
    assert intent is None
