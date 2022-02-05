from django.contrib import admin
from .models import *

admin.site.register(EditorInstitutes)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'eid']


admin.site.register(User, UserAdmin)