from django.contrib import admin
from .models import Campus, Institue, UnderGraduates, PostGraduates
# Register your models here.

admin.site.register(Campus)
admin.site.register(Institue)
admin.site.register(UnderGraduates)
admin.site.register(PostGraduates)