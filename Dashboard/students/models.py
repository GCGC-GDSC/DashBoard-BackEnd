from django.db import models


class Campus(models.Model):
    name = models.CharField(max_length=30, default="", unique=True)
    inst_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Institute(models.Model):
    name = models.CharField(max_length=10, default="")
    under_campus = models.ForeignKey(Campus,
                                     on_delete=models.CASCADE,
                                     null=True)

    @property
    def campus_name(self):
        return str(self.under_campus)

    def __str__(self):
        return self.name


class Graduates(models.Model):
    under_campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    under_institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    total_students = models.IntegerField(default=0)
    total_final_years = models.IntegerField(default=0)
    total_higher_study_and_pay_crt = models.IntegerField(default=0)
    total_not_intrested_in_placments = models.IntegerField(default=0)
    total_backlogs = models.IntegerField(default=0)
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
    is_ug = models.BooleanField(default=True)

    @property
    def total_students_eligible(self):
        return self.total_final_years - (self.total_backlogs +
                                         self.total_not_intrested_in_placments)

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

    def __str__(self):
        institute = str(self.under_institute)
        if self.is_ug:
            return 'UG ' + institute
        else:
            return 'PG ' + institute
