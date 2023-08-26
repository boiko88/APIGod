from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    context = {}
    return render(request, 'home.html', context)


def myTime(request):
    context = {}
    return render(request, 'time.html', context)


def crypto(request):
    context = {}
    return render(request, 'crypto.html', context)