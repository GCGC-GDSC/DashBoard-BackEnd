from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'campus', views.CampusViewSet)
router.register(r'institue', views.InstitueViewSet)
router.register(r'UnderGraduates', views.UnderGraduatesViewSet)
router.register(r'PostGraduates', views.PostGraduatesViewSet)

urlpatterns = [
    path('', include(router.urls))
]