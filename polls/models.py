from django.db import models

# Create your models here.


class User(models.Model):
    username = models.TextField()
    password = models.TextField()
