from rest_framework import routers
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', GraduateList.as_view(), name='graduates-list'),
    path('<str:institute>', InstituteGradList.as_view(),
         name='institute-list'),
    # path('crud/graduates/<int:pk>', GraduateRetrieveUpdateDestroy.as_view(), name='graduates-crud'),
    # path('crud/institute/<int:pk>', InstituteRetrieveUpdateDestroy.as_view(), name='institute-crud'),
    # path('crud/campus/<int:pk>', CampusRetrieveUpdateDestroy.as_view(), name='campus-crud'),
    # path('campus/', CampusesList.as_view(), name='campus-list'),
    # path('institute/<str:campus>', InstituteList.as_view(), name='institute-list'),
    path('overall/<stream>/', Overall.as_view(), name='overall-view')
]
