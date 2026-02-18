from django.urls import path
from adminpanel import views

app_name = 'adminpanel'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('returns/', views.ReturnBookingListView.as_view(), name='return-list'),
    path('return/<int:pk>/', views.ReturnBookingView.as_view(), name='return-booking'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle-list'),
    path('add-vehicle/', views.AddVehicleView.as_view(), name='add-vehicle'),
    path('update-vehicle/<int:pk>/', views.VehicleUpdateView.as_view(), name='vehicle-update'),
    path('delete-vehicle/<int:pk>/', views.VehicleDeleteView.as_view(), name='vehicle-delete'),
    path('booking-history/', views.BookingHistoryView.as_view(), name='booking-history'),

]
