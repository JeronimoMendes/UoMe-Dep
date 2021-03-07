# users/urls.py

from django.conf.urls import url, include
from django.urls import path
from users.views import dashboard, register, user_search_view, friends, welcome, dashboard2, preferences

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls")), 
    url(r'search/', user_search_view, name="search"),
    url(r"friends/", friends),
    url(r"welcome", welcome),
    url("preferences/", preferences)
]