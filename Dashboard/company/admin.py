from django.contrib import admin
from .models import (Courses, Company, CompanyCousesPlaced)

admin.site.register(Courses)
admin.site.register(Company)
admin.site.register(CompanyCousesPlaced)
