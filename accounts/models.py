from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from books.models import Book
from utils.field_validator import FieldValidator
from rest_framework_simplejwt.tokens import RefreshToken


# Extension of the standard User model
class Account(AbstractBaseUser):
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

    def clean(self):
        FieldValidator.validateUsername(self.username)
        FieldValidator.validatePassword(self.password)

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
        return self.user
