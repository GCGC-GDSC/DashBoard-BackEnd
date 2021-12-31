from django.db import models
from students.models import (Institute, Campus)


class Courses(models.Model):
    campus = models.ForeignKey(Campus, default=None, on_delete=models.CASCADE)
    institute = models.ForeignKey(
        Institute, default=None, on_delete=models.CASCADE)
    course = models.CharField(max_length=10, default="")
    is_ug = models.BooleanField(default=True)

    def __str__(self):
        return self.course


class Company(models.Model):
    name_of_the_company = models.CharField(max_length=50, default="")
    profile_offered = models.CharField(max_length=50, default="")
    package = models.DecimalField(max_digits=5, decimal_places=2)
    courses = models.ManyToManyField(Courses, through="CompanyCousesPlaced")

    def __str__(self):
        return self.name_of_the_company


class CompanyCousesPlaced(models.Model):
    company = models.ForeignKey(
        Company, default=None, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Courses, default=None, on_delete=models.CASCADE)
    selected = models.IntegerField(default=-1)

    def __str__(self):
        return "Placement Details for Company " + str(self.company) + " for " + str(self.course)
