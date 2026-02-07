from django.contrib import admin

from .models import VehicleModel,BookingModel,OrderModel

admin.site.register(VehicleModel)
admin.site.register(BookingModel)
admin.site.register(OrderModel)


