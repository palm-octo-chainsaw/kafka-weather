import requests


class CurrentWeather:
    def __init__(self,
                 url: str = 'https://api.open-meteo.com/v1/forecast',
                 latitude: float = 42.6977,
                 longitude: float = 23.3219,
                 ) -> None:
        self.url = url
        self.latitude = latitude
        self.longitude = longitude

    def get_url(self) -> str:
        return self.url

    def get_params(self) -> dict:
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'current': [
                'temperature_2m', 'relative_humidity_2m',
                'apparent_temperature', 'is_day',
                'precipitation', 'rain', 'showers',
                'snowfall', 'weather_code', 'cloud_cover',
                'pressure_msl', 'surface_pressure',
                'wind_speed_10m', 'wind_direction_10m',
                'wind_gusts_10m'
            ],
            'timezone': 'auto',
        }

    def get_current_weather(self) -> dict:
        return requests.get(self.url, params=self.get_params()).json()
