from rest_framework import routers
from django.urls import path, include
from .views import (CompanyList, InstituteLevel)

urlpatterns = [
    path('compnay_list', CompanyList.as_view()),
    path('institute_level', InstituteLevel.as_view())
]
