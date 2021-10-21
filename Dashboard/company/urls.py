from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'GIT', views.GitViewSet)
router.register(r'GIS', views.GisViewset)
router.register(r'Pharmacy', views.PharmacyViewset)
router.register(r'Business', views.Gim_BBA_BCOMViewset)
router.register(r'MBA', views.Gim_MBAViewset)

urlpatterns = [
    path('', include(router.urls))
]