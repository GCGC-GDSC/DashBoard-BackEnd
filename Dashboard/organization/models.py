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
    campus = models.ForeignKey(Campus, default=None, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute,
                                  default=None,
                                  on_delete=models.CASCADE)
    course = models.CharField(max_length=10, default=None)
    is_ug = models.BooleanField(default=True)

    def __str__(self):
        return self.course
