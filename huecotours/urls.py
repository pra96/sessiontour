
from django.contrib import admin
from django.urls import path, include

from .import views

urlpatterns = [
    path('', views.homepage, name='hoeco_homepage'),
    path('guides', views.guides, name='hoeco_guides'),
    path('request-tour', views.requestTour, name= 'hoeco_request_tour'),
    path('reverse', view=views.reserve, name='hoeco_reserve'),
    path('tour-prices', view=views.tourPrice, name= 'hoeco_tour_price')
]