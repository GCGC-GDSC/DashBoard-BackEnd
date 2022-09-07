from rest_framework import routers
from django.urls import path, include
from . import utils
from .views import *

urlpatterns = [
    path('<int:year>/overall/<str:stream>',
         Overall.as_view(),
         name='overall-view'),
    path('<int:year>', GraduateList.as_view(), name='graduates-list'),
    path('<int:year>/inst/<str:institute>/<str:campus>',
         InstituteGradList.as_view(),
         name='institute-list'),
    path(
        '<int:year>/select/<str:coursename>/<str:institute>/<str:grad>/<str:campus>',
        SelectGraduates.as_view(),
        name='data-select-view'),
    path('<int:year>/update/<pk>',
         UpdateGraduates.as_view(),
         name='data-update-view'),
    #     re_path(r'^upload/', utils.FileUploadView.as_view()),
    #     re_path(r'^upload/', FileUploadView.as_view()),
    path('<int:year>/gbstats', Gbstats.as_view(), name='test-list'),
    path('exportexcel', utils.export_data_to_excel, name='export-excel'),
    path('<int:year>/download/<str:name>',
         utils.FileDownloadListAPIView.as_view(),
         name='download-api'),
    path('<int:year>/programs', ProgramsGraduates.as_view(), name='courses'),
    path(
        'compare/<int:year1>/<int:year2>/<str:campus>/<str:institute>/<str:coursename>/<str:grad>',
        CompareYearsData.as_view(),
        name='compare'),
    path('<int:year>/updateprograms/<pk>',
         UpdateGraduatesWithPrograms.as_view(),
         name='data-update-view-with-programs'),
    path('logs', utils.log_edit_info, name='logs-api'),
#     path('<int:year>/highlights', HighlightsView.as_view(), name='Highlights'),

    # Dont touch
    # path('createinstances/<str:year>/', CreateInstances, name='CreateInstances'),
]
