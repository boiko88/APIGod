
from django.contrib import admin
from django.urls import path
from my_platform import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('time', views.myTime, name="time"),
    path('crypto', views.crypto, name="crypto"),
    path('form', views.myForm, name="form"),
]
