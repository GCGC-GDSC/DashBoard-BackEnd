from django.db import models
from organization.models import Campus, Institute


ACCESS = [('view', 'VIEW'), ('edit_all', 'EDIT ALL'),('edit_some','EDIT SOME')]
CAMPUS = [('univ', 'UNIVERSITY'), ('vskp', 'VISAKHAPATNAM'),
          ('hyd', 'HYDERABAD'), ('blr', 'BENGALURU')]


class Accounts(models.Model):
    eid = models.CharField(max_length=10, unique=True, default=None)
    name = models.CharField(max_length=50, default="")
    designation = models.CharField(max_length=100, default="")
    university = models.CharField(max_length=15, choices=CAMPUS,default="vskp")
    email = models.EmailField(max_length=50)
    access = models.CharField(max_length=10, choices=ACCESS,default="view")

    def __str__(self):
        designation_serializer = str(self.designation).split(' ')
        designation_sort = ''.join(designation_serializer[:2])
        return str(self.eid) + " " + str(self.name) + " " + designation_sort

    class Meta:
        ordering = ('id',)


class EditorInstitutes(models.Model):
    account = models.ForeignKey(Accounts,
                                on_delete=models.CASCADE,
                                default=None)


    institute = models.ForeignKey(Institute,
                                  on_delete=models.CASCADE,
                                  default=None)

    def __str__(self):
        return str(self.account) + " " + str(self.institute)
