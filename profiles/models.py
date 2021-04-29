from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from books.models import Book


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='userimg/', default='media/defaultPicture.png')
    bio = models.TextField(max_length=300)
    interest = ArrayField(
        models.CharField(max_length=100),
        size=10
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    books = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
