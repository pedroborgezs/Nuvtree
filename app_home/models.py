from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.TextField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)


