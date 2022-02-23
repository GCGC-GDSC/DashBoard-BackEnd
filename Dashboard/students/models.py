from django.db import models
from datetime import date
from organization.models import (Institute, Campus)


class Graduates(models.Model):
    under_campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    under_institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    is_ug = models.BooleanField(default=True)

    total_students = models.IntegerField(default=0)
    total_final_years = models.IntegerField(default=0)
    total_higher_study_and_pay_crt = models.IntegerField(default=0)
    total_opted_for_higher_studies_only = models.IntegerField(default=0)
    total_not_intrested_in_placments = models.IntegerField(default=0)

    # total_backlogs = models.IntegerField(default=0)
    total_backlogs_opted_for_placements = models.IntegerField(default=0)
    total_backlogs_opted_for_higherstudies = models.IntegerField(default=0)
    total_backlogs_opted_for_other_career_options = models.IntegerField(
        default=0)

    total_offers = models.IntegerField(default=0)
    total_multiple_offers = models.IntegerField(default=0)
    highest_salary = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         default=0.0)
    average_salary = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         default=0.0)
    lowest_salary = models.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        default=0.0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    @property
    def total_students_eligible(self):
        return (self.total_final_years - self.total_higher_study_and_pay_crt -
                self.total_opted_for_higher_studies_only -
                self.total_not_intrested_in_placments -
                self.total_backlogs_opted_for_placements)

    @property
    def total_placed(self):
        return self.total_offers - self.total_multiple_offers

    @property
    def total_yet_to_place(self):
        return self.total_students_eligible - self.total_placed

    @property
    def under_institute_name(self):
        return str(self.under_institute)

    @property
    def under_campus_name(self):
        return str(self.under_campus)

    @property
    def total_backlogs(self):
        return (self.total_backlogs_opted_for_higherstudies +
                self.total_backlogs_opted_for_placements +
                self.total_backlogs_opted_for_other_career_options)

    def __str__(self):
        institute = str(self.under_institute)
        campus = str(self.under_campus)
        if self.is_ug:
            return 'UG ' + institute + " " + campus
        else:
            return 'PG ' + institute + " " + campus

    class Meta:
        unique_together = ("under_campus", "under_institute", "is_ug")


'''class ExcelData(models.Model):
    uploadedFile = models.FileField(upload_to="UploadedFiles/")'''
