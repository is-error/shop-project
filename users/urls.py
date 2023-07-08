from django.urls import path

from users.views.handle import LoginAPI
from users.views.views import LoginHistoriesAPI

urlpatterns = [
    path("auth/login", LoginAPI.as_view(), name="login-api"),
    path(
        "auth/login-histories", LoginHistoriesAPI.as_view(), name="login-histories-api"
    ),
]
