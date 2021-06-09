from django.db import models

from users.models import User


class Book(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pdf = models.ImageField(upload_to='pdf')
    audiobook = models.FileField(upload_to='audiobooks')
    last_read_time = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self)
