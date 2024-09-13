from django.urls import path

from .views import CheckPickStatusAPI, PickStockAPI

app_name = "picks"

urlpatterns = [
    path("picker/<int:id>/", PickStockAPI.as_view(), name="pick_api"),
    path("unpicker/<int:id>/", PickStockAPI.as_view(), name="unpick_api"),
    path(
        "check_picker/<int:id>/", CheckPickStatusAPI().as_view(), name="check_pick_api"
    ),
]
