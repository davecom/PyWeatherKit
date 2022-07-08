# weatherkit/client.py
# A third-party library for Apple's WeatherKit API.
# Copyright 2022 David Kopec
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
import requests
from weatherkit.token import generate_token
from time import time


class TokenExpiredError(Exception):
    pass


class WKClient:
    # Generates a WKClient that can connect to WeatherKit.
    # *key_path* should be the path to a private key file.
    # *expiry* is the number of seconds the client should be valid for.
    # *team_id* is the 10 digit Apple Developer team id
    # *key_id* is the 10 digit id associated with the private key.
    # *service_id* is the custom id you specified when you created the service.
    def __init__(self, team_id: str, service_id: str, key_id: str, key_path: str, expiry: int = 3600):
        self.token = generate_token(team_id, service_id, key_id, key_path, expiry)

    # Returns the current weather for *latitude* and *longitude*.
    # *latitude* and *longitude* are floats.
    # *language* is a string representing the language to use as a 2 letter code.
    # *timezone* is a string representing the timezone to use.
    # *dataSets* is a list of strings representing the data sets to return which can include:
    # currentWeather, forecastDaily, forecastHourly, forecastNextHour, or weatherAlerts
    def get_weather(self, latitude: float, longitude: float, language: str = "en", timezone: str = "America/New_York",
                    dataSets: list[str] = ["currentWeather", "forecastDaily"]) -> dict:
        if self.token.expiry < time():
            raise TokenExpiredError("Token has expired")
        url = f"https://weatherkit.apple.com/api/v1/weather/{language}/{latitude}/{longitude}"
        headers = {
            "Authorization": f"Bearer {self.token.token}"
        }
        params = {
            "timezone": timezone,
            "dataSets": ",".join(dataSets)
        }
        response = requests.get(url, headers=headers, params=params)

        return response.json()


