from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'designation', 'is_superuser', 'eid']


admin.site.register(User, UserAdmin)


class EditorInstitutesAdmin(admin.ModelAdmin):
    list_display = ['account', 'institute']


admin.site.register(EditorInstitutes, EditorInstitutesAdmin)
