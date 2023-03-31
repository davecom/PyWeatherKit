# PyWeatherKit
A simple Python wrapper for [Apple's WeatherKit REST API](https://developer.apple.com/documentation/weatherkitrestapi).

You need an Apple developer account to use this library and you should first follow the [setup instructions](https://developer.apple.com/documentation/weatherkitrestapi/request_authentication_for_weatherkit_rest_api) in their documentation.

It has a simple interface for retrieving a raw dictionary of weather data from the API, and a method for retrieving simplified daily forecasts as Pythonic objects. Pull requests are welcome!

## Install

```bash
pip install pyweatherkit
```

## Simple Forecast Usage

```python
from weatherkit.client import WKClient 
client = WKClient("YOUR TEAM ID", "YOUR SERVICE ID", "YOUR KEY ID", "PATH TO YOUR PRIVATE KEY FILE")
forecast = client.get_simple_forecast(latitude, longitude)
for day in forecast:
    print(f"{day.day_of_week}: {day.daytime_icon} with a high of {round(day.temperature_high)} and a low of {round(day.temperature_low)}")
```

Assuming you input all of the correct client authentication parameters and a valid latitude and longitude, this should result in something like:

```bash
Thursday: 🌤️ with a high of 38 and a low of 23
Friday: 🌧️ with a high of 45 and a low of 22
Saturday: 🌧️ with a high of 67 and a low of 40
...
```

## Pulling Full Data Sets

```python
from weatherkit.client import WKClient 
client = WKClient("YOUR TEAM ID", "YOUR SERVICE ID", "YOUR KEY ID", "PATH TO YOUR PRIVATE KEY FILE")
res = client.get_weather(44.50572, -73.24026)
```

You can also specify the language of the response, the timezone, and the specific datasets you need.

### Historical Data Pull 
Only available from dates after 08/01/2021 (as of 2023-03-23)
```python
from weatherkit.client import WKClient
from datetime import datetime

# Set dates 
dailyStart = datetime.strptime("2022-11-29", "%Y-%m-%d")
dailyEnd = datetime.strptime("2022-11-30", "%Y-%m-%d")
currentAsOf = datetime.strptime("2022-11-29", "%Y-%m-%d")

client = WKClient("YOUR TEAM ID", "YOUR SERVICE ID", "YOUR KEY ID", "PATH TO YOUR PRIVATE KEY FILE")
res = client.get_weather(44.50572, -73.24026, dailyStart=dailyStart, dailyEnd=dailyEnd, currentAsOf=currentAsOf)
```

## Test/Example Program

Try running simple_test.py from the same directory as this package.

```bash
python3 simple_test.py your_team_id your_service_id your_key_id your_key_path your_latitude your_longitude
```
