from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate, login, logout

import calendar
from datetime import datetime
import folium
import json
import requests
from requests import Session
import random
from geopy.geocoders import Nominatim
from pprint import pprint

from .forms import EmailForm, PasswordForm, CustomUserCreationForm


def home(request):
    context = {}
    return render(request, 'home.html', context)


def my_time(request, year=datetime.now().year, month=datetime.now().strftime('%B'), current_day=datetime.now()):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
   
    # Get current time
    now = datetime.now()
    current_day = now.day
    now = datetime.now()
    now.strftime('%A')
    
    context = {
        'current_day': current_day,
        'now': now,
        }
    return render(request, 'time.html', context)


def crypto(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
        'slug': 'bitcoin',
        'convert': 'USD',
    }

    coinmarketcap_key = conf_settings.COINMARKETCAP_KEY

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinmarketcap_key,
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    print(json.loads(response.text)['data']['1']['quote']['USD']['price'])

    bitcoin_rate = json.loads(response.text)['data']['1']['quote']['USD']['price']
    bitcoin_rate = round(bitcoin_rate, 1)

    parameters = {
        'slug': 'ethereum',
        'convert': 'USD',
    }

    response = session.get(url, params=parameters)
    print(json.loads(response.text)['data']['1027']['quote']['USD']['price'])

    ethereum_rate = json.loads(response.text)['data']['1027']['quote']['USD']['price']
    ethereum_rate = round(ethereum_rate, 1)

    context = {
        'bitcoin_rate': bitcoin_rate,
        'ethereum_rate': ethereum_rate,
    }
    return render(request, 'crypto.html', context)


def currency(request):
    # The actual key is hidden in .env file and imported from settings.py
    EXCHANGERATE_KEY = conf_settings.EXCHANGERATE_KEY

    # USD to RUB
    USD_RUB = requests.get(url='https://v6.exchangerate-api.com/v6/' + EXCHANGERATE_KEY + 'pair/USD/RUB/').json()
    USD_RUB = round(USD_RUB['conversion_rate'], 1)
    # EUR to RUB
    EUR_RUB = requests.get(url='https://v6.exchangerate-api.com/v6/' + EXCHANGERATE_KEY + 'pair/EUR/RUB/').json()
    EUR_RUB = round(EUR_RUB['conversion_rate'], 1)
    # CNY to RUB
    CNY_RUB = requests.get(url='https://v6.exchangerate-api.com/v6/' + EXCHANGERATE_KEY + 'pair/CNY/RUB/').json()
    CNY_RUB = round(CNY_RUB['conversion_rate'], 1)

    context = {
        'USD_RUB': USD_RUB,
        'EUR_RUB': EUR_RUB,
        'CNY_RUB': CNY_RUB,
    }
    return render(request, 'currency.html', context)


def foliumMap(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        geolocator = Nominatim(user_agent='myapp')
        location = geolocator.geocode(address)
        if location:
            my_map = folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
            folium.Marker([location.latitude, location.longitude], tooltip='Click to know more', popup=address).add_to(my_map)
            my_map = my_map._repr_html_()
            context = {
                'my_map': my_map,
                'address': address,
            }
            return render(request, 'fmap.html', context)
        else:
            error_message = 'Could not find location for address: {}'.format(address)
            context = {
                'error_message': error_message,
            }
            return render(request, 'fmap.html', context)
    else:
        my_map = folium.Map(location=[19, -12], zoom_start=2)
        folium.Marker([59.43, 24.75], tooltip='Click to know more', popup='Tallinn').add_to(my_map)
        my_map = my_map._repr_html_()
        context = {
            'my_map': my_map,
        }
        return render(request, 'fmap.html', context)


def google_map(request):
    context = {
    }
    return render(request, 'gmap.html', context)


def free_email(request):
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
    }
    return render(request, 'email.html', context)


def weather(request):
    MAIN_URL = 'http://api.openweathermap.org/data/2.5/weather?'
    API_KEY = conf_settings.WEATHER_KEY
    CITY = 'lat=55.75&lon=37.61'  # Moscow
    CITY_1 = 'lat=59.26&lon=25.75'  # Tallinn

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

    # print(response)

    MAIN_URL6 = 'http://api.openweathermap.org/data/2.5/forecast?'
    url6 = MAIN_URL6 + CITY + '&units=metric&appid=' + API_KEY

    response2 = requests.get(url6).json()
    data3h = response2['list'][1]
    temp3h = response2['list'][1]['main']['temp']
    description3h = response2['list'][1]['weather'][0]['description']
    icon3h = response2['list'][1]['weather'][0]['icon']
    # pprint(data3h)

    data6h = response2['list'][2]
    temp6h = response2['list'][2]['main']['temp']
    description6h = response2['list'][2]['weather'][0]['description']
    icon6h = response2['list'][2]['weather'][0]['icon']
    # pprint(data6h)

    data24h = response2['list'][8]
    temp24h = response2['list'][8]['main']['temp']
    description24h = response2['list'][8]['weather'][0]['description']
    icon24h = response2['list'][8]['weather'][0]['icon']
    # pprint(data24h)

    context = {
        'response': response,
        'temp': temp,
        'city_name': city_name,
        'pressure': pressure,
        'humidity': humidity,
        'wind': wind,
        'main': main,
        'description': description,
        'icon': icon,
        'temp3h': temp3h,
        'description3h': description3h,
        'icon3h': icon3h,
        'temp6h': temp6h,
        'description6h': description6h,
        'icon6h': icon6h,
        'data24h': data24h,
        'temp24h': temp24h,
        'description24h': description24h,
        'icon24h': icon24h,

    }
    return render(request, 'weather.html', context)


def measurement(request):
    context = {

    }
    return render(request, 'measurement.html', context)


def generate_password(request):
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    special_symbols = ['+', '-', '/', '*', '!', '&', '$', '#', '?', '=', '@',]
    length = 19
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    password = ''
    form = PasswordForm(request.POST)
    difficulty = form.initial.get('difficulty', 'very_easy')
    if form.is_valid():
        difficulty = form.cleaned_data['difficulty']
        length = form.cleaned_data['length']
        if difficulty == 'very_easy':
            charset = numbers
        elif difficulty == 'easy':
            charset = numbers + special_symbols
        elif difficulty == 'medium':
            charset = numbers + special_symbols + lowercase_letters
        else:
            charset = numbers + special_symbols + lowercase_letters + uppercase_letter

        password_list = random.choices(charset, k=length)
        password = ''.join(password_list)

    context = {
        'password': password,
        'form': form,
        'difficulty': difficulty,
        'length': length,
    }
    return render(request, 'generate_password.html', context)


def user_register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = form.cleaned_data['email']
            user.save()
            # authenticate and log in the user
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            print('It is ok!')
            return redirect('home')
        else:
            messages.error(
                request, 'Ooops, something went wrong during the registration')
            
    context = {
        'form': form,
        }
    
    return render(request, 'user_registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def login_user(request):
    if request.method == 'POST':
        # Get the username and password from the POST data
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Authenticate the user with the given username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated, log them in and redirect to the
            # store page
            login(request, user)
            return redirect('home')
        else:
            # If the user is not authenticated, show an error message
            messages.error(request, 'Username OR password does not exist')

    # If the request method is not POST, create an empty context dictionary
    context = {}

    return render(request, 'login.html', context)
