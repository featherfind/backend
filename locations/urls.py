from django.urls import path
from . import views

urlpatterns = [
    path("", views.LocationListView.as_view()),
    path("<int:location_id>/", views.LocationView.as_view()),
    path("bird/", views.BirdLocationListView.as_view()),
    path("bird/<int:bird_id>/", views.BirdLocationView.as_view()),
]