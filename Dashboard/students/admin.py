from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib import admin
from django.urls import reverse
from django.urls import path
from django import forms
from .models import *
from import_export import resources
from tablib import Dataset
from import_export.admin import ImportExportModelAdmin, ImportMixin, ImportForm, ConfirmImportForm

class GraduatesResource(resources.ModelResource):
    class meta:
        model = Graduates

class ExcelImportForm(forms.Form):
    excel_upload = forms.FileField()

class GraduatesAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-excel/', self.upload_excel), ]
        return new_urls + urls

    def upload_excel(self, request):

        if request.method == "POST":
            graduate_resource = GraduatesResource()
            dataset = Dataset()
            excel_file = request.FILES["excel_upload"]

            if not excel_file.name.endswith('.xlsx'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            imported_data = dataset.load(excel_file.read(), format='xlsx')
            print("imported_data: ", imported_data)

            print("data 1", imported_data[0])
            """
            for data in imported_data:

                value = Graduates(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11],
                    data[12],
                    data[13],
                    data[14]
                )
                value.save()"""

        form = ExcelImportForm()
        data = {"form": form}
        return render(request, "admin/excel_upload.html", data)

admin.site.register(Graduates, GraduatesAdmin)
