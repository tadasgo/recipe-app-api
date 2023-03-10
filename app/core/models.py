from typing import Union

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users"""

    # pass None in case we want to create unusable user
    def create_user(self, email: str, password: Union[str, None], **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError("User must have an email address")

        # same as defining new user model
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # sets and hashes password
        user.set_password(password)
        # save user model
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: Union[str, None]):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# AbstractBaseUser contains functionality for authentication but not fields
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # defines field used for authentication
    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """Recipe object"""

    # reference user model set in settings
    # if user obj deleted, related recipes will be deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    # also important for model display in django admin
    def __str__(self):
        return self.title
