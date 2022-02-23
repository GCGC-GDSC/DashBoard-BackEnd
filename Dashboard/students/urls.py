from rest_framework import routers
from django.urls import path, include, re_path
from . import utils
from .views import *

urlpatterns = [
    path('', GraduateList.as_view(), name='graduates-list'),
    path('inst/<str:institute>',
         InstituteGradList.as_view(),
         name='institute-list'),
    path('overall/<stream>/', Overall.as_view(), name='overall-view'),
    path('select/<institute>/<grad>',
         SelectGraduates.as_view(),
         name='data-select-view'),
    path('update/<pk>', UpdateGraduates.as_view(), name='data-update-view'),
    #re_path(r'^upload/', utils.FileUploadView.as_view()),
    #re_path(r'^upload/', FileUploadView.as_view()),
    path('gbstats/', Gbstats.as_view(), name='test-list'),
    path('exportexcel/', utils.export_data_to_excel, name='export-excel'),
    path('download/<str:name>',
         utils.FileDownloadListAPIView.as_view(),
         name='download-api'),
    path('logs', utils.LogsDataListAPIView.as_view(), name='logs-api')
]
