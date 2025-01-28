from django.urls import path
from . import views


urlpatterns = [
    path("", views.BirdListView.as_view()),
    path("assets/<int:bird_id>/", views.BirdsetView.as_view()),
    path("<int:bird_id>/", views.BirdView.as_view()),
    path("predict/", views.BirdPredictionView.as_view()),
]
