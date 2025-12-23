from django.urls import path
from .views import index

app_name = "newspaper"

urlpatterns = [
    path("", index, name="index"),
]
