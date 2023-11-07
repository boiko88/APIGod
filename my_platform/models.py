from django.db import models
from django.contrib.auth.models import User


class Email(models.Model):
    name = models.CharField(max_length=30, blank=False)
    contact = models.CharField(max_length=300)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(blank=True, max_length=250)
