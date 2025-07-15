from transformers import pipeline

class IntentClassifier:
    def __init__(self):
        self.labels = [
            "What's the weather like?",
            "What's the temperature?",
            "Will it rain?",
            "Is it windy?",
            "What's the humidity?",
            "What can you do?"
        ]
        self.label_to_intent = {
            "What's the weather like?": "weather",
            "What's the temperature?": "temperature",
            "Will it rain?": "rain",
            "Is it windy?": "wind",
            "What's the humidity?": "humidity",
            "What can you do?": "help"
        }
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify(self, text: str):
        result = self.classifier(text, self.labels)
        best_label, score = result['labels'][0], result['scores'][0]
        return self.label_to_intent.get(best_label) if score > 0.3 else None
