from django.shortcuts import render
from django.db.models import Q
from django.views import View
from bookings.models import VehicleModel
from django.db.models.functions import Cast
from django.db.models import CharField

class SearchView(View):
    def get(self, request):

        query = request.GET.get('q')
        products = VehicleModel.objects.all()
        
        if query:
            products = VehicleModel.objects.annotate(
                price_str=Cast('price', CharField())).filter(
                Q(name__icontains=query) |
                Q(vehicle_no__icontains=query) |
                Q(type__icontains=query) |
                Q(fuel_type__icontains=query) |
                Q(transmission__icontains=query) |
                Q(price_str__icontains=query)
            ).distinct()
        context = {
            'result': products,
            'query': query
        }
        return render(request,'user/search.html', context)
