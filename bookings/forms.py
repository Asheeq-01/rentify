from django import forms
from .models import VehicleModel,BookingModel,OrderModel
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model=BookingModel
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'min': date.today().isoformat(),
                    'class': 'form-control',
                    'required': True
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'min': date.today().isoformat(),
                    'class': 'form-control',
                    'required': True
                }
            ),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get('start_date')
    #     end_date = cleaned_data.get('end_date')
    #     #  Both dates must be selected
    #     if not start_date or not end_date:
    #         raise forms.ValidationError("Both start date and end date are required.")
    #     #  Start date cannot be in the past
    #     if start_date < date.today():
    #         raise forms.ValidationError("Start date cannot be in the past.")
    #     #  End date must be after start date
    #     if end_date <= start_date:
    #         raise forms.ValidationError("End date must be after start date.")
    #     #  Minimum booking = 1 day
    #     if (end_date - start_date).days < 1:
    #         raise forms.ValidationError("Minimum booking duration is 1 day.")
    #     return cleaned_data


class Order_form(forms.ModelForm):
    payment_choice=(('COD','COD'),('ONLINE','ONLINE'))
    payment_method=forms.ChoiceField(choices=payment_choice)
    class Meta:
        model=OrderModel
        fields=['address','phone','payment_method']