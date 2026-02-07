from django import forms
from bookings.models import VehicleModel

class VehicleForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = ['name', 'type', 'price', 'vehicle_no', 'image1', 'image2', 'image3']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vehicle name'
            }),
            'vehicle_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Registration number'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per day',
                'min': 1
            }),
            'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


