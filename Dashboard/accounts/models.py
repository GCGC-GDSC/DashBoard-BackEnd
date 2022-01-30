from django.db import models
from organization.models import Campus, Institute

GRAD = [
    ('pg', 'PG'),
    ('ug', 'UG'),
]


class Accounts(models.Model):
    eid = models.CharField(max_length=10, unique=True, default=None)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return str(self.eid) + " " + str(self.name)

class AccountsHead(Accounts):
    role = models.CharField(max_length=10,default="head")
    def __str__(self):
        return str(self.role)+" "+str(self.name)

class AccountsCampusLevel(Accounts):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.eid) + " " + str(self.campus)+ " " + self.name


class AccountsInstituteLevel(AccountsCampusLevel):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.eid) + " " + str(self.campus) + " " + str(self.institute) +" "+ self.name


class AccountsGraduationLevel(AccountsInstituteLevel):
    grad = models.CharField(max_length=4, choices=GRAD)

    def __str__(self):
        return str(self.eid) + " " + str(self.campus) + " " + str(self.institute) + " " + str(self.grad) + " " + self.name
