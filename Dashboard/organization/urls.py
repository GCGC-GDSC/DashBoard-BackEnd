from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('campus/', CampusList.as_view(), name='campus-list'),
    path('institute/', InstituteList.as_view(), name='campus-list'),
    path('courses/', CoursesList.as_view(), name='courses-list'),
    path('streams/', StreamsList.as_view(), name='streams-list'),
]
