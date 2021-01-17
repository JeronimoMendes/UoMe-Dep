#common_balance/urls.py

from django.conf.urls import url, include
from django.urls import path
from .views import debt_dashboard

urlpatterns = [
    url(r"debt_dashboard/", debt_dashboard)
]