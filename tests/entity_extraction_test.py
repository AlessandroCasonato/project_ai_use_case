from entity_extraction import EntityExtractor
from datetime import datetime

def test_extract_city_and_date():
    extractor = EntityExtractor()
    city, date = extractor.extract("Will it rain in Berlin tomorrow?")
    assert city.lower() == "berlin"
    assert isinstance(date, datetime)

def test_extract_only_city():
    extractor = EntityExtractor()
    city, date = extractor.extract("What's the temperature in Florence?")
    assert city.lower() == "florence"
    assert date is None

def test_no_city_found():
    extractor = EntityExtractor()
    city, date = extractor.extract("How are you today?")
    assert not city
