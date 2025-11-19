from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleViewSet, BookingViewSet, TripViewSet, FeedbackViewSet,
    MaintenanceViewSet, FuelViewSet, IncidentViewSet, DepartmentViewSet,
    run_maintenance_check
)

router = DefaultRouter()
router.register('vehicles', VehicleViewSet)
router.register('bookings', BookingViewSet)
router.register('trips', TripViewSet)
router.register('feedback', FeedbackViewSet)
router.register('maintenance', MaintenanceViewSet)
router.register('fuel', FuelViewSet)
router.register('incidents', IncidentViewSet)
router.register('departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('jobs/run_maintenance_check/', run_maintenance_check),
]
