from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('compnay_list', CompanyList.as_view()),
    path('institute_level', InstituteLevel.as_view()),
    path('crud/course/<int:pk>/', CourseRetrieveUpdateDestroy.as_view()),
    path('crud/company/<int:pk>/', CompanyRetrieveUpdateDestroy.as_view()),# this has to be changed
    path('crud/companycourse/<int:pk>/', CompanyCousesRetrieveUpdateDestroy.as_view())
]