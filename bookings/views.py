from django.shortcuts import render,redirect
from django.views import View
from .models import VehicleModel,BookingModel,OrderModel
from .forms import BookingForm,Order_form
from datetime import date
import razorpay






class HomeViewUser(View):
    def get(self,request):
        vehicle=VehicleModel.objects.filter(available=True)
        return render(request,'user/UserHome.html',{'view':vehicle})
    
    
    
class BookVehiclePage(View):
    def get(self,request,pk):
        vehicle=VehicleModel.objects.get(id=pk)
        return render(request,'user/bookingvehicle.html',{'vehicle':vehicle})
    
    
    
    
class BookingFormPage(View):
    def get(self, request, pk):
        vehicle = VehicleModel.objects.get(id=pk)
        form = BookingForm()
        return render(request, 'user/bookingform.html', {
            'vehicle': vehicle,
            'form': form
        })

    def post(self, request, pk):
        vehicle = VehicleModel.objects.get(id=pk)
        form = BookingForm(request.POST)

        if not form.is_valid():
            return render(request, 'user/bookingform.html', {
                'vehicle': vehicle,
                'form': form
            })

        # ✅ USE cleaned_data (booking NOT created yet)
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # ❌ Validation
        if start_date < date.today():
            form.add_error('start_date', 'Start date cannot be in the past')
            return render(request, 'user/bookingform.html', {
                'vehicle': vehicle,
                'form': form
            })

        if end_date < start_date:
            form.add_error('end_date', 'End date must be after start date')
            return render(request, 'user/bookingform.html', {
                'vehicle': vehicle,
                'form': form
            })

        # ✅ NOW create booking
        booking = form.save(commit=False)
        booking.user = request.user
        booking.vehicle = vehicle

        total_days = (end_date - start_date).days 
        booking.total_amount = total_days * vehicle.price
        booking.status = 'PENDING'
        booking.save()

        return redirect('bookings:payment', booking_id=booking.id)



            
            
            
    
from django.shortcuts import get_object_or_404
from django.conf import settings

class PaymentView(View):

    def get(self, request, booking_id):
        booking = get_object_or_404(
            BookingModel,
            id=booking_id,
            user=request.user
        )
        form = Order_form()
        return render(request, 'user/payment.html', {
            'form': form,
            'booking': booking
        })



    def post(self, request, booking_id):
        booking = get_object_or_404(
            BookingModel,
            id=booking_id,
            user=request.user
        )

        form = Order_form(request.POST)
        if not form.is_valid():
            return render(request, 'user/payment.html', {
                'form': form,
                'booking': booking
            })

        order = form.save(commit=False)
        order.user = request.user
        order.booking = booking
        order.amount = booking.total_amount
        order.is_order = True

        # COD
        if order.payment_method == 'COD':
            order.save()

            booking.status = 'APPROVED'
            booking.save()

            # ✅ MAKE VEHICLE UNAVAILABLE
            vehicle = booking.vehicle
            vehicle.available = False
            vehicle.save()

            return redirect('bookings:payment_success')


        # ONLINE
        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        razorpay_order = client.order.create({
            'amount': int(booking.total_amount * 100),
            'currency': 'INR',
            'payment_capture': 1
        })

        order.order_id = razorpay_order['id']
        order.save()

        return render(request, 'user/razorpay.html', {
            'razorpay_order': razorpay_order,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'booking': booking
        })


# ✅ ONLY UI PAGE (GET)
class PaymentSuccessPage(View):
    def get(self, request):
        return render(request, 'user/payment_success.html')


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# ✅ ONLY RAZORPAY CALLBACK (POST)
@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(View):
    def post(self, request):
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        order = get_object_or_404(OrderModel, order_id=razorpay_order_id)

        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            return redirect('bookings:user-home')

        booking = order.booking

        # ✅ prevent double payment
        if booking.status == 'APPROVED':
            return redirect('bookings:payment_success')

        booking.status = 'APPROVED'
        booking.save()

        booking.vehicle.available = False
        booking.vehicle.save()

        return redirect('bookings:payment_success')



    
    



from django.contrib.auth.mixins import LoginRequiredMixin

class MyBookingsView(LoginRequiredMixin, View):
    def get(self, request):
        bookings = BookingModel.objects.filter(
            user=request.user
        ).select_related('vehicle').order_by('-created_at')

        return render(request, 'user/my_bookings.html', {
            'bookings': bookings
        })

    
    
    
    

