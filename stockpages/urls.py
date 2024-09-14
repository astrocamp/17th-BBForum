from django.urls import path

from . import views

app_name = "stocks"

urlpatterns = [
    path("<int:id>", views.stock_data, name="stock_data"),
]
