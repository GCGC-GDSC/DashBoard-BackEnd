from django.contrib import admin
from .models import (Institute, Campus, Stream)

admin.site.register(Stream)
admin.site.register(Campus)
admin.site.register(Institute)
