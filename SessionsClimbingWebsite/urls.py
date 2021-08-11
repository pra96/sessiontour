"""SessionsClimbingWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from huecotours import urls
from users.views import signup,login , logout
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import users
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('climbing', views.climbing, name='climbing'),
    path('about_us', views.about_us, name='about_us'),
    path('yoga_fit', views.yoga_fit, name='yoga_fit'),
    path('youth_programs', views.youth_programs, name='youth_programs'),
    path('cafe_lounge', views.cafe_lounge, name='cafe_lounge'),
    path('coming_soon', views.under_construction, name='under_construction'),
    path('shop/', include('shop.urls')),
    path('events/', include('events.urls')),
    path('hueco_tanks/', include('huecotours.urls')),
    path("login/", login, name="login"),
    path("logout/", logout , name="logout"),
    path('signup/', signup, name="signup"),
]
