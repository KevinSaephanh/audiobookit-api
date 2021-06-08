from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from books.models import Book
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Username field should be filled')
        if email is None:
            raise TypeError('Email field should be filled')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Password field should be filled')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(
        upload_to='userimg/',
        default='media/defaultPicture.png',
        max_length=255,
        null=True,
        blank=True
    )
    books = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email', 'password']

    objects = UserManager()

    def get_user_id(self):
        return self.pk

    def get_books(self):
        return Book.objects.filter(user=self.user)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.username
