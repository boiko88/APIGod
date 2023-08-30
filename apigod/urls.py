
from django.contrib import admin
from django.urls import path
from my_platform import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('time', views.myTime, name="time"),
    path('crypto', views.crypto, name="crypto"),
    path('currency', views.currency, name="currency"),
    path('fmap', views.foliumMap, name="fmap"),
    path('gmap', views.googleMap, name="gmap"),
]
