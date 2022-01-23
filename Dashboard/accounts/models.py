from django.db import models
from organization.models import Campus, Institute

ACCESS_LEVEL = (
    ('pg','PG'),
    ('ug', 'UG'),
    ('both','BOTH'),
)

class Accounts(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,
                                     default="",
                                     null=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE,
                                     default="",
                                     null=True)
    ug_pg = models.CharField(max_length=6, choices=ACCESS_LEVEL, default='both')
    can_edit = models.BooleanField(default=False)
