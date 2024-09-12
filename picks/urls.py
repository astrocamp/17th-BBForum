from django.urls import path

from .views import PickStockAPI

app_name = "picks"

urlpatterns = [
    path("pick/<int:id>/", PickStockAPI.as_view(), name="pick_api"),
    path("unpick/<int:id>/", PickStockAPI.as_view(), name="unpick_api"),
    # path("check_follow/<int:id>/", CheckFollowStatusAPI.as_view(), name="check_follow_api"),
]
