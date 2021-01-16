# users/urls.py

from django.conf.urls import url, include
from django.urls import path
from users.views import dashboard, register, edit_info, user_search_view, friend_request, friends

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls")), 
    url(r"edit_info/", edit_info),
    url(r'search/', user_search_view, name="search"),
    url(r"friend_request/", friend_request),
    url(r"friends/", friends)
]