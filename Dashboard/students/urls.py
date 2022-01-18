from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', GraduateList.as_view(), name='graduates-list'),
    path('<str:institute>', InstituteGradList.as_view(),
         name='institute-list'),
    path('overall/<stream>/', Overall.as_view(), name='overall-view'),
    path('select/<institute>/<grad>', SelectGraduates.as_view(), name='data-select-view'),
    path('update/<pk>', UpdateGraduates.as_view(), name='data-update-view')
]
