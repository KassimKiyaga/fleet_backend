from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vehicle, Driver, Booking, Trip, Feedback, MaintenanceRecord, FuelRecord, Incident, Department

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user','created_at','status')

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ('user','created_at')

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelRecord
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
