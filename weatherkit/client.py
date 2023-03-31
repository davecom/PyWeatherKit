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
from datetime import datetime
from http import HTTPStatus
from weatherkit.forecast import DailyForecast, daily_forecast_dictionary_to_object


class TokenExpiredError(Exception):
    pass


class WKClient:
    # Generates a WKClient that can connect to WeatherKit.
    # *team_id* is the 10 digit Apple Developer team id
    # *service_id* is the custom id you specified when you created the service.
    # *key_id* is the 10 digit id associated with the private key.
    # *key_path* should be the path to a private key file
    # *expiry* is the number of seconds the client should be valid for.
    def __init__(self, team_id: str, service_id: str, key_id: str, key_path: str, expiry: int = 3600):
        self.token = generate_token(
            team_id, service_id, key_id, key_path, expiry)
    
    # Returns a list of DailyForecast objects for *latitude* and *longitude*.
    # *latitude* and *longitude* are floats.
    # *language* is a string representing the language to use as a 2 letter code.
    # *timezone* is a string representing the timezone to use.
    # *imperial* is a boolean representing whether to use imperial units (default True)
    def get_simple_forecast(self, latitude: float, longitude: float, language: str = "en", timezone: str = "America/New_York", imperial = True) -> list[DailyForecast]:
        forecast = self.get_weather(latitude, longitude, language, timezone, dataSets=["forecastDaily"])
        return [daily_forecast_dictionary_to_object(forecast, imperial) for forecast in forecast["forecastDaily"]["days"]]

    # Returns the current weather for *latitude* and *longitude*.
    # *latitude* and *longitude* are floats.
    # *language* is a string representing the language to use as a 2 letter code.
    # *timezone* is a string representing the timezone to use.
    # *dataSets* is a list of strings representing the data sets to return which can include:
    # currentWeather, forecastDaily, forecastHourly, forecastNextHour, or weatherAlerts
    # *dailyStart* optional datetime parameter for specifying when the forecast should start
    # *dailyEnd* optional datetime parameter for specifying when the forecast should end
    def get_weather(self, latitude: float, longitude: float, language: str = "en", timezone: str = "America/New_York",
                    dataSets: list[str] = ["currentWeather", "forecastDaily"], currentAsOf: datetime = None, dailyStart: datetime = None, dailyEnd: datetime = None) -> dict:
        if self.token.expiry_time < time():
            raise TokenExpiredError("Token has expired")
        url = f"https://weatherkit.apple.com/api/v1/weather/{language}/{latitude}/{longitude}"
        headers = {
            "Authorization": f"Bearer {self.token.token}"
        }
        # Co-opted from stackoverflow answer: https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testing
        retries = 3
        retry_codes = [
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]
        params = {
            "timezone": timezone,
            "dataSets": ",".join(dataSets),
        }
        # Add extra (optional) params for historical data
        # Apple expects datetimes to be in format like:
        #   YYYY-MM-DDTHour:Minute:SecondZ (sent in utc)
        if dailyStart is not None and dailyEnd is not None:
            # Check if
            if type(dailyStart) == datetime:
                params["dailyStart"] = dailyStart.strftime("%Y-%m-%dT%XZ")
            else:
                raise (TypeError("dailyStart should be a datetime object"))
            if type(dailyEnd) == datetime:
                params["dailyEnd"] = dailyEnd.strftime("%Y-%m-%dT%XZ")
            else:
                raise (TypeError("dailyEnd should be a datetime object"))
            if currentAsOf is not None:
                if type(currentAsOf) == datetime:
                    params["currentAsOf"] = currentAsOf.strftime(
                        "%Y-%m-%dT%XZ")
                else:
                    raise (TypeError(f"currentAsOf should be a datetime object"))
            else:
                # User didn't select currentAsOf, assume is dailyStart
                params["currentAsOf"] = dailyStart.strftime("%Y-%m-%dT%XZ")
        for n in range(retries):
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                break

            except requests.HTTPError as exc:
                code = exc.response.status_code

                if code in retry_codes:
                    # retry after n seconds
                    time.sleep(n)
                    continue

                raise
        response.raise_for_status()
        return response.json()
