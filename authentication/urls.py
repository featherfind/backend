from django.urls import path
from .views import SimpleAuthenticationView

urlpatterns = [
    path('', SimpleAuthenticationView.as_view(), name='simple-authenticate'),
]
