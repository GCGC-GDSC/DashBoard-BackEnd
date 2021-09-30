from django.shortcuts import render
from . import Campus,Institue,UnderGraduates,PostGraduates

c = Campus.objects.all()
print(c)