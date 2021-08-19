import datetime
import json
from .models import TourReservations, GuideTourMapping, GuideInfo


def process_data(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data['amount'])

    max_clientMap = {
        'bouldering':10,
        'hiking':25,
        'rock art':6,
        'technical climbing':6
    }
    tourReservationId = data["id"]
    tourReservation = TourReservations.objects.get(reservationId=tourReservationId)
    tourReservation.transaction_id = transaction_id
    tourReservation.tansaction_status = True
    tourReservation.transaction_amount = total
    tourReservation.save()
    getGuide = GuideInfo.objects.get(destination=tourReservation.destination)
    try:
        tourGuideMap = GuideTourMapping.objects.get(
            tourType=tourReservation.tourType,
            tourStyle=tourReservation.tourStyle,
            tourDate=tourReservation.tourDate,
            meetTime=tourReservation.meetTime,
            destination=tourReservation.destination
        )
        clients = tourGuideMap.clients
        tourClientData = tourReservation.__dict__
        tourClientData["_state"] = None
        clients[str(tourClientData["reservationId"])] = tourClientData
        tourGuideMap.clients = clients
        tourGuideMap.numberOfPersons += int(tourReservation.number_of_clients)
        tourGuideMap.save()

    except Exception as e:
        client = dict()
        tourClientData = tourReservation.__dict__
        del tourClientData["_state"]
        client[tourReservation.reservationId] = tourClientData
        GuideTourMapping.objects.create(
            tourType=tourReservation.tourType,
            tourStyle=tourReservation.tourStyle,
            tourDate=tourReservation.tourDate,
            meetTime=tourReservation.meetTime,
            clients=client,
            guide=getGuide.guide.id,
            destination=tourReservation.destination,
            numberOfPersons=int(tourReservation.number_of_clients)
        )   
