from django.db import models

# Create your models here.
class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.TextField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.TextField(max_length=255)
    is_active = models.BooleanField(default=False)

    