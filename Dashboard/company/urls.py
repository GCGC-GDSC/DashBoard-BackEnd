from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('git', GitList.as_view(), name='graduates-list'),
    path('gis', GisList.as_view(), name='graduates-list'),
    path('Pharmacy', PharmacyList.as_view(), name='graduates-list'),
    path('BBA', Gim_BBA_BCOMList.as_view(), name='graduates-list'),
    path('MBA', Gim_MBAList.as_view(), name='graduates-list'),
    # path('campus/', CampusesList.as_view(), name='campus-list'),
    # path('institute/<str:campus>', InstituteList.as_view(), name='institute-list'),
]