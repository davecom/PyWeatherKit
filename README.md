# PyWeatherKit
A simple Python wrapper for [Apple's WeatherKit REST API](https://developer.apple.com/documentation/weatherkitrestapi).

You need an Apple developer account to use this library and you should first follow the [setup instructions](https://developer.apple.com/documentation/weatherkitrestapi/request_authentication_for_weatherkit_rest_api) in their documentation.

So far it doesn't do much beyond retrieving a dictionary of weather data because that's all I need. Pull requests are welcome though!

## Install

```bash
pip install pyweatherkit
```

## Usage

```python
from weatherkit.client import WKClient 
client = WKClient("YOUR TEAM ID", "YOUR SERVICE ID", "YOUR KEY ID", "PATH TO YOUR PRIVATE KEY FILE")
res = client.get_weather(44.50572, -73.24026)
```

You can also specify the language of the response, the timezone, and the specific datasets you need.