from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from books.models import Book
from utils.field_validator import FieldValidator


class Profile(models.Model):
    bio = models.TextField(max_length=300)
    interests = ArrayField(models.CharField(max_length=100), size=10)
    profile_pic = models.ImageField(
        upload_to='userimg/',
        default='media/defaultPicture.png',
        max_length=255,
        null=True,
        blank=True
    )


# Extension of the standard User model
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", min_length=7, max_length=50, unique=True)
    username = models.CharField(unique=True)
    password = models.CharField()
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True
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
        return self.user.pk

    def get_username(self):
        return self.user.username

    def get_profile(self):
        return Profile.objects.filter(user=self.user)

    def get_books(self):
        return Book.objects.filter(user=self.user)

    def __str__(self):
        return str(self.user)
