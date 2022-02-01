from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="GitamPlacments API",
        default_version='v1',
        description=
        "An internal project of University Dashboard for Career Fulfillment statistics. GCGC 🤝 GDSC",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('organization/', include('organization.urls')),
    path('account/',include('account.urls')),
    # path('data/', include('data.urls')),
    #path('company/', include('company.urls')),
]
