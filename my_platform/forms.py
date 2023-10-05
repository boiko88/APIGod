from django.forms import ModelForm
from django import forms
from .models import Email

class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    actual_message = forms.CharField(widget=forms.Textarea)


class PasswordForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('very_easy', 'Very Easy'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES)
    length = forms.IntegerField(min_value=6, max_value=30)
