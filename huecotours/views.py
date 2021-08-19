import re
from django.contrib import messages
from users.models import User
from django.shortcuts import render, redirect
from requests import request
from .models import TourReservations, GuideInfo, Tours, GuideTourMapping
import json
from django.http import JsonResponse
from .utils import process_data
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
                if currGuide.fix_price == 0:
                    price = "$" + str(currGuide.variable_price)+"/person"
                else:
                    price = "$" + str(currGuide.fix_price) +" + " + str(currGuide.variable_price)+"/person"

                if currGuide.priceType == "negotiable":
                    price = "negotiable"

                data[ind] = {
                    "guide":guide.id,
                    "name": guide.first_name + " " + guide.last_name,
                    "phoneNumber": currGuide.mobile_number,
                    "email":guide.email,
                    "description": currGuide.description,
                    "price": price
                }
            return render(request, 'huecotours/guides.html', {'data':data})
        except Exception as e:
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
            comments = request.POST.get("comments", False)
            booked_by_user = get_user.id
            if number_of_person is False:
                number_of_person = 1
            try:
                try:
                    getGuide = GuideInfo.objects.get(destination=destination)
                except:
                    messages.info(request, "Guide Not Available for this locations")
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
                    booked_by_user=booked_by_user,
                    guide_assigned=getGuide.guide.id,
                    number_of_clients=number_of_person,
                    comments=comments
                )
                max_clientMap = {
                    'bouldering':10,
                    'hiking':25,
                    'rock art':6,
                    'technical climbing':6
                }
                try:
                    tourGuideMap = GuideTourMapping.objects.get(
                        tourType=tourType,
                        tourStyle=tourStyle,
                        tourDate=tourDate,
                        meetTime=meetTime,
                        destination=destination
                    )

                    if tourGuideMap.numberOfPersons + int(number_of_person) >= max_clientMap[tourGuideMap.tourType]:
                        messages.info(request, "All Seats full for this tour, apply for another")
                        return render(request, 'huecotours/request-tour.html')
                except:
                    messages.info(request, "All Seats available for this tour")
                price_type = getGuide.priceType
                fix_price = getGuide.fix_price
                variable_price = getGuide.variable_price
                if price_type == 'negotiable':
                    total_amount = fix_price
                else:
                    total_amount = fix_price + variable_price*int(number_of_person)
                data = {
                    "amount":total_amount,
                    "name":first_name,
                    "tourReservationId": tourClient.reservationId
                }
                return render(request, 'huecotours/payment.html', { "data":data})
            except Exception as e:
                print(e)
                messages.info(request, "Registration Failed")
            return redirect('hoeco_reserve')
        return render(request, 'huecotours/request-tour.html')
    else:
        return redirect('login')

def reserve(request):
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        if request.method == 'POST':
            guideTourId = request.POST.get("product", False)
            guideTourMap = GuideTourMapping.objects.get(tourStyle="public", guideTourId=guideTourId)
            get_user = User.objects.get(username=request.session['username'], first_name = request.session['first_name'])
            tourClient = TourReservations.objects.create(
                    first_name=get_user.first_name,
                    last_name=get_user.last_name,
                    email_id=get_user.email,
                    tourDate=guideTourMap.tourDate,
                    meetTime=guideTourMap.meetTime,
                    tourType=guideTourMap.tourType,
                    tourStyle=guideTourMap.tourStyle,
                    destination=guideTourMap.destination,
                    booked_by_user=get_user.id,
                    guide_assigned=guideTourMap.guide,
                    number_of_clients=1
                )
            max_clientMap = {
                'bouldering':10,
                'hiking':25,
                'rock art':6,
                'technical climbing':6
            }
            getGuide = GuideInfo.objects.get(destination=guideTourMap.destination)
            if guideTourMap.numberOfPersons >= max_clientMap[guideTourMap.tourType]:
                messages.info(request, "All Seats full for this tour, apply for another")
                return render(request, 'huecotours/request-tour.html')
            price_type = getGuide.priceType
            fix_price = getGuide.fix_price
            variable_price = getGuide.variable_price
            if price_type == 'negotiable':
                total_amount = fix_price
            else:
                total_amount = variable_price + fix_price
            data = {
                "amount":total_amount,
                "name":get_user.first_name,
                "tourReservationId": tourClient.reservationId
            }
            return render(request, 'huecotours/payment.html', { "data":data})

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


def process_order(request):
    process_data(request)
    return JsonResponse('Payment submitted...', safe=False)
    