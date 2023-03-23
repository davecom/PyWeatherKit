# PyWeatherKit
A simple Python wrapper for [Apple's WeatherKit REST API](https://developer.apple.com/documentation/weatherkitrestapi).

You need an Apple developer account to use this library and you should first follow the [setup instructions](https://developer.apple.com/documentation/weatherkitrestapi/request_authentication_for_weatherkit_rest_api) in their documentation.

So far it doesn't do much beyond retrieving a dictionary of weather data because that's all I need. Pull requests are welcome though!

## Install

```bash
pip install pyweatherkit
```

## Standard Usage

```python
from weatherkit.client import WKClient 
client = WKClient("YOUR TEAM ID", "YOUR SERVICE ID", "YOUR KEY ID", "PATH TO YOUR PRIVATE KEY FILE")
res = client.get_weather(44.50572, -73.24026)
```

You can also specify the language of the response, the timezone, and the specific datasets you need.

## Historical Data Pull 
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
