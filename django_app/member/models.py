from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            gender=None,
            age=None,
            latitude=None,
            hardness=None,
            password=None,
            ):
        user = self.model(
            email=email,
            gender=gender,
            age=age,
            latitude=latitude,
            hardness=hardness,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            gender=None,
            age=None,
            latitude=None,
            hardness=None,
            password=None,
            ):
        user = self.model(
            email=email,
            gender=gender,
            age=age,
            latitude=latitude,
            hardness=hardness,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICE = (('M', "Male"), ('F', "Female"),)
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICE,
                              null=True,blank=True
                              )
    age = models.DateField(null=True)
    latitude = models.FloatField(null=True)
    hardness = models.FloatField(null=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def position(self):
        return self.pk, self.latitude, self.hardness

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
