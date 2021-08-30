import imp
import re
from django.contrib import messages
from users.models import User
from django.shortcuts import render, redirect
from requests import request
from .models import TourReservations, GuideInfo, Tours, GuideTourMapping
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from .utils import process_data
# Create your views here.

def homepage(request):

    return render(request, 'huecotours/tour-prices.html')

def guides(request):

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

def requestTour(request):
    if request.method == 'POST':
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
        if number_of_person is False:
            number_of_person = 1
        try:
            tourReservation = TourReservations.objects.create(
                first_name=first_name,
                last_name=last_name,
                email_id=email_id,
                mobile_phone=mobile_phone,
                tourDate=tourDate,
                meetTime=meetTime,
                tourType=tourType,
                tourStyle=tourStyle,
                destination=destination,
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
                    tourType=tourReservation.tourType,
                    tourStyle=tourReservation.tourStyle,
                    tourDate=tourReservation.tourDate,
                    meetTime=tourReservation.meetTime,
                    destination=tourReservation.destination
                )
                if tourGuideMap.numberOfPersons + int(number_of_person) >= max_clientMap[tourGuideMap.tourType]:
                    messages.info(request, "All Seats full for this tour, apply for another")
                    return render(request, 'huecotours/request-tour.html')
                clients = tourGuideMap.clients
                tourClientData = tourReservation.__dict__
                tourClientData["_state"] = None
                tourClientData["uuid"] = str(tourClientData["uuid"])
                clients[str(tourClientData["id"])] = tourClientData
                tourGuideMap.clients = clients
                tourGuideMap.numberOfPersons += int(tourReservation.number_of_clients)
                tourGuideMap.save()

            except Exception as e:
                client = dict()
                tourClientData = tourReservation.__dict__
                del tourClientData["_state"]
                tourClientData["uuid"] = str(tourClientData["uuid"])
                client[str(tourReservation.id)] = tourClientData
                tourGuideMap = GuideTourMapping.objects.create(
                    tourType=tourReservation.tourType,
                    tourStyle=tourReservation.tourStyle,
                    tourDate=tourReservation.tourDate,
                    meetTime=tourReservation.meetTime,
                    clients=client,
                    destination=tourReservation.destination,
                    numberOfPersons=int(tourReservation.number_of_clients)
                )
            if tourGuideMap.numberOfPersons >= max_clientMap[tourGuideMap.tourType]:
                tourGuideMap.is_full = True
                tourGuideMap.save()

        except Exception as e:
            messages.info(request, "Registration Failed")
            return render(request, 'huecotours/request-tour.html')

        messages.info(request, "Registration Successfull")
        return redirect('hoeco_reserve')
    return render(request, 'huecotours/request-tour.html')

def reserve(request):
    # if request.method == 'POST':
    #     guideTourId = request.POST.get("product", False)
    #     guideTourMap = GuideTourMapping.objects.get(tourStyle="public", guideTourId=guideTourId)
    #     get_user = User.objects.get(username=request.session['username'], first_name = request.session['first_name'])
    #     tourClient = TourReservations.objects.create(
    #             first_name=get_user.first_name,
    #             last_name=get_user.last_name,
    #             email_id=get_user.email,
    #             tourDate=guideTourMap.tourDate,
    #             meetTime=guideTourMap.meetTime,
    #             tourType=guideTourMap.tourType,
    #             tourStyle=guideTourMap.tourStyle,
    #             destination=guideTourMap.destination,
    #             booked_by_user=get_user.id,
    #             guide_assigned=guideTourMap.guide,
    #             number_of_clients=1
    #         )
    #     max_clientMap = {
    #         'bouldering':10,
    #         'hiking':25,
    #         'rock art':6,
    #         'technical climbing':6
    #     }
    #     getGuide = GuideInfo.objects.get(destination=guideTourMap.destination)
    #     if guideTourMap.numberOfPersons >= max_clientMap[guideTourMap.tourType]:
    #         messages.info(request, "All Seats full for this tour, apply for another")
    #         return render(request, 'huecotours/request-tour.html')
    #     price_type = getGuide.priceType
    #     fix_price = getGuide.fix_price
    #     variable_price = getGuide.variable_price
    #     if price_type == 'negotiable':
    #         total_amount = fix_price
    #     else:
    #         total_amount = variable_price + fix_price
    #     data = {
    #         "amount":total_amount,
    #         "name":get_user.first_name,
    #         "tourReservationId": tourClient.reservationId
    #     }
    #     return render(request, 'huecotours/payment.html', { "data":data})

    not_full_tours = GuideTourMapping.objects.filter(is_full = False)
    full_tours = GuideTourMapping.objects.filter(is_full=True)
    return render(request, 'huecotours/reserve.html', {'not_full':not_full_tours, 'full':full_tours}) 

def tourPrice(request):
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

def Notification(request, uuid=None):
    tourReservation = TourReservations.objects.get(uuid=uuid)
    max_clientMap = {
        'bouldering':10,
        'hiking':25,
        'rock art':6,
        'technical climbing':6
    }
    guide = User.objects.get(id=tourReservation.guide_assigned)
    getGuideInfo = GuideInfo.objects.get(guide=guide)
    price_type = getGuideInfo.priceType
    fix_price = getGuideInfo.fix_price
    variable_price = getGuideInfo.variable_price
    if price_type == 'negotiable':
        total_amount = fix_price
    else:
        total_amount = variable_price + fix_price
    data = {
        "amount":total_amount,
        "name":tourReservation.first_name,
        "tourReservationId": tourReservation.id
    }
    return render(request, 'huecotours/payment.html', { "data":data})

def process_order(request):
    process_data(request)
    return JsonResponse('Payment submitted...', safe=False)
    

def GuideClaim(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        guide = User.objects.get(id=data["guide_id"])
        guideTourMapping = GuideTourMapping.objects.get(guideTourId=data["guidTourMapping"])
        guideTourMapping.guide = guide.id 
        guideTourMapping.save()
        for resevationId, reservationData in guideTourMapping.clients.items():
            tourReservations = TourReservations.objects.get(uuid=reservationData["uuid"])
            tourReservations.guide_assigned = guide.id
            tourReservations.is_notification_send = True
            tourReservations.save()
            body = "Hello " + reservationData["first_name"] + ", Your request has been approved by guide " + guide.first_name + " Please click here to complete the payment,"+ "http://127.0.0.1:8000/hueco_tanks/notification/"+reservationData["uuid"]
            send_mail('Your request for Tour Approved', 
                body,
                'tours@sessionsclimbing.com',
                [reservationData.email_id],
                fail_silently=False
            )
            print("Message Sent")
        return JsonResponse('Claimed submitted...', safe=False)
    return JsonResponse("Not claimed successfully")
