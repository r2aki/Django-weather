from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests


load_dotenv()


def ViewWeather(request: HttpRequest) -> HttpResponse:
    api = os.getenv("WEATHER_API_KEY")
    print("Loaded API key:", repr(api))

    if not api:
        return HttpResponse("API key not configured!", status=500)

    city = "Москва"
    lang = "ru"
    url = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&lang={lang}&units=metric"
    response = requests.get(url.format(city=city, API=api, lang=lang)).json()
    # print("Response:", response.json())

    city_info = {
        "city": city,
        "temperature": response.get("main", {}).get("temp"),
        "pressure": response.get("main", {}).get("pressure"),
        "description": response.get("weather", [{}])[0].get("description"),
        "icon": response.get("weather", [{}])[0].get("icon"),
    }

    context = {
        "info": city_info
    }
    return render(request, 'weather/weather.html', context=context)
