from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from organization.models import Campus, Institute
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save

ACCESS = [('view', 'VIEW'), ('edit_all', 'EDIT ALL'),
          ('edit_some', 'EDIT SOME')]
CAMPUS = [('univ', 'UNIVERSITY'), ('vskp', 'VISAKHAPATNAM'),
          ('hyd', 'HYDERABAD'), ('blr', 'BENGALURU')]


class UserManager(BaseUserManager):

    def create_user(self,
                    name,
                    email,
                    eid,
                    designation,
                    university,
                    access,
                    password=None):
        if name is None:
            raise TypeError('Users should have a name')
        if email is None:
            raise TypeError('Users should have a Email')
        if eid is None:
            raise TypeError('Users should have a eid')

        user = self.model(name=name,
                          eid=eid,
                          designation=designation,
                          university=university,
                          access=access,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, eid, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        designation = "admin"
        university = "univ"
        access = "edit_all"
        user = self.create_user(name, email, eid, designation, university,
                                access, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    eid = models.CharField(max_length=10, unique=True)
    designation = models.CharField(max_length=100, default="")
    university = models.CharField(max_length=15,
                                  choices=CAMPUS,
                                  default="vskp")
    access = models.CharField(max_length=10, choices=ACCESS, default="view")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'eid']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.designation

    def __str__(self):
        return self.eid + " " + self.name + " " + self.university


class EditorInstitutes(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    institute = models.ForeignKey(Institute,
                                  on_delete=models.CASCADE,
                                  default=None)

    def __str__(self):
        return str(self.account) + " " + str(self.institute)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
