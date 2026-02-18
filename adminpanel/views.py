from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Sum
from django.contrib.auth.models import User
from bookings.models import VehicleModel, BookingModel
from .mixins import AdminRequiredMixin  
from .forms import VehicleForm
from django.views import View
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.models import User
from bookings.models import VehicleModel, BookingModel
from .mixins import AdminRequiredMixin
from django.views import View
from datetime import date


class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        # Counts
        total_users = User.objects.count()
        total_vehicles = VehicleModel.objects.count()
        total_bookings = BookingModel.objects.count()
        approved_bookings = BookingModel.objects.filter(status='APPROVED').count()
        total_revenue = BookingModel.objects.filter(status__in=['APPROVED', 'RETURNED']).aggregate(total=Sum('total_amount'))['total'] or 0
        total_fine = BookingModel.objects.aggregate(total=Sum('fine_amount'))['total'] or 0
        # Recent bookings
        recent_bookings = BookingModel.objects.select_related('user', 'vehicle').order_by('-id')[:5]
        # Simple chart data (last 7 bookings)
        revenue_series = list(
            BookingModel.objects.filter(
                status__in=['APPROVED', 'RETURNED']
            ).order_by('-id').values_list('total_amount', flat=True)[:7]
        )
        context = {
            'total_users': total_users,
            'total_vehicles': total_vehicles,
            'total_bookings': total_bookings,
            'approved_bookings': approved_bookings,
            'total_revenue': total_revenue,
            'total_fine': total_fine,
            'recent_bookings': recent_bookings,
            'revenue_series': revenue_series,
        }
        return render(request, 'adminview/admindashboard.html', context)




class ReturnBookingView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(BookingModel, id=booking_id)
        return render(request, 'adminview/return_booking.html', {'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(BookingModel, id=booking_id)
        today = date.today()
        booking.returned_date = today

        # Late return fine calculation
        if today > booking.end_date:
            late_days = (today - booking.end_date).days
            fine_per_day = 500  # you can change this
            booking.fine_amount = late_days * fine_per_day
        booking.status = 'RETURNED'
        booking.save()
        # Make vehicle available again
        vehicle = booking.vehicle
        vehicle.available = True
        vehicle.save()
        return redirect('adminpanel:admin-dashboard')




class ReturnBookingListView(AdminRequiredMixin, View):
    def get(self, request):
        bookings = BookingModel.objects.filter(status='APPROVED')
        return render(request, 'adminview/return_list.html', {'bookings': bookings})




class ReturnBookingView(AdminRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(
            BookingModel,
            id=pk,
            status='APPROVED'
        )

        returned_date = date.today()
        booking.returned_date = returned_date
        # Fine calculation
        if returned_date > booking.end_date:
            extra_days = (returned_date - booking.end_date).days
            booking.fine_amount = extra_days * booking.vehicle.price
        booking.status = 'RETURNED'
        booking.save()
        # Make vehicle available again
        vehicle = booking.vehicle
        vehicle.available = True
        vehicle.save()
        return redirect('adminpanel:return-list')




class AddVehicleView(AdminRequiredMixin, View):
    def get(self, request):
        form = VehicleForm()
        return render(request, 'adminview/add_vehicle.html', {'form': form})

    def post(self, request):
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:vehicle-list')
        return render(request, 'adminview/add_vehicle.html', {'form': form})

    
    
    


class VehicleListView(AdminRequiredMixin, View):
    def get(self, request):
        vehicles = VehicleModel.objects.all().order_by('-created_at')
        return render(request, 'adminview/vehicle_list.html', {'vehicles': vehicles})


class VehicleUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        vehicle = get_object_or_404(VehicleModel, id=pk)
        form = VehicleForm(instance=vehicle)
        return render(request, 'adminview/update_vehicle.html', {'form': form})

    def post(self, request, pk):
        vehicle = get_object_or_404(VehicleModel, id=pk)
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:vehicle-list')
        return render(request, 'adminview/update_vehicle.html', {'form': form})


class VehicleDeleteView(AdminRequiredMixin, View):
    def get(self, request, pk):
        vehicle = get_object_or_404(VehicleModel, id=pk)
        return render(request, 'adminview/delete_vehicle.html', {'vehicle': vehicle})

    def post(self, request, pk):
        vehicle = get_object_or_404(VehicleModel, id=pk)
        vehicle.delete()
        return redirect('adminpanel:vehicle-list')




class BookingHistoryView(AdminRequiredMixin, View):
    def get(self, request):
        bookings = BookingModel.objects.select_related('user','vehicle').order_by('created_at')
        return render(request,'adminview/booking_history.html',{'bookings':bookings})
