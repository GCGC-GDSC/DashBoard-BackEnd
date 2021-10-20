from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'GIT', views.GitViewSet)
router.register(r'GIS', views.GisViewset)

urlpatterns = [
    path('', include(router.urls))
]