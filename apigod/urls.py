
from django.contrib import admin
from django.urls import path
from my_platform import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('time', views.my_time, name="time"),
    path('crypto', views.crypto, name="crypto"),
    path('currency', views.currency, name="currency"),
    path('fmap', views.foliumMap, name="fmap"),
    path('gmap', views.google_map, name="gmap"),
    path('email', views.free_email, name="email"),
    path('weather', views.weather, name="weather"),
    path('measurement', views.measurement, name="measurement"),
    path('generate-password', views.generate_password, name="generate-password"),
    path('user-register', views.user_register, name="user-register"),
    path('logout-user/', views.logout_user, name="logout-user"),
    path('login-user/', views.login_user, name="login-user"),
]
