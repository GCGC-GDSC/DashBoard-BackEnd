from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Accounts)
admin.site.register(AccountsHead)
admin.site.register(AccountsCampusLevel)
admin.site.register(AccountsInstituteLevel)
admin.site.register(AccountsGraduationLevel)

