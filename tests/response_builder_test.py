from response_builder import ResponseBuilder
from datetime import datetime

def test_help_response():
    rb = ResponseBuilder()
    response = rb.build("help", None, None, None, None)
    assert "I can give you weather info" in response

def test_weather_response_current():
    rb = ResponseBuilder()
    current = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25.0, "humidity": 60},
        "wind": {"speed": 4.5}
    }
    response = rb.build("weather", "Rome", None, current, None)
    assert "Rome" in response and "25.0°C" in response
