from django.urls import path

from . import views

app_name = "stocks"

urlpatterns = [
    path("<int:id>", views.stock_detele, name="stock_detele"),
]
