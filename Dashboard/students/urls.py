from rest_framework import routers
from django.urls import path, include, re_path
from . import utils
from .views import *

urlpatterns = [
    path('<str:year>', GraduateList.as_view(), name='graduates-list'),
    path('<str:year>/inst/<str:institute>/<str:campus>',
         InstituteGradList.as_view(),
         name='institute-list'),
    path('<str:year>/overall/<stream>', Overall.as_view(),
         name='overall-view'),
    path('<str:year>/select/<str:institute>/<str:grad>/<str:campus>',
         SelectGraduates.as_view(),
         name='data-select-view'),
    path('<str:year>/update/<pk>',
         UpdateGraduates.as_view(),
         name='data-update-view'),
    #re_path(r'^upload/', utils.FileUploadView.as_view()),
    #re_path(r'^upload/', FileUploadView.as_view()),
    path('<str:year>/gbstats', Gbstats.as_view(), name='test-list'),
    path('exportexcel', utils.export_data_to_excel, name='export-excel'),
    path('<str:year>/download/<str:name>',
         utils.FileDownloadListAPIView.as_view(),
         name='download-api'),
    path('logs', LogsDataListAPIView.as_view(), name='logs-api'),
    path('<str:year>/programs', ProgramsGraduates.as_view(), name='courses'),
    path('compare/<str:year1>/<str:year2>/<str:coursename>/<str:grad>',
         CompareYearsData.as_view(),
         name='compare'),
     path('<str:year>/updateprograms/<pk>', UpdateGraduatesWithPrograms.as_view(), name='data-update-view-with-programs'),
]
