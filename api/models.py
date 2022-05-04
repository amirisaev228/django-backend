import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=120)

class Book(models.Model):
    name = models.CharField(max_length=120)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    author = models.CharField(max_length=5500)
    description = models.TextField()
    image = models.CharField(max_length=5500)
    price = models.FloatField()

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        token = jwt.encode({
            'id': self.pk,
            'exp': '10000000000'
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Order(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)

