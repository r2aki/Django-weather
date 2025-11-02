from django.urls import path
from .views import ViewWeather

urlpatterns = [
    path('', ViewWeather, name ='view_weather'),
]
