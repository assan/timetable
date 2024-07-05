# timetable_week/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduling.urls')),  # Включение маршрутов из приложения scheduling
]
