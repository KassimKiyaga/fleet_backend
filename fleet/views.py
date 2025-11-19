from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Vehicle, Driver, Booking, Trip, Feedback, MaintenanceRecord, FuelRecord, Incident, Department
from .serializers import (
    VehicleSerializer, BookingSerializer, TripSerializer, FeedbackSerializer,
    MaintenanceSerializer, FuelSerializer, IncidentSerializer, DepartmentSerializer
)
from rest_framework.permissions import IsAuthenticated


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='PENDING')


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def start(self, request):
        booking_id = request.data.get('booking_id')
        driver_id = request.data.get('driver_id')
        start_odometer = request.data.get('start_odometer')

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({'detail':'Booking not found'}, status=404)

        trip = Trip.objects.create(
            booking=booking,
            driver_id=driver_id,
            start_time=timezone.now(),
            start_odometer=start_odometer,
            active=True
        )
        booking.status = 'APPROVED'
        booking.save()
        return Response(TripSerializer(trip).data, status=201)

    @action(detail=False, methods=['post'])
    def complete(self, request):
        trip_id = request.data.get('trip_id')
        end_odometer = request.data.get('end_odometer')

        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return Response({'detail':'Trip not found'}, status=404)

        trip.end_time = timezone.now()
        trip.end_odometer = end_odometer
        trip.active = False
        trip.save()
        return Response(TripSerializer(trip).data)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all().order_by('-created_at')
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]


class FuelViewSet(viewsets.ModelViewSet):
    queryset = FuelRecord.objects.all().order_by('-created_at')
    serializer_class = FuelSerializer
    permission_classes = [IsAuthenticated]


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


# Manual maintenance check endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def run_maintenance_check(request):
    today = timezone.now().date()
    due = Vehicle.objects.filter(next_due_date__lte=today)
    results = []
    for v in due:
        rec = MaintenanceRecord.objects.create(vehicle=v, description="Auto reminder: maintenance due")
        results.append({'vehicle': v.reg_no, 'due_date': str(v.next_due_date)})
    return Response({'due_count': len(results), 'vehicles': results})
