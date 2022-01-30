from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('verify/<str:email>', Authenticate.as_view(), name='auth-account'),
]
