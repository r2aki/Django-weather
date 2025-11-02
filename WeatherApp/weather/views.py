from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import os
import requests

from .models import City

# Загружаем переменные окружения
from dotenv import load_dotenv
load_dotenv()


def ViewWeather(request: HttpRequest) -> HttpResponse:
    lang = "ru"
    url_template = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&lang={lang}&units=metric"

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return HttpResponse("Ошибка: API-ключ не настроен.", status=500)

    # Получаем город из GET-запроса
    user_city_input = request.POST.get("city", "").strip()

    all_cities_data = []

    # 1 Обработка пользовательского города
    if user_city_input:
        response = requests.get(url_template.format(city=user_city_input, API=api_key, lang=lang))
        if response.status_code == 200:
            data = response.json()
            city_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data.get("wind", {}).get("speed", 0),
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "is_user_city": True,
            }
            all_cities_data.append(city_info)
        else:
            try:
                error_msg = response.json().get("message", "Неизвестная ошибка")
            except:
                error_msg = "Не удалось получить данные"
            context = {
                "all_info": [],
                "error": f"Ошибка: {error_msg}",
            }
            return render(request, 'weather/weather.html', context)

    # 2 Обработка сохранённых городов из БД
    saved_cities = City.objects.all()
    for city_obj in saved_cities:
        city_name = city_obj.name
        response = requests.get(url_template.format(city=city_name, API=api_key, lang=lang))
        if response.status_code == 200:
            data = response.json()
            city_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data.get("wind", {}).get("speed", 0),
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "is_user_city": False,
            }
            all_cities_data.append(city_info)
        # Ошибки для сохранённых городов просто пропускаем

    context = {
        "all_info": all_cities_data,
        "error": None,
    }
    return render(request, 'weather/weather.html', context)