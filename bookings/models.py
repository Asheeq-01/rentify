
from django.db import models
from django.contrib.auth.models import User
from datetime import date





from django.db import models

class VehicleModel(models.Model):
    VEHICLE_TYPE_CHOICES = [('BIKE', 'Bike'),('CAR', 'Car'),('VAN', 'Van'),]
    TRANSMISSION_CHOICES = [('AUTO', 'Automatic'),('MANUAL', 'Manual'),]
    FUEL_CHOICES = [('PETROL', 'Petrol'),('DIESEL', 'Diesel'),('ELECTRIC', 'Electric'),]
    name = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10,choices=VEHICLE_TYPE_CHOICES)
    price = models.PositiveIntegerField(help_text="Price per day")
    seats = models.PositiveIntegerField(default=2)
    transmission = models.CharField(max_length=10,choices=TRANSMISSION_CHOICES,default='AUTO')
    fuel_type = models.CharField(max_length=15,choices=FUEL_CHOICES,default='PETROL')
    image1 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image2 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image3 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True, help_text="Is the vehicle physically available for rent?")
    
    

    def is_available(self, start_date, end_date):
        if not self.available:
            return False
        return not BookingModel.objects.filter(
            vehicle=self,
            start_date__lte=end_date,
            end_date__gte=start_date,
            status__in=['PENDING', 'APPROVED']
        ).exists()


    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} ({self.vehicle_no})"





class BookingModel(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),    # Admin rejected
        ('CANCELLED', 'Cancelled'),  # User cancelled
        ('RETURNED', 'Returned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    PAYMENT_CHOICES = (
        ('ONLINE', 'Online Payment'),
        ('COD', 'Cash on Delivery'),
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='ONLINE'
    )

    
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name} ({self.status})"

    
    
    
    
    

    

class OrderModel(models.Model):
    booking = models.ForeignKey(
        BookingModel,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    order_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50)

    ordered_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} | Booking #{self.booking.id}"




