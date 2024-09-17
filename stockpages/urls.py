from django.urls import path

from . import views

app_name = "stocks"

urlpatterns = [
    path("twii", views.stock_data_twii, name="stock_data_twii"),
    path("<str:id>", views.stock_data, name="stock_data"),
]
