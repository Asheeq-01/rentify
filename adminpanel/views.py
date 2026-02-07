from django.shortcuts import render
from django.views.generic import  TemplateView, CreateView
# Create your views here.

from django.db.models import Sum
from django.contrib.auth.models import User

from bookings.models import VehicleModel, BookingModel
from .mixins import AdminRequiredMixin   # make sure this exists
from .forms import VehicleForm


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'adminview/admindashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔢 Counts
        context['total_users'] = User.objects.count()
        context['total_vehicles'] = VehicleModel.objects.count()
        context['total_bookings'] = BookingModel.objects.count()
        context['approved_bookings'] = BookingModel.objects.filter(
            status='APPROVED'
        ).count()

        # 💰 Financials
        context['total_revenue'] = (
            BookingModel.objects.filter(
                status__in=['APPROVED', 'RETURNED']
            ).aggregate(total=Sum('total_amount'))['total'] or 0
        )

        context['total_fine'] = (
            BookingModel.objects.aggregate(
                total=Sum('fine_amount')
            )['total'] or 0
        )

        # 🕒 Recent bookings
        context['recent_bookings'] = BookingModel.objects.select_related(
            'user', 'vehicle'
        ).order_by('-id')[:5]

        # 📊 Chart data (last 7 bookings)
        revenue_series = list(
            BookingModel.objects.filter(
                status__in=['APPROVED', 'RETURNED']
            ).order_by('-id').values_list('total_amount', flat=True)[:7][::-1]
        )

        max_revenue = max(revenue_series) if revenue_series else 1
        bars = []

        for i, value in enumerate(revenue_series):
            height = int((value / max_revenue) * 80)
            bars.append({
                'x': i * 20,
                'height': height,
                'y': 100 - height,
                'value': value
            })

        context['bars'] = bars

        return context




from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from bookings.models import BookingModel

class ReturnBookingView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(BookingModel, id=booking_id)
        return render(request, 'adminview/return_booking.html', {
            'booking': booking
        })

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




from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from bookings.models import BookingModel
from .mixins import AdminRequiredMixin


class ReturnBookingListView(AdminRequiredMixin, View):
    def get(self, request):
        bookings = BookingModel.objects.filter(status='APPROVED')
        return render(request, 'adminview/return_list.html', {
            'bookings': bookings
        })


from django.shortcuts import get_object_or_404, redirect
from datetime import date

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



from django.urls import reverse_lazy
class AddVehicleView(AdminRequiredMixin, CreateView):
    model = VehicleModel
    form_class = VehicleForm
    template_name = 'adminView/add_vehicle.html'
    # Ensure 'vehicle_list' is a valid URL name in your urls.py
    success_url = reverse_lazy("add-vehicle")