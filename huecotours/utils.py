import datetime
import json
from .models import TourReservations, GuideTourMapping, GuideInfo
from users.models import User


def process_data(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(request)
    data = json.loads(request.body)
    total = float(data['amount'])
    print(data)
    max_clientMap = {
        'bouldering':10,
        'hiking':25,
        'rock art':6,
        'technical climbing':6
    }
    try:
        tourReservationId = data["id"]
        tourReservation = TourReservations.objects.get(id=tourReservationId)
        tourReservation.transaction_id = transaction_id
        tourReservation.isAccept = True
        tourReservation.tansaction_status = True
        tourReservation.transaction_amount = total
        tourReservation.save()
        guide = User.objects.get(id=tourReservation.guide_assigned)
        getGuide = GuideInfo.objects.get(guide = guide) 
    except Exception as e:
        print(e)
