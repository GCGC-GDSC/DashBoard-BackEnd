from django.urls import path, include
from .api import SimpleApI
urlpatterns = [
    path('api/hello', SimpleApI.as_view() ),
]