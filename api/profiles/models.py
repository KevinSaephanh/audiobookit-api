from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from api.books.models import Book

# Extension of the standard User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(max_length=300)
    interests = ArrayField(
        models.CharField(max_length=100),
        size=10
    )
    profile_pic = models.ImageField(
        upload_to='userimg/',
        default='media/defaultPicture.png',
        null=True,
        blank=True
    )
    books = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def get_user_id(self):
        return self.user.pk

    def get_username(self):
        return self.user.username

    def get_books(self):
        return Book.objects.filter(user=self.user)

    def __str__(self):
        return str(self.user)
