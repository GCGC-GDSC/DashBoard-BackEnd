from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('institite/<str:institute>', GitUgList.as_view()),
    path('gis', GisUgList.as_view()),
    path('Pharmacy', PharmacyList.as_view()),
    path('BBA', Gim_BBA_BCOMList.as_view()),
    path('MBA', Gim_MBAList.as_view()),
    # path('campus/', CampusesList.as_view(), name='campus-list'),
    # path('institute/<str:campus>', InstituteList.as_view(), name='institute-list'),
]