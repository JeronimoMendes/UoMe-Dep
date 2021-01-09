# users/urls.py

from django.conf.urls import url, include
from users.views import dashboard, register, edit_info

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls")), 
    url(r"edit_info/", edit_info)
]