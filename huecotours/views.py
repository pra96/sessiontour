from django.contrib import messages
from users.models import User
from django.shortcuts import render, redirect
from requests import request
from .models import TourReservations, GuideInfo, Tours, GuideTourMapping
import json
# Create your views here.

def homepage(request):
    try:
        if 'is_authenticated' in request.session and request.session['is_authenticated']:
            return render(request, 'huecotours/tour-prices.html')
        return render(request, 'huecotours/tour-prices.html')
    except:
        return redirect('login')

def guides(request):
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        try:
            guides = User.objects.filter(is_guide = True)
            data = {}
            for ind, guide in enumerate(guides):
                currGuide = GuideInfo.objects.get(guide=guide)
                data[ind] = {
                    "guide":guide.id,
                    "name": guide.first_name + " " + guide.last_name,
                    "phoneNumber": "",
                    "email":guide.email,
                    "description": currGuide.description,
                    "price": currGuide.variable_price
                }
            return render(request, 'huecotours/guides.html', {'data':data})
        except:
            return render(request, 'huecotours/guides.html', {'data':{}})
        
    else:
        return redirect('login')

def requestTour(request):
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        if request.method == 'POST':
            get_user = User.objects.get(username=request.session['username'], first_name = request.session['first_name'])
            first_name = request.POST.get("first_name", False)
            last_name = request.POST.get("last_name", False)
            email_id = request.POST.get("email", False)
            mobile_phone = request.POST.get("phone", False)
            tourDate = request.POST.get("date", False)
            meetTime = request.POST.get("start_time", False)
            tourType = request.POST.get("tour_type", False)
            tourStyle = request.POST.get("tour_style", False)
            destination = request.POST.get("destination", False)
            number_of_person = request.POST.get("no_persons", False)
            booked_by_user = get_user.id
            try:
                try:
                    getGuide = GuideInfo.objects.get(destination=destination)
                except:
                    messages.INFO(request, "Guide Not Available for this locations")
                tourClient = TourReservations.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email_id=email_id,
                    mobile_phone=mobile_phone,
                    tourDate=tourDate,
                    meetTime=meetTime,
                    tourType=tourType,
                    tourStyle=tourStyle,
                    destination=destination,
                    numberOfPersons =number_of_person,
                    booked_by_user=booked_by_user,
                    guide_assigned=getGuide.guide.id
                )
                try:
                    tourGuideMap = GuideTourMapping.objects.get(
                        tourType=tourType,
                        tourStyle=tourStyle,
                        tourDate=tourDate,
                        meetTime=meetTime,
                        destination=destination
                    )
                    clients = tourGuideMap.clients
                    tourClientData = tourClient.__dict__
                    tourClientData["_state"] = None
                    clients[str(tourClientData["reservationId"])] = tourClientData
                    tourGuideMap.clients = clients
                    tourGuideMap.save()
                except:
                    client = dict()
                    tourClientData = tourClient.__dict__
                    del tourClientData["_state"]
                    client[tourClient.reservationId] = tourClientData
                    GuideTourMapping.objects.create(
                        tourType=tourType,
                        tourStyle=tourStyle,
                        tourDate=tourDate,
                        meetTime=meetTime,
                        clients=client,
                        guide=getGuide.guide.id,
                        destination=destination
                    )
                messages.success(request, "Registration Submitted")
            except Exception as e:
                messages.info(request, "Registration Failed")
        return render(request, 'huecotours/request-tour.html')
    else:
        return redirect('login')

def reserve(request):
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        publicTours = GuideTourMapping.objects.filter(tourStyle="public")
        privateTours = GuideTourMapping.objects.filter(tourStyle="private")
        return render(request, 'huecotours/reserve.html', {'public':publicTours, 'private':privateTours}) 
    return redirect('login') 

def tourPrice(request):
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        tour = Tours.objects.filter(isActive = True)
        data = {}
        for ind, t in enumerate(tour):
            if t.fixedCost == 0:
                cost = "$"+str(t.fixedCost) + "/Person"
            else:
                cost = "$" + str(t.fixedCost) + " + " + "$" + str(t.variableCost) +  "/Person"
            data[ind] = {
                "tourType":t.tourType,
                "tourStyle":t.tourStyle,
                "tourDescription":t.tourDescription ,
                "maxPersonAllowed":t.maxPersonAllowed,
                "cost":cost
            }
        return render(request, 'huecotours/tour-prices.html', {'data':data})
    
    else:
        return redirect('login')
    