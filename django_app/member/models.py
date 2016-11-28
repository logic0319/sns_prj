from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            gender,
            age,
            password=None,
            ):
        user = self.model(
            email=email,
            gender=gender,
            age=age,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            gender,
            age,
            password=None,
            ):
        user = self.model(
            email=email,
            gender=gender,
            age=age,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    gender = models.BooleanField()
    age = models.DateField()
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['gender', 'age']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

