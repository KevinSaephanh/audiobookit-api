from django.db import models


# Create your models here.
class Book(models.Model):
    pdf = models.ImageField(upload_to='pdf')
    audiobook = models.FileField(upload_to='audiobooks')
    last_read_time = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
