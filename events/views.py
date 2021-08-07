from django.shortcuts import render
from . models import *
from datetime import datetime


def events(request):
    context = {
        'events': Event.objects.all(),
        'today': datetime.today().date()
    }
    return render(request, 'events/events.html', context)


def event_view(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'title': event.title,
        'date': event.date_time.date(),
        'time': event.date_time.time(),
        'description': event.description,
        'image': event.image_url
    }
    return render(request, 'events/event_view.html', context)
