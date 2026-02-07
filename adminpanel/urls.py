from django.urls import path
from .views import (
    AdminDashboardView,
    ReturnBookingListView,
    ReturnBookingView,
    AddVehicleView
)

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('returns/', ReturnBookingListView.as_view(), name='return-list'),
    path('return/<int:pk>/', ReturnBookingView.as_view(), name='return-booking'),
    path('add-vehicle/', AddVehicleView.as_view(), name='add-vehicle'),
]
