from django.db import models

class Email(models.Model):
    name = models.CharField(max_length=30, blank=False)
    contact = models.CharField(max_length=300)


class Measurement(models.Model):
    fahrenheit = models.FloatField(default=45)

    def __str__(self):
        return f"The temperature is {self.fahrenheit}"

    def get_celsius(self):
        celsius = self.fahrenheit - 32 * 5/9
        super(Measurement, self).save(*args, **kwargs)
