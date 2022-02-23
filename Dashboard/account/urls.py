from rest_framework import routers
from django.urls import path, include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('verify/<str:email>', Authenticate.as_view(), name='auth-account'),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    path('getusertoken/<str:eid>/',
         GetTokenOfUser.as_view(),
         name='get-user-token')
]
