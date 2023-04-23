from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("average_rate", views.get_average_exchange_rate, name="average_exchange_rate"),
    path(
        "average_value", views.get_max_min_average_value, name="max_min_average_value"
    ),
    path("major_difference", views.get_major_difference, name="major_difference"),
]
