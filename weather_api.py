import requests

API_KEY = "5ebfaae5335ce790b0cb60f2d1dfd0e9"

class WeatherAPI:
    def get_current(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        return data if data.get("cod") == 200 else None

    def get_forecast(self, city):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        return data if data.get("cod") == "200" else None
