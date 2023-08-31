from django.shortcuts import render
import calendar
from datetime import datetime
import folium 
import geocoder

def home(request):
    context = {}
    return render(request, 'home.html', context)


def myTime(request, year=datetime.now().year, month=datetime.now().strftime('%B'), current_day=datetime.now()):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    # Get current time
    now = datetime.now()
    current_year = now.year
    current_day = now.day
    now = datetime.now()
    now.strftime("%A")
    
    context = {
        'current_year': current_year,
        'current_day': current_day,
        'now': now,
        }
    return render(request, 'time.html', context)


def crypto(request):
    context = {}
    return render(request, 'crypto.html', context)


def currency(request):
    context = {}
    return render(request, 'currency.html', context)


def foliumMap(request):
    my_map = folium.Map(location=[19, -12], zoom_start=2)
    my_map = my_map._repr_html_()
    context = {
        'my_map': my_map,
    }
    return render(request, 'fmap.html', context)


def googleMap(request):
    context = {}
    return render(request, 'gmap.html', context)


