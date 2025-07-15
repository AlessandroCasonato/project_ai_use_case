from intent_classifier import IntentClassifier

def test_intent_classification_weather():
    classifier = IntentClassifier()
    intent = classifier.classify("What's the weather like in Rome?")
    assert intent == "weather"

def test_intent_classification_help():
    classifier = IntentClassifier()
    intent = classifier.classify("What can you do?")
    assert intent == "help"

def test_intent_unknown():
    classifier = IntentClassifier()
    intent = classifier.classify("This is a random string for test purposes.")
    assert intent is None
