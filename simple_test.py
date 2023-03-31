# simple_test.py
# Does a simple test of the weatherkit library, retrieving a forecast for one location and displaying it.
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
from argparse import ArgumentParser
from weatherkit.client import WKClient

def display_forecast(client: WKClient, latitude: float, longitude: float):
    forecast = client.get_simple_forecast(latitude, longitude)
    for day in forecast:
        print(f"{day.day_of_week}: {day.daytime_icon} with a high of {round(day.temperature_high)} and a low of {round(day.temperature_low)}")


if __name__ == "__main__":
    # parse the command line arguments which are the
    # team_id, service_id, key_id, key_path, latitude, and longitude
    parser = ArgumentParser()
    parser.add_argument("team_id", help="The team ID for your WeatherKit account")
    parser.add_argument("service_id", help="The service ID for your WeatherKit account")
    parser.add_argument("key_id", help="The key ID for your WeatherKit account")
    parser.add_argument("key_path", help="The path to the key file for your WeatherKit account")
    parser.add_argument("latitude", type=float, help="The latitude of the location you want to get a forecast for")
    parser.add_argument("longitude", type=float, help="The longitude of the location you want to get a forecast for")
    args = parser.parse_args()
    client = WKClient(args.team_id, args.service_id, args.key_id, args.key_path)
    display_forecast(client, args.latitude, args.longitude)