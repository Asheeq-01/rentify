from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('home/', views.HomeViewUser.as_view(), name="user-home"),
    path('booking-vehicle/<int:pk>/', views.BookVehiclePage.as_view(), name='bookingVehicle'),
    path('booking-vehicle/<int:pk>/book/', views.BookingFormPage.as_view(), name='book-form'),

    path('payment/<int:booking_id>/', views.PaymentView.as_view(), name="payment"),

    # Razorpay callback (POST)
    path('payment-callback/', views.PaymentSuccessView.as_view(), name='payment_callback'),

    # Success UI (GET)
    path('payment-success/', views.PaymentSuccessPage.as_view(), name='payment_success'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),

]


