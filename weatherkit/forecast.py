# weatherkit/forecast.py
# A third-party library for Apple's WeatherKit API.
# Copyright 2023 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from time import time
from datetime import datetime
from dataclasses import dataclass


def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32

MM_TO_INCHES = 0.0393700787402
KPH_TO_MPH = 0.621371191666667

weather_icons = {'Clear': '☀️', 'Cloudy': '☁️', 'Dust': '💨', 'Fog': '🌫️', 'Haze': '🌫️', 'MostlyClear': '🌤️', 'MostlyCloudy': '⛅', 'PartlyCloudy': '⛅', 'ScatteredThunderstorms': '⛈️', 'Smoke': '🌫️', 'Breezy': '💨', 'Windy': '💨', 'Drizzle': '🌧️', 'HeavyRain': '🌧️', 'Rain': '🌧️', 'Showers': '🌦️', 'Flurries': '❄️', 'HeavySnow': '❄️', 'MixedRainAndSleet': '🥶', 'MixedRainAndSnow': '🥶', 'MixedRainfall': '🥶', 'MixedSnowAndSleet': '🥶', 'ScatteredShowers': '🌦️', 'ScatteredSnowShowers': '❄️', 'Sleet': '🥶', 'Snow': '❄️', 'SnowShowers': '❄️', 'Blizzard': '❄️', 'BlowingSnow': '❄️', 'FreezingDrizzle': '🥶', 'FreezingRain': '🥶', 'Frigid': '', 'Hail': '🥶', 'Hot': '🥵', 'Hurricane':'🌀', "IsolatedThunderstorms":'⛈️', "SevereThunderstorm":'⛈️', "Thunderstorm":'⛈️', "Tornado":'🌪️', "TropicalStorm":'🌀' }

# A class for representing a daily forecast
@dataclass
class DailyForecast:
    forecast_start: datetime
    forecast_end: datetime
    daytime_condition: str
    overnight_condition: str
    daytime_humidity: float
    overnight_humidity: float
    daytime_precipitation_amount: float
    overnight_precipitation_amount: float
    daytime_precipitation_chance: float
    overnight_precipitation_chance: float
    daytime_precipitation_type: str
    overnight_precipitation_type: str
    daytime_snowfall_amount: float
    overnight_snowfall_amount: float
    daytime_wind_speed: float
    overnight_wind_speed: float
    sunrise: datetime
    sunset: datetime
    temperature_high: float
    temperature_low: float
    imperial: bool
    temperature_unit: str = "°C"
    precipitation_unit: str = "mm"
    snowfall_unit: str = "mm"
    wind_speed_unit: str = "km/h"
    
    def __post_init__(self):
        if self.imperial:
            self.temperature_high = celsius_to_fahrenheit(self.temperature_high)
            self.temperature_low = celsius_to_fahrenheit(self.temperature_low)
            self.daytime_wind_speed = self.daytime_wind_speed * KPH_TO_MPH
            self.overnight_wind_speed = self.overnight_wind_speed * KPH_TO_MPH
            self.daytime_snowfall_amount = self.daytime_snowfall_amount * MM_TO_INCHES
            self.overnight_snowfall_amount = self.overnight_snowfall_amount * MM_TO_INCHES
            self.daytime_precipitation_amount = self.daytime_precipitation_amount * MM_TO_INCHES
            self.overnight_precipitation_amount = self.overnight_precipitation_amount * MM_TO_INCHES
            self.temperature_unit = "°F"
            self.precipitation_unit = "in"
            self.snowfall_unit = "in"
            self.wind_speed_unit = "mph"
    
    @property
    def daytime_icon(self) -> str:
        return weather_icons.get(self.daytime_condition, "🌞")
    
    @property
    def overnight_icon(self) -> str:
        return weather_icons.get(self.overnight_condition, "🌝")
    
    @property
    def day_of_week(self) -> str:
        return self.forecast_start.strftime("%A")

def daily_forecast_dictionary_to_object(d: dict, imperial: bool) -> DailyForecast:
    return DailyForecast(
        forecast_start=datetime.fromisoformat(d['forecastStart']),
        forecast_end=datetime.fromisoformat(d['forecastEnd']),
        daytime_condition=d['daytimeForecast']['conditionCode'],
        overnight_condition=d['overnightForecast']['conditionCode'],
        daytime_humidity=d['daytimeForecast']['humidity'],
        overnight_humidity=d['overnightForecast']['humidity'],
        daytime_precipitation_amount=d['daytimeForecast']['precipitationAmount'],
        overnight_precipitation_amount=d['overnightForecast']['precipitationAmount'],
        daytime_precipitation_chance=d['daytimeForecast']['precipitationChance'],
        overnight_precipitation_chance=d['overnightForecast']['precipitationChance'],
        daytime_precipitation_type=d['daytimeForecast']['precipitationType'],
        overnight_precipitation_type=d['overnightForecast']['precipitationType'],
        daytime_snowfall_amount=d['daytimeForecast']['snowfallAmount'],
        overnight_snowfall_amount=d['overnightForecast']['snowfallAmount'],
        daytime_wind_speed=d['daytimeForecast']['windSpeed'],
        overnight_wind_speed=d['overnightForecast']['windSpeed'],
        sunrise=datetime.fromisoformat(d['sunrise']),
        sunset=datetime.fromisoformat(d['sunset']),
        temperature_high=d['temperatureMax'],
        temperature_low=d['temperatureMin'],
        imperial=imperial
    )
