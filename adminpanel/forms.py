from django import forms
from bookings.models import VehicleModel

class VehicleForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = ['fuel_type', 'name', 'vehicle_no', 'type', 'price', 'seats', 'transmission', 'available', 'image1', 'image2', 'image3']
        widgets = {
            'fuel_type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }

