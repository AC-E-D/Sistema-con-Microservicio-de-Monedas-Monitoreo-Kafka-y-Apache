# api/urls.py
from django.urls import path
from .views import MonedasAPIView

urlpatterns = [
    path("monedas/", MonedasAPIView.as_view(), name="api_monedas"),
]
