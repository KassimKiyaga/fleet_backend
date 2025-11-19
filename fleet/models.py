from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    reg_no = models.CharField(max_length=30, unique=True)
    model = models.CharField(max_length=100, blank=True)
    odometer = models.PositiveIntegerField(default=0)
    next_due_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.reg_no} - {self.model}"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_no = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.user.username

class Booking(models.Model):
    STATUS_CHOICES = [('PENDING','PENDING'), ('APPROVED','APPROVED'), ('REJECTED','REJECTED')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class Trip(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    start_odometer = models.PositiveIntegerField(null=True, blank=True)
    end_odometer = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=False)

class FuelRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    liters = models.FloatField()
    odometer = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

class Feedback(models.Model):
    trip = models.ForeignKey(Trip, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Incident(models.Model):
    trip = models.ForeignKey(Trip, null=True, blank=True, on_delete=models.SET_NULL)
    reported_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    photo = models.ImageField(upload_to='incidents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
