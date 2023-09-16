from django.forms import ModelForm
from django import forms
from .models import Email

class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    actual_message = forms.CharField(widget=forms.Textarea)


# class MeasurementForm(forms.Form):
#     fahrenheit = forms.FloatField()
#     celsius = fahrenheit-32*5/9


class FahrenheitForm(forms.Form):
    fahrenheit = forms.IntegerField()