from django.db import models

# Create your models here.
class User(models.Model):
    emailId = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=30)