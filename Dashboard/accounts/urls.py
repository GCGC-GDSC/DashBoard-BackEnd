from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/<str:email>', Authenticate.as_view(), name='auth-account'),
]
