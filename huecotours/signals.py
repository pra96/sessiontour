from http.client import FAILED_DEPENDENCY
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.shortcuts import render

from .models import GuideInfo, TourReservations

# @receiver(post_save, sender=TourReservations)
# def payment_integration(instance, request, **kwargs):
#     try:
#         guide_id = instance.guide_assigned
#         number_of_persons = instance.number_of_clients
#         guide = GuideInfo.objects.get(guide_id=guide_id)
#         price_type = guide.priceType
#         fix_price = guide.fix_price
#         variable_price = guide.variable_price
#         if price_type == 'negotiable':
#             total_amount = fix_price
#         else:
#             total_amount = variable_price + fix_price*number_of_persons
        
#         if request.method == 'POST':
            

#             return "success"

#         return render(request, 'huecotours/payment.html', {"amount":total_amount, "name":instance.first_name})


#     except ObjectDoesNotExist:
#         return "failed"