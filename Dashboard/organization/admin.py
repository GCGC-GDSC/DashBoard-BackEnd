from django.contrib import admin
from .models import (Institute, Campus, Stream)


class StreamAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Stream, StreamAdmin)


class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'inst_count']


admin.site.register(Campus, CampusAdmin)


class InstituteAdmin(admin.ModelAdmin):
    list_display = ['name', 'under_campus', 'stream']


admin.site.register(Institute, InstituteAdmin)
