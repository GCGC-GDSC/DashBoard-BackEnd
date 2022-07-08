from django.db import models


class Stream(models.Model):
    name = models.CharField(max_length=20, default=None, unique=True)

    def __str__(self):
        return self.name


class Campus(models.Model):
    name = models.CharField(max_length=30, default=None, unique=True)
    inst_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Institute(models.Model):
    name = models.CharField(max_length=10, default=None)
    under_campus = models.ForeignKey(Campus,
                                     on_delete=models.CASCADE,
                                     default=None,
                                     null=True)
    stream = models.ForeignKey(Stream,
                               on_delete=models.CASCADE,
                               default=None,
                               null=True)

    @property
    def campus_name(self):
        return str(self.under_campus)

    def __str__(self):
        return self.name


class Courses(models.Model):
    course = models.CharField(max_length=10, default=None)

    def __str__(self):
        return self.course


class Programs(models.Model):
    under_campus = models.ForeignKey(Campus,
                                     on_delete=models.CASCADE,
                                     default=None,
                                     null=True)
    under_institute = models.ForeignKey(Institute,
                                        on_delete=models.CASCADE,
                                        default=None,
                                        null=True)
    under_course = models.ForeignKey(Courses,
                                     on_delete=models.CASCADE,
                                     default=None,
                                     null=True)
    name = models.CharField(max_length=36, default=None)
    is_ug = models.BooleanField(default=False)

    @property
    def campus_name(self):
        return str(self.under_campus)
    
    @property
    def institute_name(self):
        return str(self.under_institute)

    @property
    def grad_type(self):
        return "UG" if self.is_ug else "PG"
    
    @property
    def display_name(self):
        return f"{self.name} ( {self.under_institute} {self.under_course} {self.grad_type} )"
    class Meta:
        unique_together = ("under_campus", "under_institute", "name", "is_ug")

    def __str__(self):
        return f"{self.name} ( {self.under_institute} {self.under_course} {self.grad_type} )"