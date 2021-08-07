from django.contrib import admin
from .models import TourReservations, Tours, GuideInfo, GuideTourMapping
# Register your models here.

admin.site.register(TourReservations)
admin.site.register(Tours)
admin.site.register(GuideInfo)
admin.site.register(GuideTourMapping)