from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import VehicleModel, BookingModel, OrderModel
from .forms import BookingForm, Order_form
from datetime import date
import razorpay
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse


class HomeViewUser(View):
    def get(self, request):
        vehicle = VehicleModel.objects.filter(available=True)
        return render(request, 'user/UserHome.html', {'view': vehicle})


class BookVehiclePage(View):
    def get(self, request, pk):
        vehicle = VehicleModel.objects.get(id=pk)
        return render(request, 'user/bookingvehicle.html', {'vehicle': vehicle})


@method_decorator(login_required, name="dispatch")
class BookingFormPage(View):
    def get(self, request, pk):
        vehicle = VehicleModel.objects.get(id=pk)
        form = BookingForm()
        return render(request, 'user/bookingform.html', {'vehicle': vehicle, 'form': form})

    def post(self, request, pk):
        vehicle = VehicleModel.objects.get(id=pk)
        form = BookingForm(request.POST)
        if not form.is_valid():
            return render(request, 'user/bookingform.html', {'vehicle': vehicle, 'form': form})

        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if start_date < date.today():
            form.add_error('start_date', 'Start date cannot be in the past')
            return render(request, 'user/bookingform.html', {'vehicle': vehicle, 'form': form})

        if end_date < start_date:
            form.add_error('end_date', 'End date must be after start date')
            return render(request, 'user/bookingform.html', {'vehicle': vehicle, 'form': form})

        booking = form.save(commit=False)
        booking.user = request.user
        booking.vehicle = vehicle
        total_days = (end_date - start_date).days
        booking.total_amount = total_days * vehicle.price
        booking.status = 'PENDING'
        booking.save()
        return redirect('bookings:payment', booking_id=booking.id)


@method_decorator(login_required, name="dispatch")
class PaymentView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(BookingModel, id=booking_id, user=request.user)
        form = Order_form()
        return render(request, 'user/payment.html', {'form': form, 'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(BookingModel, id=booking_id, user=request.user)
        form = Order_form(request.POST)
        if not form.is_valid():
            return render(request, 'user/payment.html', {'form': form, 'booking': booking})

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
            # MAKE VEHICLE UNAVAILABLE
            vehicle = booking.vehicle
            vehicle.available = False
            vehicle.save()
            return redirect('bookings:payment_success')

        # ONLINE
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
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


@method_decorator(login_required, name="dispatch")
class PaymentSuccessPage(View):
    def get(self, request):
        return render(request, 'user/payment_success.html')


@method_decorator(login_required, name="dispatch")
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


@method_decorator(login_required, name="dispatch")
class MyBookingsView(View):
    def get(self, request):
        bookings = BookingModel.objects.filter(user=request.user).select_related('vehicle').order_by('-created_at')
        return render(request, 'user/my_bookings.html', {'bookings': bookings})


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            msg = data.get("message", "").lower()

            if "book" in msg:
                reply = "Go to Vehicles page and click Book Now."
            elif "cancel" in msg:
                reply = "You can cancel from My Bookings before start date."
            elif "payment" in msg:
                reply = "We support COD and Online payment."
            elif "hello" in msg:
                reply = "Hello 👋 Welcome to Rentify."
            else:
                reply = "Sorry, I didn't understand. Try asking about booking, payment, or cancellation."

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": "Something went wrong"}, status=400)