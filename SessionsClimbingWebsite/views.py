from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from events.models import Event
from shop.models import *
from SessionsClimbingWebsite import settings


def homepage(request):
    if request.method == 'POST':
        form = request.POST
        subject = f"{form['contact_name']} has reached out via the Website!!"
        message = f"Contact Details\n"\
                  f"-------------------------------------\n"\
                  f"Name: {form['contact_name']}\n"\
                  f"Email: {form['contact_email']}\n"\
                  f"Phone: {form['contact_phone']}\n" \
                  f"-------------------------------------\n"\
                  f"Message: {form['contact_message']}\n"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['tours@sessionsclimbing.com']
        )
        messages.info(request, "Thank you for reaching out! We'll get back to you as soon as possible!")
    products = Product.objects.all()
    events = Event.objects.all()
    context = {
        'products': products,
        'events': events,
    }
    return render(request, 'website/homepage.html', context)


def climbing(request):
    return render(request, 'website/climbing.html', {
        'events': Event.objects.all()
    })


def about_us(request):
    return render(request, 'website/about-us.html')


def yoga_fit(request):
    return render(request, 'website/yoga-fit.html', {
        'events': Event.objects.all()
    })


def youth_programs(request):
    return render(request, 'website/youth-programs.html')


def cafe_lounge(request):
    return render(request, 'website/cafe-lounge.html')


def under_construction(request):
    return render(request, 'website/under-construction.html')
