from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name='events'),
    path('<str:event_id>', views.event_view, name='event_view')

]
