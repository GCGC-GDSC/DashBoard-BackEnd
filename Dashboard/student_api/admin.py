from django.contrib import admin
from .models import Campus, Institute, UnderGraduates, PostGraduates
# Register your models here.

admin.site.register(Campus)
admin.site.register(Institute)
admin.site.register(UnderGraduates)
admin.site.register(PostGraduates)