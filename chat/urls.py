from django.urls import path
from . import views

urlpatterns = [
    path("birdchat/", views.BirdChatterView.as_view(), name="chat_about_birds"),
]