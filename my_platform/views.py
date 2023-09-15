from django.shortcuts import render, redirect
from django.contrib import messages
import calendar
from datetime import datetime
import folium 
from .forms import EmailForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
import urllib.request
import json
from .models import Measurement
import requests



def home(request):
    now = datetime.now()
    current_year = now.year

    context = {
        'current_year': current_year,
    }
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
    now.strftime('%A')
    
    context = {
        'current_year': current_year,
        'current_day': current_day,
        'now': now,
        }
    return render(request, 'time.html', context)


def crypto(request):
    now = datetime.now()
    current_year = now.year

    context = {
        'current_year': current_year,
    }
    return render(request, 'crypto.html', context)


def currency(request):
    response = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = response.get('rates')
    now = datetime.now()
    current_year = now.year

    context = {
        'current_year': current_year,
    }
    return render(request, 'currency.html', context)


def foliumMap(request):
    now = datetime.now()
    current_year = now.year

    my_map = folium.Map(location=[19, -12], zoom_start=2)
    folium.Marker([59.43, 24.75], tooltip='Click to know more', popup='Tallinn').add_to(my_map)
    my_map = my_map._repr_html_()
    context = {
        'my_map': my_map,
        'current_year': current_year,
    }
    return render(request, 'fmap.html', context)


def googleMap(request):
    now = datetime.now()
    current_year = now.year

    context = {
        'current_year': current_year,
    }
    return render(request, 'gmap.html', context)


def freeEmail(request):
    now = datetime.now()
    current_year = now.year

    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            actual_message = form.actual_message['actual_message']

            html = render_to_string('send_report.html', {
                'name': name,
                'email': email,
                'actual_message': actual_message,
            })
            print('It works')
            send_mail('The report form is here', 
                      'This is the message',
                      'noreply@TonyBoiko88.com',
                      ['bo1ko.ant@yandex.com'], 
                      html_message=html)
            
            messages.success(request, 'The message was sent')
            return redirect('gmap')
    else:
        form = EmailForm()
        messages.warning(request, 'The message was not sent')


    context = {
        'form': form,
        'current_year': current_year,
    }
    return render(request, 'email.html', context)


def weather(request):
    now = datetime.now()
    current_year = now.year

    MAIN_URL = 'http://api.openweathermap.org/data/2.5/weather?'
    API_KEY = 'api_key'
    CITY = 'lat=55.75&lon=37.61' # Moscow
    CITY_1 = 'lat=59.26&lon=25.75' # Tallinn


    url = MAIN_URL + CITY + '&units=metric&appid=' + API_KEY

    response = requests.get(url).json()
    temp = round(response['main']['temp'], 1)
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    wind = response['wind']['speed']
    main = response['weather'][0]['main']
    description = response['weather'][0]['description']
    icon = response['weather'][0]['icon']
    city_name = response['name']

    # print(city_name)

    context = {
        'current_year': current_year,
        'response': response,
        'temp': temp,
        'city_name': city_name,
        'pressure': pressure,
        'humidity': humidity,
        'wind': wind,
        'main': main,
        'description': description,
        'icon': icon,
    }
    return render(request, 'weather.html', context)


def measurement(request):
    now = datetime.now()
    current_year = now.year

    # actualt_fahrenheit = Measurement.objects.all()

    fahrenheit = 48
    celcius = fahrenheit - 32 *5/9
    print(celcius)

    context = {
        'current_year': current_year,
        # 'actualt_fahrenheit': actualt_fahrenheit,
        'celcius': celcius,
    }
    return render(request, 'measurement.html', context)



