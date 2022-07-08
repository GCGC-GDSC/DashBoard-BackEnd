from django.contrib import admin
from .models import (Institute, Campus, Stream, Courses, Programs)


class StreamAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Stream, StreamAdmin)


class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'inst_count']


admin.site.register(Campus, CampusAdmin)


class InstituteAdmin(admin.ModelAdmin):
    list_display = ['name', 'under_campus', 'stream']


admin.site.register(Institute, InstituteAdmin)

class InstituteAdmin(admin.ModelAdmin):
    list_display = ['name', 'under_campus', 'stream']

admin.site.register(Courses)

class ProgramsAdmin(admin.ModelAdmin):
    list_display = ['display_name','under_campus', 'under_institute','under_course','grad_type']

admin.site.register(Programs,ProgramsAdmin)