from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send_prompt/", views.send_prompt, name="send_prompt")
]