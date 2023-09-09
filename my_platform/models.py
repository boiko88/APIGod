from django.db import models

class Email(models.Model):
    name = models.CharField(max_length=30, blank=False)
    contact = models.CharField(max_length=300)
