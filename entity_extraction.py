import re
import string
from dateparser.search import search_dates

class EntityExtractor:
    STOPWORDS = {"what", "is", "the", "weather", "like", "will", "it", "be", "going", "to", "rain", "tomorrow", "humidity", "temperature", "forecast", "in", "at", "on", "and", "of", "for"}

    def extract(self, user_input):
        date = None
        parsed = search_dates(user_input, settings={'PREFER_DATES_FROM': 'future'})
        if parsed:
            found_text, date = parsed[0]
            cleaned_input = user_input.replace(found_text, "")
        else:
            cleaned_input = user_input

        city_match = re.search(r"\b(?:in|at)\s+([A-ZÀ-Ùa-zà-ù\s]+)", cleaned_input)
        if city_match:
            city = city_match.group(1).strip()
        else:
            words = cleaned_input.split()
            candidates = [w for w in words if w.lower() not in self.STOPWORDS]
            city = candidates[-1] if candidates else None

        if city:
            city = city.strip(string.punctuation)
        return city, date
